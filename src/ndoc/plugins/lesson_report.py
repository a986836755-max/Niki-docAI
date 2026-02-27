"""
Lesson Report Plugin (Action).
Generates _LESSONS.md (Lessons Learned) from ECS data.
Ported from lesson_flow.
"""
from pathlib import Path
from typing import Dict, Any, List
from ndoc.sdk.interfaces import ActionPlugin
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType
from ndoc.core.templates import render_document
from datetime import datetime
from ndoc.parsing import scanner

class LessonReportPlugin(ActionPlugin):
    """
    Action plugin to generate _LESSONS.md.
    """
    
    def ndoc_generate_docs(self, context: KernelContext):
        print("[LessonReport] Generating _LESSONS.md...")
        
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        lessons = []
        
        print(f"[LessonReport] Scanning {len(files)} files for lessons...")
        
        try:
            # We assume scanner can resolve relative paths correctly if we pass correct root.
            # Context usually doesn't store root explicitly, but we can guess.
            root = Path.cwd() 
            
            for f in files:
                path = f.path
                if not path.exists(): continue
                
                try:
                    result = scanner.scan_file(path, root)
                    if result and result.lessons:
                        for l in result.lessons:
                            lessons.append({
                                "file": path,
                                "rel_path": f.id,
                                "content": l['content'],
                                "line": l['line']
                            })
                except Exception:
                    pass
        except Exception as e:
            print(f"[LessonReport] Error during scan: {e}")
            return

        if not lessons:
            print("[LessonReport] No @LESSON tags found.")
            return

        # Render
        lines = []
        # Header format
        # lines.append("# Lessons Learned (Project Memory)")
        # lines.append("> @CONTEXT: Experience | @TAGS: @LESSON")
        
        for l in lessons:
            link = f"[{l['rel_path']}]({l['rel_path']}#L{l['line']})"
            lines.append(f"*   **{l['content']}**")
            lines.append(f"    *   Context: {link}")
            
        content = "\n".join(lines)
        
        doc = render_document(
            "lessons.md.tpl",
            title="Lessons Learned",
            context="Experience | Memory",
            tags="@LESSON",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content=content,
            lessons_count=len(lessons)
        )
        
        # Write
        try:
            output_path = root / "_LESSONS.md"
            output_path.write_text(doc, encoding="utf-8")
            print(f"[LessonReport] Written to: {output_path}")
        except Exception as e:
            print(f"[LessonReport] Failed to write: {e}")
