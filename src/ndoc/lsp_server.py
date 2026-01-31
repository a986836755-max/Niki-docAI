"""
LSP Server implementation using pygls.
基于 pygls 的 LSP 服务实现，作为 IDE 插件的后端引擎。
"""
import sys
import os
from pathlib import Path
from typing import Optional, List

from pygls.server import LanguageServer
from lsprotocol.types import (
    INITIALIZE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_HOVER,
    Hover,
    MarkupContent,
    MarkupKind,
    TextDocumentItem,
    HoverParams,
)

# 确保 src 目录在路径中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    ls.root_path = Path(params.root_path or os.getcwd())
    ls.lsp_service = lsp.get_service(ls.root_path)
    
    # 记录日志到标准错误，以免干扰标准输出的 RPC 通信
    sys.stderr.write(f"LSP Server: Initializing at {ls.root_path}\n")
    
    # 加载配置以获取忽略模式
    cfg = config.load_config(ls.root_path)
    ignore_patterns = cfg.get("ignore", [])
    
    # 扫描并索引所有文件
    files = list(fs.walk_files(ls.root_path, ignore_patterns))
    sys.stderr.write(f"LSP Server: Found {len(files)} files to index\n")
    ls.lsp_service.index_project(files)
    
    sys.stderr.write(f"LSP Server: Indexing complete\n")

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: NDocLanguageServer, params):
    """
    当文件打开时，确保它是最新的索引。
    """
    # 可以在这里做单文件重扫描逻辑
    pass

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
    # 默认通过标准输入输出 (stdio) 通信
    server.start_io()

if __name__ == "__main__":
    main()
