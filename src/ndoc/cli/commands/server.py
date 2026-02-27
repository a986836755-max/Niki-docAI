"""
Command: LSP Server.
"""
import sys
from ndoc.core.cli import ndoc_command
from ndoc import lsp_server

@ndoc_command(name="server", help="Start LSP Server (stdio)", group="Core")
def run(stdio: bool = True) -> bool:
    """
    Start the LSP server.
    """
    sys.stderr.write("Starting Niki-docAI LSP Server...\n")
    # lsp_server.run usually blocks
    try:
        lsp_server.run()
    except KeyboardInterrupt:
        pass
    return True
