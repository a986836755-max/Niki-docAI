"""
Map Report Plugin (Action).
Generates _MAP.md (Project Structure) from ECS data.
Uses MetaComponent for file summaries.
"""
from pathlib import Path
from typing import Dict, Any, List
from ndoc.sdk.interfaces import ActionPlugin, hookimpl
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType, MetaComponent
from ndoc.core.templates import render_document
from ndoc.views import map as map_view
from datetime import datetime

class MapReportPlugin(ActionPlugin):
    """
    Action plugin to generate _MAP.md.
    """
    
    @hookimpl
    def ndoc_generate_docs(self, context: KernelContext):
        print("[MapReport] Generating _MAP.md...")
        
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        if not files:
            return

        # Determine root
        root = context.root_path if hasattr(context, 'root_path') else Path.cwd()
        
        # Build Summary Cache from Components
        summary_cache = {}
        for f in files:
            try:
                meta = context.get_component(f.id, MetaComponent)
                if meta and meta.docstring:
                    # Simple summary extraction from docstring first line
                    summary = meta.docstring.strip().split('\n')[0]
                    summary_cache[f.path] = summary
            except KeyError:
                pass
        
        # Reconstruct Tree Logic
        # Since map_view expects a recursive function that lists directories,
        # but we have flat entities.
        # We can simulate fs.list_dir by grouping entities by parent.
        
        # Group by parent
        dir_map = {}
        for f in files:
            parent = f.path.parent
            if parent not in dir_map:
                dir_map[parent] = []
            dir_map[parent].append(f)
            
        # Also need to know subdirectories for each directory
        # We can infer this from all parents in dir_map keys
        all_dirs = set(dir_map.keys())
        # Add intermediate dirs
        for d in list(all_dirs):
            curr = d
            try:
                while curr != root:
                    curr.relative_to(root)
                    parent = curr.parent
                    if parent == curr: break
                    all_dirs.add(parent)
                    curr = parent
            except ValueError: pass
        all_dirs.add(root)
        
        subdir_map = {}
        for d in all_dirs:
            parent = d.parent
            if parent not in subdir_map:
                subdir_map[parent] = set()
            subdir_map[parent].add(d)

        def build_tree_lines_from_ecs(current_path: Path, level: int = 0) -> List[str]:
            lines = []
            
            # 1. Subdirectories
            subdirs = sorted(list(subdir_map.get(current_path, [])))
            for d in subdirs:
                if d == current_path: continue # Should not happen
                lines.append(map_view.format_dir_entry(d.name, level))
                lines.extend(build_tree_lines_from_ecs(d, level + 1))
                
            # 2. Files
            current_files = sorted(dir_map.get(current_path, []), key=lambda x: x.name)
            for f in current_files:
                lines.append(map_view.format_file_entry(f.path, root, level, summary_cache))
                
            return lines

        tree_lines = build_tree_lines_from_ecs(root)
        tree_content = "\n".join(tree_lines)
        
        # Render
        doc = render_document(
            "map.md.tpl",
            title="Project Map",
            context="Map | Project Structure",
            tags="@MAP",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tree_content=tree_content
        )
        
        target_file = root / "_MAP.md"
        try:
            # Simple write
            # TODO: preserve markers if needed, but for now overwrite is safer for consistency
            from ndoc.core import io
            io.write_text(target_file, doc)
            print(f"[MapReport] Written: {target_file}")
        except Exception as e:
            print(f"[MapReport] Failed to write {target_file}: {e}")
