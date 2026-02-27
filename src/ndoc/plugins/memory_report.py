"""
Memory Report Plugin (Action).
Scans for memory markers (@DECISION, @LESSON, etc.) and generates _MEMORY.md.
Also supports vector embedding of memories.
"""
from pathlib import Path
from typing import Dict, Any, List
from ndoc.sdk.interfaces import ActionPlugin, hookimpl
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType, MetaComponent, MemoryComponent
from ndoc.core.templates import render_document
from datetime import datetime
from ndoc.core import io, fs

class MemoryReportPlugin(ActionPlugin):
    """
    Action plugin to generate _MEMORY.md.
    """
    
    @hookimpl
    def ndoc_generate_docs(self, context: KernelContext):
        print("[MemoryReport] Generating _MEMORY.md...")
        
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        root = context.root_path if hasattr(context, 'root_path') else Path.cwd()
        
        decisions = []
        lessons = []
        rules = []
        intents = set()
        
        # Prepare for VectorDB
        docs_to_embed = []
        metas_to_embed = []
        ids_to_embed = []
        
        for f in files:
            try:
                mem = context.get_component(f.id, MemoryComponent)
                meta = context.get_component(f.id, MetaComponent)
                
                if not mem: continue
                
                rel_p = f.id # Entity ID is relative path
                
                # Embed Docstring
                if meta and meta.docstring:
                     docs_to_embed.append(meta.docstring)
                     metas_to_embed.append({"source": str(rel_p), "type": "docstring"})
                     ids_to_embed.append(f"doc_{rel_p}")
                
                # Process Decisions
                for item in mem.decisions:
                    content = item.get("content", "")
                    line = item.get("line", 0)
                    decisions.append({
                        "file": f.path,
                        "line": line,
                        "content": content
                    })
                    docs_to_embed.append(content)
                    metas_to_embed.append({"source": str(rel_p), "type": "decision"})
                    ids_to_embed.append(f"dec_{rel_p}_{line}")
                    
                # Process Lessons
                for item in mem.lessons:
                    content = item.get("content", "")
                    line = item.get("line", 0)
                    lessons.append({
                        "file": f.path,
                        "line": line,
                        "content": content
                    })
                    docs_to_embed.append(content)
                    metas_to_embed.append({"source": str(rel_p), "type": "lesson"})
                    ids_to_embed.append(f"les_{rel_p}_{line}")
                    
                # Process Intents
                for item in mem.intents:
                    if isinstance(item, str):
                        intents.add(item)
                        
                # Process Rules
                for item in mem.memories:
                    if item.get("type") == "RULE":
                        content = item.get("content", "")
                        line = item.get("line", 0)
                        rules.append({
                            "file": f.path,
                            "line": line,
                            "content": content
                        })
                        docs_to_embed.append(content)
                        metas_to_embed.append({"source": str(rel_p), "type": "rule"})
                        ids_to_embed.append(f"rul_{rel_p}_{line}")
                        
            except KeyError:
                pass
                
        # Update VectorDB
        try:
            from ndoc.brain.vectordb import VectorDB
            vdb = VectorDB(root)
            if docs_to_embed:
                print(f"🧠 [MemoryReport] Syncing {len(docs_to_embed)} knowledge fragments to VectorDB...")
                vdb.add_documents(docs_to_embed, metas_to_embed, ids_to_embed)
        except Exception as e:
            # print(f"[MemoryReport] VectorDB sync skipped: {e}")
            pass
            
        # Generate Content
        lines = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lines.append(f"# Project Memory")
        lines.append(f"> @CONTEXT: Memory | Knowledge Base | @TAGS: @MEMORY")
        lines.append(f"> 最后更新 (Last Updated): {timestamp}")
        lines.append("")
        
        # Decisions
        lines.append("## 1. Decisions (@DECISION)")
        if not decisions:
            lines.append("*   *(No decisions recorded)*")
        else:
            for d in decisions:
                rel_path = fs.get_relative_path(d['file'], root)
                link = f"[`{d['file'].name}:{d['line']}`]({rel_path}#L{d['line']})"
                lines.append(f"*   {link}: {d['content']}")
        lines.append("")
        
        # Lessons
        lines.append("## 2. Lessons (@LESSON)")
        if not lessons:
            lines.append("*   *(No lessons recorded)*")
        else:
            for l in lessons:
                rel_path = fs.get_relative_path(l['file'], root)
                link = f"[`{l['file'].name}:{l['line']}`]({rel_path}#L{l['line']})"
                lines.append(f"*   {link}: {l['content']}")
        lines.append("")
        
        # Rules
        lines.append("## 3. Distributed Rules (!RULE)")
        if not rules:
            lines.append("*   *(No local rules found)*")
        else:
            for r in rules:
                rel_path = fs.get_relative_path(r['file'], root)
                link = f"[`{r['file'].name}:{r['line']}`]({rel_path}#L{r['line']})"
                lines.append(f"*   {link}: {r['content']}")
        lines.append("")

        # Intents
        lines.append("## 4. Intents (@INTENT)")
        if not intents:
            lines.append("*   *(No intents recorded)*")
        else:
            for i in sorted(list(intents)):
                lines.append(f"*   {i}")
        lines.append("")
        
        content = "\n".join(lines)
        
        memory_file = root / "_MEMORY.md"
        io.write_text(memory_file, content)
        print(f"[MemoryReport] Written to: {memory_file}")
