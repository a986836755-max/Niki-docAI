"""
Core Kernel Context (ECS World).
Acts as the central registry for Entities and Components.
"""
from typing import Dict, Type, List, Optional, Any
from collections import defaultdict
import pluggy
from ndoc.sdk.models import Entity, Component
from ndoc.sdk import interfaces

class KernelContext:
    def __init__(self):
        # ECS Storage
        # entity_id -> Entity
        self.entities: Dict[str, Entity] = {}
        
        # component_type -> entity_id -> Component
        self.components: Dict[Type[Component], Dict[str, Component]] = defaultdict(dict)
        
        # Plugin Manager
        self.pm = pluggy.PluginManager("ndoc")
        # Register hook specs individually from the classes or functions, 
        # NOT the module if the module just contains classes with methods.
        # Pluggy expects a class or module that HAS the hookspecs as methods/functions.
        # In our interfaces.py, hookspecs are methods of SensorPlugin/ActionPlugin classes.
        # So we should add_hookspecs(SensorPlugin) and add_hookspecs(ActionPlugin).
        self.pm.add_hookspecs(interfaces.SensorPlugin)
        self.pm.add_hookspecs(interfaces.ActionPlugin)

    def register_plugin(self, plugin: Any):
        """Register a new plugin instance."""
        self.pm.register(plugin)

    def add_entity(self, entity: Entity):
        """Register an entity in the world."""
        self.entities[entity.id] = entity

    def add_component(self, entity_id: str, component: Component):
        """Attach a component to an entity."""
        if entity_id not in self.entities:
            raise ValueError(f"Entity {entity_id} does not exist.")
        
        comp_type = type(component)
        self.components[comp_type][entity_id] = component

    def get_component(self, entity_id: str, comp_type: Type[Component]) -> Optional[Component]:
        """Get component for entity."""
        return self.components[comp_type].get(entity_id)

    def query(self, *comp_types: Type[Component]) -> List[str]:
        """
        Simple Query System.
        Returns list of entity_ids that have ALL specified components.
        """
        if not comp_types:
            return list(self.entities.keys())
            
        # Get sets of entity IDs for each component type
        sets = [set(self.components[t].keys()) for t in comp_types]
        
        # Intersect
        result = set.intersection(*sets)
        return list(result)

    def process_all_hooks(self):
        """
        Manually trigger lifecycle hooks in order.
        (In a real app, this might be event-driven or pipeline based)
        """
        # 1. Collect Entities (Already done via manual call in Pilot, but hook exists)
        # 2. Process Syntax (Already done via manual call in Pilot)
        
        # 3. Process Dependencies (Global)
        self.pm.hook.ndoc_process_dependencies(context=self)
        
        # 4. Generate Docs (Action)
        print("[Kernel] Triggering ndoc_generate_docs hook...")
        self.pm.hook.ndoc_generate_docs(context=self)
