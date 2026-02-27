"""
Command: Typecheck.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig
from ndoc.flows import quality_flow

@ndoc_command(name="typecheck", help="Run typecheck commands defined in _RULES.md", group="Diagnostics")
def run(config: ProjectConfig) -> bool:
    """Run typecheck commands."""
    return quality_flow.run_typecheck(config)
