"""
Context Report Plugin (Action).
Generates recursive _AI.md files for each directory.
Using ECS Components to generate detailed documentation.
"""
from pathlib import Path
from typing import Dict, Any, List, Set
from collections import defaultdict
from ndoc.sdk.interfaces import ActionPlugin, hookimpl
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType, MetaComponent, SymbolComponent, GraphComponent
from ndoc.core.templates import render_document
from ndoc.models.context import FileContext
from ndoc.views import context as context_view
from datetime import datetime

class ContextReportPlugin(ActionPlugin):
    """
    Action plugin to generate _AI.md in each directory.
    This is the core "Recursive Context" feature.
    """
    
    @hookimpl
    def ndoc_generate_docs(self, context: KernelContext):
        print("[ContextReport] Generating _AI.md files...")
        
        # 1. Group Files by Directory
        dir_map: Dict[Path, List[Entity]] = defaultdict(list)
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        
        root_path = context.root_path if hasattr(context, 'root_path') else Path.cwd()
        
        for f in files:
            if f.path and f.path.exists():
                dir_map[f.path.parent].append(f)
            
        # 2. Iterate each directory and generate _AI.md
        count = 0
        
        all_dirs = set(dir_map.keys())
        # Add intermediate directories
        for d in list(all_dirs):
            current = d
            try:
                while current != root_path:
                    # Check if current is relative to root_path
                    current.relative_to(root_path)
                    
                    parent = current.parent
                    if parent == current: break
                    
                    all_dirs.add(parent)
                    current = parent
            except ValueError:
                pass
                
        all_dirs.add(root_path)
        
        for dir_path in all_dirs:
            lines = []
            lines.append("## @STRUCTURE")
            
            # 1. Subdirectories
            subdirs = set()
            for d in all_dirs:
                if d == dir_path: continue
                try:
                    rel = d.relative_to(dir_path)
                    if len(rel.parts) == 1:
                        subdirs.add(d)
                except ValueError:
                    pass
            
            if subdirs:
                for subdir in sorted(subdirs, key=lambda x: x.name):
                     link = f"*   **[{subdir.name}/]({subdir.name}/_AI.md#L1)**"
                     lines.append(link)

            # 2. Files
            dir_files = dir_map.get(dir_path, [])
            sorted_files = sorted(dir_files, key=lambda x: x.name)
            
            for f in sorted_files:
                # Construct FileContext for view rendering
                f_ctx = FileContext(
                    path=f.path,
                    rel_path=f.id,
                    tags=[],
                    sections={},
                    symbols=[],
                    imports=[],
                    docstring="",
                    memories=[],
                    description=""
                )
                
                # Fill from Components
                try:
                    meta = context.get_component(f.id, MetaComponent)
                    if meta:
                        f_ctx.docstring = meta.docstring
                        # Convert Component Tags (str) to Model Tags (Tag) if needed
                        # But view currently doesn't use tags heavily for formatting structure
                except KeyError: pass
                
                try:
                    sym_comp = context.get_component(f.id, SymbolComponent)
                    if sym_comp:
                        f_ctx.symbols = sym_comp.symbols
                except KeyError: pass
                
                try:
                    graph_comp = context.get_component(f.id, GraphComponent)
                    if graph_comp:
                        f_ctx.imports = set(graph_comp.imports)
                except KeyError: pass
                
                # Render using View
                summary = context_view.format_file_summary(f_ctx, root=dir_path)
                lines.append(summary)
                
                sym_list = context_view.format_symbol_list(f_ctx, root_path=root_path)
                if sym_list:
                    lines.append(sym_list)
            
            if not subdirs and not dir_files:
                lines.append("*   *No structural content.*")
            
            content = "\n".join(lines)
            
            # Format memories (if we have MemoryComponent later)
            memory_content = ""
            
            doc = render_document(
                "ai.md.tpl",
                title=f"Context: {dir_path.name}",
                context=f"Recursive Context | {dir_path.name}",
                tags="@AI",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                content=content, # Deprecated in new tpl?
                file_table=content, # New tpl uses this
                memory_content=memory_content,
                rules_section="*No local rules defined (Pilot)*"
            )
            
            try:
                output_path = dir_path / "_AI.md"
                if not dir_path.exists():
                     continue
                output_path.write_text(doc, encoding="utf-8")
                count += 1
            except Exception as e:
                print(f"[ContextReport] Failed to write {dir_path}: {e}")
            
        print(f"[ContextReport] Generated {count} _AI.md files.")
