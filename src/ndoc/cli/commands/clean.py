"""
Command: Clean.
"""
from typing import Optional
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig
from ndoc.flows import clean_flow

@ndoc_command(name="clean", help="Clean/Reset generated documentation artifacts", group="Core")
def run(config: ProjectConfig, target: Optional[str] = None, force: bool = False) -> bool:
    """
    Execute Clean Flow.
    """
    return clean_flow.run(config, target, force)
