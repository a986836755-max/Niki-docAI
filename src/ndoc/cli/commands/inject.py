"""
Command: Inject.
"""
from typing import Optional
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig
from ndoc.flows import inject_flow

@ndoc_command(name="inject", help="Inject context headers into source files", group="Granular")
def run(config: ProjectConfig, target: Optional[str] = None) -> bool:
    """
    Execute injection flow.
    """
    return inject_flow.run(config, target)
