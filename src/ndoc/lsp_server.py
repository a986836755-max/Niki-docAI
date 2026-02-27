"""
LSP Server implementation using pygls.
Provides Niki-docAI capabilities to IDEs.
"""
import sys
import os
import logging
from typing import Optional, List
from pathlib import Path
from urllib.parse import urlparse, unquote
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
from ndoc.core import fs
from ndoc.flows import config_flow

server = LanguageServer("ndoc-lsp", "0.1.0")

# Cache for LSPService instances per root
_services = {}

def get_service(root_path: str) -> Optional[LSPService]:
    if root_path not in _services:
        logging.info(f"Initializing service for root: {root_path}")
        svc = LSPService(root_path)
        _services[root_path] = svc
    return _services[root_path]

def _uri_to_path(uri: str) -> Path:
    parsed = urlparse(uri)
    if parsed.scheme != "file":
        return Path(uri)
    path = unquote(parsed.path)
    if os.name == "nt" and path.startswith("/") and len(path) > 2 and path[2] == ":":
        path = path[1:]
    return Path(path)

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
            line_no = max(0, (v.line - 1)) if v.line else 0
            char_no = max(0, v.character) if v.character else 0
            diag = Diagnostic(
                range=Range(
                    start=Position(line=line_no, character=char_no),
                    end=Position(line=line_no, character=char_no + 100)
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

    md_sections: List[str] = [f"**Niki-docAI Hover**", f"**Symbol**: `{word}`"]

    try:
        svc = get_service(root)
        context = svc.get_context_for_file(Path(document.path))
        if context:
            md_sections.append("### Rules")
            md_sections.append(context)
    except Exception as e:
        logging.error(f"Hover context failed: {e}")

    try:
        from ndoc.brain.vectordb import VectorDB
        vdb = VectorDB(Path(root))
        results = vdb.query(f"{word} concept definition", n_results=2)
        if results:
            md_sections.append("### Vector")
            for res in results:
                meta = res.get('metadata', {})
                src = meta.get('source', 'unknown')
                doc = res.get('document', '')
                if len(doc) > 200:
                    doc = doc[:200] + "..."
                md_sections.append(f"**{src}**")
                md_sections.append(doc)
        else:
            md_sections.append("### Vector")
            md_sections.append("_no results_")
    except Exception as e:
        logging.error(f"Hover vector search failed: {e}")

    return Hover(contents=MarkupContent(kind=MarkupKind.Markdown, value="\n\n".join(md_sections)))

@server.feature(TEXT_DOCUMENT_CODE_LENS)
def code_lens(ls: LanguageServer, params: CodeLensParams):
    uri = params.text_document.uri
    # Create CodeLens for showing context
    # Command arguments must be JSON serializable
    # VS Code commands expect URI as string or Uri object
    
    return [
        CodeLens(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=0)),
            command=Command(
                title="Niki: Show Thinking Context",
                command="ndoc.showContext",
                arguments=[uri]
            )
        )
    ]

def main():
    # Use standard IO (stdin/stdout) for LSP communication
    # Ensure stdout is binary to avoid encoding issues on Windows?
    # pygls handles this internally, but we must ensure no print() calls corrupt stdout.
    # We already configured logging to stderr.
    
    # Force stdin/stdout to binary mode on Windows if needed
    if sys.platform == "win32":
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        
    server.start_io()

run = main

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    """
    When a file is opened, ensure service is initialized and validate.
    """
    uri = params.text_document.uri
    logging.info(f"File opened: {uri}")
    validate_document(ls, uri)

@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls: LanguageServer, params: DidSaveTextDocumentParams):
    """
    When file is saved, re-validate.
    """
    uri = params.text_document.uri
    logging.info(f"File saved: {uri}")
    validate_document(ls, uri)

if __name__ == "__main__":
    main()
