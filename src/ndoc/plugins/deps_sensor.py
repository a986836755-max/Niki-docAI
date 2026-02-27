"""
Dependency Graph Sensor Plugin.
Responsible for building the dependency graph (GraphComponent) for entities.
"""
from pathlib import Path
from typing import Dict, Any, List
from ndoc.sdk.interfaces import SensorPlugin, hookimpl
from ndoc.sdk.models import Entity, GraphComponent
from ndoc.parsing.deps import builder 

class DependencySensorPlugin(SensorPlugin):
    """
    Scans files to extract import statements and builds a dependency graph.
    """
    
    def __init__(self):
        # We store raw import data in memory until we can resolve it
        self._raw_import_map: Dict[str, List[str]] = {}
        
    @hookimpl
    def ndoc_process_syntax(self, entity: Entity) -> Dict[str, Any]:
        """
        Step 1: Collect raw imports (just strings) for each entity.
        This is a 'local' operation.
        """
        # For simplicity in Pilot, we use builder.collect_imports BUT
        # ideally we should parse just this file content here.
        # Let's use builder.collect_imports ONCE for the whole project to populate cache,
        # then return the specific file's imports.
        
        # Check if we have cached the whole project scan
        if not self._raw_import_map:
            # Assume CWD is root for now (or find root)
            root = Path.cwd()
            try:
                self._raw_import_map = builder.collect_imports(root)
            except Exception:
                self._raw_import_map = {}
        
        # Get relative path key
        try:
            rel_path = entity.path.relative_to(Path.cwd()).as_posix()
        except ValueError:
            rel_path = entity.id

        imports = self._raw_import_map.get(rel_path, [])
        
        # We return this data so Kernel can attach it temporarily?
        # Actually, GraphComponent needs resolved IDs.
        # We can attach a temporary component or just store it in plugin state.
        # Let's store it in plugin state (self._raw_import_map) and process later.
        return {} 

    @hookimpl
    def ndoc_process_dependencies(self, context):
        """
        Step 2: Resolve raw imports to Entity IDs and create GraphComponent.
        This is a 'global' operation.
        """
        # 1. Build the graph using existing logic
        # builder.build_dependency_graph returns { 'file_a': {'file_b', 'file_c'} }
        # where keys and values are relative paths (which match our Entity IDs).
        
        resolved_graph = builder.build_dependency_graph(self._raw_import_map)
        
        # EXPOSE GRAPH FOR SERVICES
        context.graph = resolved_graph
        
        print(f"[DEBUG] DependencySensor: Resolved graph size: {len(resolved_graph)}")
        if resolved_graph:
            print(f"[DEBUG] DependencySensor: Sample node: {list(resolved_graph.keys())[0]}")
            print(f"[DEBUG] DependencySensor: Sample entities: {list(context.entities.keys())[:3]}")
        
        # 2. Update Entities with GraphComponent
        count = 0
        for source_id, target_ids in resolved_graph.items():
            # Check if source entity exists
            if source_id in context.entities:
                # Filter targets to ensure they exist as entities
                valid_targets = [tid for tid in target_ids if tid in context.entities]
                
                # Create Component
                comp = GraphComponent(imports=valid_targets)
                context.add_component(source_id, comp)
                
                # Also update 'imported_by' for targets
                for target_id in valid_targets:
                    target_comp = context.get_component(target_id, GraphComponent)
                    if not target_comp:
                        target_comp = GraphComponent()
                        context.add_component(target_id, target_comp)
                    target_comp.imported_by.append(source_id)
                
                count += 1
                
        print(f"[DependencySensor] Built graph for {count} nodes.")
