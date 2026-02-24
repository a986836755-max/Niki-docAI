"""
LSP Server implementation using pygls.
基于 pygls 的 LSP 服务实现，作为 IDE 插件的后端引擎。
"""
import sys
import os
from pathlib import Path
from typing import Optional, List

from pygls.lsp.server import LanguageServer
from lsprotocol.types import (
    INITIALIZE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_HOVER,
    Hover,
    MarkupContent,
    MarkupKind,
    TextDocumentItem,
    HoverParams,
    DidSaveTextDocumentParams,
    InitializeResult,
    ServerCapabilities,
    Diagnostic,
    DiagnosticSeverity,
    Position,
    Range,
)

# 确保 src 目录在路径中
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 调试：打印路径
sys.stderr.write(f"LSP Server starting. sys.path: {sys.path}\n")

from ndoc.atoms import lsp, fs, scanner
from ndoc.models import config

class NDocLanguageServer(LanguageServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lsp_service: Optional[lsp.LSPService] = None
        self.root_path: Optional[Path] = None

server = NDocLanguageServer("ndoc-ai-server", "v0.1.0")

@server.feature(INITIALIZE)
def lsp_initialize(ls: NDocLanguageServer, params):
    """
    项目初始化：索引整个工作区。
    """
    sys.stderr.write("LSP Server: Handling initialize request...\n")
    sys.stderr.flush()
    
    # 兼容性处理
    if isinstance(params, dict):
        root_path = params.get('rootPath') or params.get('root_path')
        root_uri = params.get('rootUri') or params.get('root_uri')
    else:
        root_path = getattr(params, 'root_path', None) or getattr(params, 'rootPath', None)
        root_uri = getattr(params, 'root_uri', None) or getattr(params, 'rootUri', None)
    
    if not root_path and root_uri:
        if root_uri.startswith("file:///"):
            root_path = root_uri[8:].replace("/", os.sep)
        elif root_uri.startswith("file://"):
            root_path = root_uri[7:].replace("/", os.sep)
            
    ls.root_path = Path(root_path or os.getcwd())
    ls.lsp_service = lsp.get_service(ls.root_path)
    
    sys.stderr.write(f"LSP Server: Workspace root is {ls.root_path}\n")
    sys.stderr.flush()
    
    # 执行全量索引
    cfg = config.load_config(ls.root_path)
    ignore_patterns = cfg.get("ignore", [])
    files = list(fs.walk_files(ls.root_path, ignore_patterns))
    sys.stderr.write(f"LSP Server: Found {len(files)} files to index.\n")
    sys.stderr.flush()
    ls.lsp_service.index_project(files)
    
    sys.stderr.write(f"LSP Server: Indexing completed successfully.\n")
    sys.stderr.flush()
    
    return InitializeResult(
        capabilities=ServerCapabilities(
            hover_provider=True,
            text_document_sync=1, # Full sync for simplicity in initial version
        )
    )

def check_architecture(ls: NDocLanguageServer, doc_uri: str):
    """
    架构校验：检查目录是否包含 _AI.md，并报告诊断信息。
    """
    if not doc_uri.startswith("file:///"):
        return
    
    file_path = Path(doc_uri[8:].replace("/", os.sep))
    dir_path = file_path.parent
    ai_md_path = dir_path / "_AI.md"
    
    diagnostics = []
    if not ai_md_path.exists():
        # 如果不存在 _AI.md，在第一行显示一个警告
        diagnostics.append(Diagnostic(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=1)
            ),
            message=f"Missing architecture documentation: {ai_md_path.name} not found in {dir_path.name}. 请根据项目规范创建 _AI.md 以同步架构知识。",
            severity=DiagnosticSeverity.Information,
            source="NDoc Architecture Check"
        ))
    
    ls.publish_diagnostics(doc_uri, diagnostics)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: NDocLanguageServer, params):
    """
    当文件打开时，确保它是最新的索引，并运行架构校验。
    """
    doc_uri = params.text_document.uri
    if doc_uri.startswith("file:///"):
        file_path = Path(doc_uri[8:].replace("/", os.sep))
        sys.stderr.write(f"LSP Server: Opening file {file_path}\n")
        ls.lsp_service.index_project([file_path])
        # 运行架构校验
        check_architecture(ls, doc_uri)

@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls: NDocLanguageServer, params: DidSaveTextDocumentParams):
    """
    当文件保存时，重新索引该文件以更新语义，并运行架构校验。
    """
    doc_uri = params.text_document.uri
    if doc_uri.startswith("file:///"):
        file_path = Path(doc_uri[8:].replace("/", os.sep))
        sys.stderr.write(f"LSP Server: Re-indexing on save: {file_path}\n")
        sys.stderr.flush()
        # 增量更新索引
        ls.lsp_service.index_project([file_path])
        # 运行架构校验
        check_architecture(ls, doc_uri)

@server.feature(TEXT_DOCUMENT_HOVER)
def hover(ls: NDocLanguageServer, params: HoverParams):
    """
    悬停提示：展示增强后的 Docstring。
    """
    doc_uri = params.text_document.uri
    # 转换为本地路径
    if doc_uri.startswith("file:///"):
        # 处理 Windows 路径
        file_path = Path(doc_uri[8:].replace("/", os.sep))
    else:
        return None

    # 获取当前光标下的单词
    doc = ls.workspace.get_text_document(doc_uri)
    word = doc.word_at_position(params.position)
    
    if not word:
        return None

    # 从 LSP Service 查找符号
    symbols = ls.lsp_service.find_definitions(word)
    if not symbols:
        return None

    # 构造悬停内容
    contents = []
    for sym in symbols:
        header = f"**{sym.kind.upper()}**: `{sym.name}`"
        if sym.docstring:
            # 使用 Markdown 格式展示增强版 Docstring
            content = f"{header}\n\n---\n\n{sym.docstring}"
        else:
            content = header
        
        # 添加引用计数信息（热度）
        ref_count = ls.lsp_service.get_reference_count(sym.name)
        content += f"\n\n---\n*🔥 Usage Intensity (Ref Count): {ref_count}*"
        
        contents.append(content)

    return Hover(
        contents=MarkupContent(
            kind=MarkupKind.Markdown,
            value="\n\n".join(contents)
        )
    )

def main():
    sys.stderr.write("LSP Server: Inside main()\n")
    sys.stderr.flush()
    # 显式使用 stdio 传输
    server.start_io()

if __name__ == "__main__":
    sys.stderr.write("LSP Server: Running via main block\n")
    sys.stderr.flush()
    main()
