"""
LSP Server implementation using pygls.
Provides Niki-docAI capabilities to IDEs.
"""
import sys
import os
import logging
from typing import Optional, List
from pathlib import Path
from pygls.lsp.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_HOVER,
    WORKSPACE_EXECUTE_COMMAND,
    DidOpenTextDocumentParams,
    HoverParams,
    Hover,
    MarkupContent,
    MarkupKind,
    ExecuteCommandParams
)

# Setup basic logging to stderr so it shows up in VS Code Output
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='[Niki-LSP] %(message)s')

# Adjust path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ndoc.atoms.lsp import LSPService

server = LanguageServer("ndoc-lsp", "0.1.0")

# Cache for LSPService instances per root
_services = {}

def get_service(root_path: str) -> Optional[LSPService]:
    if root_path not in _services:
        logging.info(f"Initializing service for root: {root_path}")
        # Try to find _MAP.md or similar to confirm it's an ndoc project
        # For now, just initialize blindly
        svc = LSPService(root_path)
        # We might want to trigger a lightweight index here?
        # svc.index_project(...) # This can be slow, maybe do it async or on demand
        _services[root_path] = svc
    return _services[root_path]

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    """
    When a file is opened, we might want to ensure we have context for it.
    """
    uri = params.text_document.uri
    path = Path(ls.workspace.get_text_document(uri).path)
    logging.info(f"File opened: {path}")
    
    # Pre-warm service
    try:
        get_service(str(path.parent))
    except Exception as e:
        logging.error(f"Error initializing service: {e}")

@server.feature(TEXT_DOCUMENT_HOVER)
def hover(ls: LanguageServer, params: HoverParams) -> Optional[Hover]:
    """
    Show 'Thinking Context' or Symbol Info on hover.
    """
    uri = params.text_document.uri
    document = ls.workspace.get_text_document(uri)
    path = Path(document.path)
    
    logging.info(f"Hover request at {path}:{params.position.line}")

    # Simplify logic: Try to get context for ANY line, to test connectivity
    try:
        # Find project root (naive)
        # Better: use ls.workspace.root_path if available
        root = ls.workspace.root_path
        if not root:
             root = str(path.parent) # Fallback
        
        svc = get_service(root)
        if svc:
            ctx = svc.get_context_for_file(path)
            if ctx:
                # If on first line, show full context
                if params.position.line == 0:
                     return Hover(
                         contents=MarkupContent(
                             kind=MarkupKind.Markdown,
                             value=f"### 🧠 Niki-docAI Context\n\n{ctx}"
                         )
                     )
                # For other lines, maybe show a small indicator if we have context?
                # Or just return nothing to avoid noise.
                # BUT for debugging, let's return something if the user asks for it
                # Maybe we can add a command to "Show Context" explicitly instead of Hover?
                # For now, let's keep the line 0 rule but log it.
            else:
                logging.info(f"No context found for {path}")
                if params.position.line == 0:
                     return Hover(
                         contents=MarkupContent(
                             kind=MarkupKind.Markdown,
                             value=f"### 🧠 Niki-docAI\n\nNo context found. Have you run `ndoc init` and `ndoc all`?"
                         )
                     )
    except Exception as e:
        logging.error(f"Hover error: {e}")
        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"### 🧠 Niki-docAI Error\n\n{str(e)}"
            )
        )
            
    return None

@server.feature(WORKSPACE_EXECUTE_COMMAND)
def execute_command(ls: LanguageServer, params: ExecuteCommandParams):
    if params.command == "ndoc.getThinkingContext":
        # ... existing logic ...
        pass

def run():
    server.start_io()

if __name__ == "__main__":
    run()
