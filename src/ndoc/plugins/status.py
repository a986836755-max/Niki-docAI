"""
Status Report Plugin (Ported from Status Flow).
"""
import re
from pathlib import Path
from typing import List, Dict, Any
from ndoc.sdk.interfaces import SensorPlugin, ActionPlugin
from ndoc.sdk.models import Entity, MetaComponent, SyntaxComponent
from ndoc.kernel.context import KernelContext
from ndoc.core.templates import render_document

# Regex for TODOs
TODO_PATTERN = re.compile(r'#\s*(TODO|FIXME|XXX):\s*(.*)', re.IGNORECASE)

class StatusPlugin(SensorPlugin, ActionPlugin):
    """
    1. Sensor: Scans files for TODO comments (MetaComponent).
    2. Action: Generates _STATUS.md based on collected MetaComponents.
    """
    
    def ndoc_process_syntax(self, entity: Entity) -> Dict[str, Any]:
        """
        Mock implementation: Just read file content and find TODOs.
        In real world, this would use Tree-sitter or reuse SyntaxComponent.
        """
        todos = []
        try:
            # Read file content
            # In a real system, we might query SyntaxComponent first
            content = entity.path.read_text(encoding="utf-8", errors="ignore")
            
            for i, line in enumerate(content.splitlines(), 1):
                match = TODO_PATTERN.search(line)
                if match:
                    tag, msg = match.groups()
                    todos.append({
                        "line": i,
                        "tag": tag.upper(),
                        "msg": msg.strip(),
                        "content": line.strip()
                    })
                    
        except Exception:
            pass
            
        return {"todos": todos} if todos else {}

    def ndoc_generate_docs(self, context: KernelContext):
        """
        Generate _STATUS.md from ECS data.
        """
        # Query: Find all entities with MetaComponent
        # But wait, how do we know which ones have TODOs?
        # We query all entities, and check their MetaComponent
        
        # 1. Collect Data
        todo_list = []
        # TODO: Add query method to Context to filter by Component field?
        # For now, iterate all MetaComponents
        
        # Get all entities that have MetaComponent
        # Note: In our current simple Kernel, we query entities that HAVE a component type.
        entities_with_meta = context.query(MetaComponent)
        print(f"[DEBUG] Found {len(entities_with_meta)} entities with MetaComponent")
        
        for eid in entities_with_meta:
            entity = context.entities[eid]
            meta = context.get_component(eid, MetaComponent)
            if meta and meta.todos:
                for item in meta.todos:
                    todo_list.append({
                        "file": entity.id,
                        "line": item['line'],
                        "tag": item['tag'],
                        "msg": item['msg']
                    })
        print(f"[DEBUG] Found {len(todo_list)} TODO items")
                    
        # 2. Render Template
        # Reuse existing render_document
        from datetime import datetime
        
        # Format todo content for template
        # Simple markdown list
        content_lines = []
        for t in todo_list:
            content_lines.append(f"- `[{t['tag']}]` **{t['file']}:{t['line']}** {t['msg']}")
            
        todo_content = "\n".join(content_lines) if content_lines else "No pending tasks found."
        
        doc = render_document(
            "status.md.tpl",
            title="Project Status",
            context="Task Tracking",
            tags="@STATUS",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            todo_content=todo_content
        )
        
        # 3. Write Output
        # In a real system, we might write to a DocComponent first
        # For pilot, just write file
        output_path = context.entities[list(context.entities.keys())[0]].path.parent / "_STATUS_NEW.md" 
        # Hacky: just use root of first entity. 
        # Ideally context should know root.
        
        # Let's assume root is passed or stored in context.
        # For now, print to stdout to verify pilot.
        print(f"--- Generated Status Doc Preview ({len(todo_list)} items) ---")
        
        # Write to disk to ensure we can verify it
        try:
            output_path = Path.cwd() / "_STATUS.md"
            output_path.write_text(doc, encoding="utf-8")
            print(f"[StatusReport] Written to: {output_path}")
        except Exception as e:
            print(f"[StatusReport] Failed to write: {e}")
            if entities_with_meta:
                 output_path = context.entities[entities_with_meta[0]].path.parent / "_STATUS.md"
                 output_path.write_text(doc, encoding="utf-8")
                 print(f"[StatusReport] Written to fallback: {output_path}")
