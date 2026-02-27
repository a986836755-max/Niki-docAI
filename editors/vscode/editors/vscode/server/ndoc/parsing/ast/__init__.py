"""
Atoms: AST Parsing (Tree-sitter Wrapper).
原子能力：AST 解析 (Tree-sitter 封装)。
"""
from .base import (
    get_language, get_parser, parse_code, query_tree, AstNode, get_lang_key
)
from .utils import (
    node_to_data, truncate, MAX_VALUE_LENGTH, MAX_CONTENT_LENGTH
)
from .discovery import (
    find_calls, find_imports
)
from .symbols import (
    extract_symbols
)

# Export for compatibility
__all__ = [
    'get_language', 'get_parser', 'parse_code', 'query_tree', 'AstNode', 'get_lang_key',
    'node_to_data', 'truncate', 'MAX_VALUE_LENGTH', 'MAX_CONTENT_LENGTH',
    'find_calls', 'find_imports', 'extract_symbols'
]
