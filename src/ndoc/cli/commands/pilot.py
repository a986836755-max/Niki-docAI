"""
Command: Pilot (Legacy Alias).
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig
from . import all as all_cmd

@ndoc_command(name="pilot", help="Alias for 'ndoc all'", group="Core")
def run(config: ProjectConfig) -> bool:
    """
    Legacy alias for ECS Pipeline.
    """
    print("Redirecting 'pilot' to 'all' (ECS Pipeline)...")
    return all_cmd.run(config)
