"""
Command: Update.
"""
from ndoc.core.cli import ndoc_command
from ndoc.flows import update_flow

@ndoc_command(name="update", help="Self-update the tool (git pull)", group="Core")
def run() -> bool:
    """
    Execute self-update via git pull.
    """
    return update_flow.run()
