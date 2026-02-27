"""
Command: Verify.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig
from ndoc.flows import verify_flow

@ndoc_command(name="verify", help="Verify documentation artifacts", group="Diagnostics")
def run(config: ProjectConfig) -> bool:
    """
    Execute Verification.
    """
    return verify_flow.run(config)
