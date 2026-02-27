"""
Plugin Interface Definitions (HookSpecs)
"""
import pluggy
from typing import List, Dict, Any
from .models import Entity

hookspec = pluggy.HookspecMarker("ndoc")
hookimpl = pluggy.HookimplMarker("ndoc")

class NdocPlugin:
    """
    Marker interface for all Ndoc plugins.
    """
    pass

class SensorPlugin(NdocPlugin):
    """
    Plugins that READ from the codebase.
    """
    @hookspec(firstresult=True)
    def ndoc_collect_entities(self, root_path: str) -> List[Entity]:
        """Collect entities (files) from the project root."""

    @hookspec(firstresult=False)
    def ndoc_process_syntax(self, entity: Entity) -> Dict[str, Any]:
        """Process syntax for an entity and return Component data."""

    @hookspec(firstresult=False)
    def ndoc_process_dependencies(self, context: Any):
        """
        Process cross-entity dependencies.
        This hook is called AFTER all entities have been collected.
        """

class ActionPlugin(NdocPlugin):
    """
    Plugins that WRITE or GENERATE content.
    """
    @hookspec(firstresult=False)
    def ndoc_generate_docs(self, context: Any):
        """Generate documentation based on current context."""
