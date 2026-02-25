# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Proactive Capability Check**: `entry.py` serves as the primary gatekeeper. It must invoke `capability_flow` to ...
# *   **Dynamic Watchdog**: `daemon.py` monitors file system events. When a new file type is detected (e.g., a `.rs` fi...
# *   **CLI Robustness**: All CLI commands (including `lsp`) must handle missing capabilities gracefully, either by att...
# *   **LSP Protocol Integrity**: `entry.py`'s `server` command MUST NOT print anything to `stdout` other than JSON-RPC...
# *   **Context Awareness**: `lsp_server.py` implements "Thinking Context" via `textDocument/hover`, aggregating rules ...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
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
    TEXT_DOCUMENT_CODE_LENS,
    TEXT_DOCUMENT_DID_SAVE,
    WORKSPACE_EXECUTE_COMMAND,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    HoverParams,
    Hover,
    MarkupContent,
    MarkupKind,
    ExecuteCommandParams,
    CodeLensParams,
    CodeLens,
    Command,
    Range,
    Position,
    Diagnostic,
    DiagnosticSeverity,
    PublishDiagnosticsParams
)

# Setup basic logging to stderr so it shows up in VS Code Output
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='[Niki-LSP] %(message)s')

# Adjust path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ndoc.interfaces.lsp import LSPService
from ndoc.brain import checker, index
from ndoc.parsing import scanner
from ndoc.models.context import FileContext

server = LanguageServer("ndoc-lsp", "0.1.0")

# Cache for LSPService instances per root
_services = {}

def get_service(root_path: str) -> Optional[LSPService]:
    if root_path not in _services:
        logging.info(f"Initializing service for root: {root_path}")
        svc = LSPService(root_path)
        _services[root_path] = svc
    return _services[root_path]

def validate_document(ls: LanguageServer, uri: str):
    """
    Run ndoc checker on the document and publish diagnostics.
    """
    try:
        document = ls.workspace.get_text_document(uri)
        path = Path(document.path)
        
        # Determine root
        root = ls.workspace.root_path
        if not root:
            root = str(path.parent)
        root_path = Path(root)
            
        # 1. Scan the file
        # Note: We should scan content from memory (document.source) to be real-time
        # But scanner currently reads from disk.
        # TODO: Refactor scanner to accept string content.
        # For now, we assume on_save so disk is fresh.
        scan_result = scanner.scan_file(path, root_path)
        
        # Convert to FileContext
        # We need a proper way to do this conversion, maybe expose the helper from check_flow?
        # Or just manually create it here.
        try:
            rel = str(path.relative_to(root_path))
        except ValueError:
            rel = str(path)
            
        file_ctx = FileContext(
            path=path,
            rel_path=rel,
            tags=scan_result.tags,
            sections=scan_result.sections,
            symbols=scan_result.symbols,
            docstring=scan_result.docstring,
            memories=scan_result.memories
        )
        
        # 2. Build Index (Lazy)
        # In a real LSP, we should cache the index.
        # For this prototype, we rebuild index from local _AI.md files nearby?
        # Or just use what we have.
        # Let's assume we scan all _AI.md files in root (heavy but correct)
        # Optimization: Use LSPService to cache the index.
        
        svc = get_service(root)
        if not svc.semantic_index:
            # First time load
            ai_files = list(root_path.rglob("_AI.md"))
            rule_contexts = []
            for f in ai_files:
                ctx = scanner.scan_file(f, root_path)
                if ctx:
                    # Convert to FileContext
                    try:
                        r = str(f.relative_to(root_path))
                    except: r = str(f)
                    
                    rule_contexts.append(FileContext(path=f, rel_path=r, tags=ctx.tags))
            
            svc.semantic_index = index.build_index(rule_contexts)
            logging.info(f"Built semantic index with {len(svc.semantic_index.rules)} rules")
            
        # 3. Check
        violations = checker.check_file(file_ctx, svc.semantic_index)
        
        # 4. Publish Diagnostics
        diagnostics = []
        for v in violations:
            # We need line number.
            # Checker currently doesn't return line number in Violation object?
            # Let's check checker.py... It returns Violation(file_path, rule_name, message, severity)
            # We need to enhance Checker to return line numbers.
            # For now, we put it at the top of file (Range 0,0 - 0,1)
            
            # Find the tag line if possible
            line_no = 0
            if "tag" in v.message:
                # Naive search for tag in file content
                # This is a hack until Checker returns line numbers
                tag_name = v.message.split("'")[3] # Extract '@tag' from message
                for i, line in enumerate(document.lines):
                    if tag_name in line:
                        line_no = i
                        break
            
            diag = Diagnostic(
                range=Range(
                    start=Position(line=line_no, character=0),
                    end=Position(line=line_no, character=100)
                ),
                message=f"{v.message} ({v.rule_name})",
                severity=DiagnosticSeverity.Error if v.severity == "ERROR" else DiagnosticSeverity.Warning,
                source="ndoc"
            )
            diagnostics.append(diag)
            
        ls.publish_diagnostics(uri, diagnostics)
        
    except Exception as e:
        logging.error(f"Validation failed: {e}")

@server.feature(TEXT_DOCUMENT_HOVER)
def hover(ls: LanguageServer, params: HoverParams):
    """
    Semantic Hover: Show relevant rules or vector search results for the symbol under cursor.
    """
    uri = params.text_document.uri
    document = ls.workspace.get_text_document(uri)
    pos = params.position
    
    # 1. Extract word under cursor (Naive implementation)
    line = document.lines[pos.line]
    word = ""
    # Simple word extraction
    start = pos.character
    end = pos.character
    while start > 0 and (line[start-1].isalnum() or line[start-1] == '_'):
        start -= 1
    while end < len(line) and (line[end].isalnum() or line[end] == '_'):
        end += 1
    word = line[start:end]
    
    if not word:
        return None
        
    # 2. Vector Search for Concept
    root = ls.workspace.root_path
    if not root:
        root = str(Path(document.path).parent)
    
    try:
        from ndoc.brain.vectordb import VectorDB
        vdb = VectorDB(Path(root))
        results = vdb.query(f"{word} concept definition", n_results=2)
        
        if results:
            md_content = [f"**Niki-docAI Context for `{word}`**"]
            for res in results:
                meta = res.get('metadata', {})
                src = meta.get('source', 'unknown')
                doc = res.get('document', '')
                # Truncate doc if too long
                if len(doc) > 200:
                    doc = doc[:200] + "..."
                md_content.append(f"---")
                md_content.append(f"**From `{src}`**:\n{doc}")
                
            return Hover(contents=MarkupContent(kind=MarkupKind.Markdown, value="\n\n".join(md_content)))
    except Exception as e:
        logging.error(f"Hover vector search failed: {e}")
        pass
        
    return None

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    """
    When a file is opened, ensure service is initialized and validate.
    """
    uri = params.text_document.uri
    document = ls.workspace.get_text_document(uri)
    path = Path(document.path)
    logging.info(f"File opened: {path}")
    
    validate_document(ls, uri)

@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls: LanguageServer, params: DidSaveTextDocumentParams):
    """
    Validate on save.
    """
    validate_document(ls, params.text_document.uri)

if __name__ == '__main__':
    server.start_io()

def run():
    server.start_io()

if __name__ == "__main__":
    run()
