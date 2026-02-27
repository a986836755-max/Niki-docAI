"""
Command: Lint.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig
from ndoc.flows import quality_flow

@ndoc_command(name="lint", help="Run lint commands defined in _RULES.md", group="Diagnostics")
def run(config: ProjectConfig) -> bool:
    """Run lint commands."""
    return quality_flow.run_lint(config)
