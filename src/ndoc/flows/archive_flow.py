# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: New flows (like `capability_flow.py`) must be registered in `entry.py` to ensure ...
# *   **Auto-Provisioning**: `capability_flow` acts as the project's "immune system", proactively detecting and install...
# *   **Doctor Integration**: `doctor_flow` should reuse the `CapabilityManager` logic to verify system health, rather ...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Project Archiving & Memory.
业务流：项目归档与记忆提取。将已完成任务移入历史并提取关键决策。
"""
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from ..core import fs, io
from ..parsing import scanner
from ..models.config import ProjectConfig

def run(config: ProjectConfig) -> bool:
    """
    Execute Archive Flow.
    Scans the project for memory markers (@DECISION, @LESSON, @INTENT, !RULE)
    and aggregates them into _MEMORY.md.
    """
    root_path = config.scan.root_path
    memory_file = root_path / "_MEMORY.md"
    
    print(f"🧠 Scanning for project memories in {root_path}...")
    
    # 1. Scan all files
    # Fix: config.scan.extensions instead of include_extensions
    # Also need to create a proper FileFilter instance
    # fs.FileFilter expects: ignore_patterns: Set[str], allow_extensions: Set[str]
    # But wait, fs.FileFilter is a dataclass.
    # We need to construct it properly.
    
    # Let's check fs.py signature again.
    # @dataclass class FileFilter: ignore_patterns, allow_extensions, spec
    
    filter_config = fs.FileFilter(
        ignore_patterns=set(config.scan.ignore_patterns),
        allow_extensions=set(config.scan.extensions)
    )
    
    decisions = []
    lessons = []
    intents = set()
    rules = []
    
    # Init VectorDB for Auto-Knowledge Distillation
    vdb = None
    try:
        from ..brain.vectordb import VectorDB
        vdb = VectorDB(root_path)
    except:
        pass
    
    files = list(fs.walk_files(root_path, config.scan.ignore_patterns))
    
    docs_to_embed = []
    metas_to_embed = []
    ids_to_embed = []
    
    for file_path in files:
        # Skip _MEMORY.md itself to avoid recursion if we scan .md files
        if file_path.name == "_MEMORY.md":
            continue
            
        try:
            # Use scanner to extract metadata
            result = scanner.scan_file(file_path, root_path)
            
            # Prepare for VectorDB Embedding
            # We embed:
            # 1. Decisions/Lessons content
            # 2. File Docstrings (High-level summary)
            
            rel_p = fs.get_relative_path(file_path, root_path)
            
            # Embed Docstring if available
            if result.docstring:
                 docs_to_embed.append(result.docstring)
                 metas_to_embed.append({"source": str(rel_p), "type": "docstring"})
                 ids_to_embed.append(f"doc_{rel_p}")
            
            # Aggregate Decisions
            for item in result.decisions:
                content = item.get("content", "")
                decisions.append({
                    "file": file_path,
                    "line": item.get("line", 0),
                    "content": content
                })
                # Embed Decision
                docs_to_embed.append(content)
                metas_to_embed.append({"source": str(rel_p), "type": "decision"})
                ids_to_embed.append(f"dec_{rel_p}_{item.get('line',0)}")
                
            # Aggregate Lessons
            for item in result.lessons:
                content = item.get("content", "")
                lessons.append({
                    "file": file_path,
                    "line": item.get("line", 0),
                    "content": content
                })
                # Embed Lesson
                docs_to_embed.append(content)
                metas_to_embed.append({"source": str(rel_p), "type": "lesson"})
                ids_to_embed.append(f"les_{rel_p}_{item.get('line',0)}")
                
            # Aggregate Intents
            for item in result.intents:
                if isinstance(item, str):
                    intents.add(item)
            
            # Aggregate Rules (!RULE)
            for item in result.memories:
                if item.get("type") == "RULE":
                    content = item.get("content", "")
                    rules.append({
                        "file": file_path,
                        "line": item.get("line", 0),
                        "content": content
                    })
                    # Embed Rule
                    docs_to_embed.append(content)
                    metas_to_embed.append({"source": str(rel_p), "type": "rule"})
                    ids_to_embed.append(f"rul_{rel_p}_{item.get('line',0)}")
                    
        except Exception as e:
            # print(f"⚠️ Failed to scan {file_path.name}: {e}")
            pass

    # Update VectorDB
    if vdb and docs_to_embed:
        print(f"🧠 Embedding {len(docs_to_embed)} knowledge fragments into VectorDB...")
        vdb.add_documents(docs_to_embed, metas_to_embed, ids_to_embed)

    # 2. Generate Content
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
            rel_path = fs.get_relative_path(d['file'], root_path)
            link = f"[`{d['file'].name}:{d['line']}`]({rel_path}#L{d['line']})"
            lines.append(f"*   {link}: {d['content']}")
    lines.append("")
    
    # Lessons
    lines.append("## 2. Lessons (@LESSON)")
    if not lessons:
        lines.append("*   *(No lessons recorded)*")
    else:
        for l in lessons:
            rel_path = fs.get_relative_path(l['file'], root_path)
            link = f"[`{l['file'].name}:{l['line']}`]({rel_path}#L{l['line']})"
            lines.append(f"*   {link}: {l['content']}")
    lines.append("")
    
    # Rules
    lines.append("## 3. Distributed Rules (!RULE)")
    if not rules:
        lines.append("*   *(No local rules found)*")
    else:
        for r in rules:
            rel_path = fs.get_relative_path(r['file'], root_path)
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
    
    # 3. Write to file
    io.write_text(memory_file, content)
    print(f"✅ Memory updated: {memory_file.name}")
    
    return True
