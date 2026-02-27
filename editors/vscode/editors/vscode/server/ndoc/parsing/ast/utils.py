"""
Atoms: AST Parsing Utilities.
辅助工具函数。
"""
from typing import Optional
from tree_sitter import Node
from .base import AstNode, query_tree
from .. import langs

MAX_VALUE_LENGTH = 60
MAX_CONTENT_LENGTH = 200

def truncate(text: str, max_len: int = 100) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."

def node_to_data(node: Node, include_children: bool = False) -> AstNode:
    data = AstNode(
        type=node.type,
        text=node.text.decode("utf8"),
        start_point=node.start_point,
        end_point=node.end_point
    )
    if include_children:
        data.children = [node_to_data(child, True) for child in node.children]
    return data

def _get_parent_name(node: Node, lang_key: str = 'python') -> Optional[str]:
    lang_def = langs.get_lang_def(lang_key)
    if not lang_def:
        return None
        
    target_types = lang_def.CLASS_TYPES
    if not target_types:
        return None
        
    curr = node.parent
    while curr:
        if curr.type in target_types:
            name_node = curr.child_by_field_name('name')
            if name_node:
                return name_node.text.decode('utf8')
        curr = curr.parent
    return None

def _is_inside_function(node: Node) -> bool:
    curr = node.parent
    while curr:
        if curr.type in ('function_definition', 'async_function_definition', 'method_definition'):
            return True
        curr = curr.parent
    return False

def _extract_docstring_from_node(node: Node, content_bytes: bytes, lang_key: str = 'python') -> Optional[str]:
    lang_def = langs.get_lang_def(lang_key)
    if not lang_def:
        return None
    return lang_def.extract_docstring(node, content_bytes)

def _is_async_function(node: Node, lang_key: str = 'python') -> bool:
    lang_def = langs.get_lang_def(lang_key)
    if not lang_def:
        return False
    try:
        text = node.text.decode('utf8').strip()
        return lang_def.is_async(text)
    except:
        return False
