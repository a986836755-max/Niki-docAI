"""
Mind Map Plugin (Action).
Generates _MIND.md (Intent Index) from ECS data.
Ported from mind_flow.
"""
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict
from ndoc.sdk.interfaces import ActionPlugin
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType
from ndoc.core.templates import render_document
from datetime import datetime
from ndoc.parsing import scanner

class MindMapPlugin(ActionPlugin):
    """
    Action plugin to generate _MIND.md.
    """
    
    def ndoc_generate_docs(self, context: KernelContext):
        print("[MindMap] Generating _MIND.md...")
        
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        intents = defaultdict(list)
        
        print(f"[MindMap] Scanning {len(files)} files for intents...")
        
        try:
            root = Path.cwd()
            
            for f in files:
                path = f.path
                if not path.exists(): continue
                
                try:
                    result = scanner.scan_file(path, root)
                    if result and result.intents:
                        for intent in result.intents:
                            key = intent.lower().strip()
                            intents[key].append(f.id)
                except Exception:
                    pass
        except Exception as e:
            print(f"[MindMap] Error during scan: {e}")
            return

        if not intents:
            print("[MindMap] No @INTENT tags found.")
            return

        # Render
        lines = []
        
        for intent in sorted(intents.keys()):
            display_title = intent.title()
            lines.append(f"## {display_title}")
            for rel_path in sorted(set(intents[intent])):
                lines.append(f"*   [{rel_path}]({rel_path})")
            lines.append("")
            
        content = "\n".join(lines)
        
        doc = render_document(
            "mind.md.tpl",
            title="Mental Map (Intent Index)",
            context="Mental Map | Intent",
            tags="@MIND",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content=content,
            intents_count=len(intents)
        )
        
        # Write
        try:
            output_path = root / "_MIND.md"
            output_path.write_text(doc, encoding="utf-8")
            print(f"[MindMap] Written to: {output_path}")
        except Exception as e:
            print(f"[MindMap] Failed to write: {e}")
