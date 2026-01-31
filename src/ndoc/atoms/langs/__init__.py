"""
Language Definition Protocol.
语言定义协议。
"""
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Type

class LanguageDefinition:
    """
    Base class for language definitions.
    """
    ID: str = ""
    EXTENSIONS: List[str] = []
    SCM_QUERY: str = ""
    CALL_QUERY: str = ""
    SCM_IMPORTS: str = ""
    CLASS_TYPES: List[str] = []  # AST node types that define a class/struct/interface
    ASYNC_KEYWORDS: List[str] = ["async"] # Keywords that indicate an async function

    @staticmethod
    def get_visibility(captures: Dict[str, Any], content_bytes: bytes) -> str:
        if 'visibility' in captures:
            v_node = captures['visibility'][0] if isinstance(captures['visibility'], list) else captures['visibility']
            return content_bytes[v_node.start_byte:v_node.end_byte].decode('utf8', 'ignore').strip()
        return "public"

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        """
        Default visibility logic.
        """
        return True

    @classmethod
    def is_async(cls, node_text: str) -> bool:
        """
        Check if the code text starts with an async keyword.
        """
        for kw in cls.ASYNC_KEYWORDS:
            if node_text.startswith(kw + " "):
                return True
        return False

    @staticmethod
    def extract_docstring(node: Any, content_bytes: bytes) -> Optional[str]:
        """
        Extract docstring from node. Improved implementation with multi-line merging.
        """
        from tree_sitter import Node
        if not isinstance(node, Node):
            return None

        scan_node = node
        # Handle export/declaration wrappers (JS/TS)
        if node.parent and node.parent.type in ('export_statement', 'lexical_declaration', 'variable_declaration'):
            scan_node = node.parent
            if scan_node.parent and scan_node.parent.type == 'export_statement':
                scan_node = scan_node.parent

        curr = scan_node.prev_sibling
        while curr and curr.type in ('\n', ' ', ';'):
            curr = curr.prev_sibling

        comment_nodes = []
        while curr and curr.type in ('comment', 'line_comment', 'block_comment'):
            comment_nodes.insert(0, curr)
            
            # Look for previous sibling, but don't jump too far (max 1-2 lines)
            prev = curr.prev_sibling
            gap_lines = 0
            while prev and prev.type in ('\n', ' '):
                if prev.type == '\n':
                    gap_lines += 1
                prev = prev.prev_sibling
            
            if prev and prev.type in ('comment', 'line_comment', 'block_comment') and gap_lines <= 1:
                curr = prev
            else:
                break
        
        if not comment_nodes:
            return None

        # Process comment nodes
        from ..text_utils import clean_docstring
        full_raw = "\n".join([n.text.decode('utf8') for n in comment_nodes])
        return clean_docstring(full_raw)

    @staticmethod
    def format_signature(params_text: Optional[str], return_text: Optional[str]) -> str:
        """
        Format function signature. Default implementation is Generic.
        """
        sig = ""
        if params_text:
            sig = " ".join(params_text.split())
        if return_text:
            sig += f" -> {return_text}"
        return sig

# Global Registry
_LANG_REGISTRY: Dict[str, Type[LanguageDefinition]] = {}
_EXT_TO_LANG: Dict[str, str] = {}

def register_language(lang_cls: Type[LanguageDefinition]):
    """Register a language definition."""
    if not lang_cls.ID:
        return
    _LANG_REGISTRY[lang_cls.ID] = lang_cls
    for ext in lang_cls.EXTENSIONS:
        _EXT_TO_LANG[ext] = lang_cls.ID

def load_languages():
    """Automatically discover and load language definitions from the current package."""
    # Clear existing
    _LANG_REGISTRY.clear()
    _EXT_TO_LANG.clear()
    
    # Iterate over modules in the current package
    package_path = str(Path(__file__).parent)
    for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
        if is_pkg or module_name == "__init__":
            continue
            
        # Import the module
        full_module_name = f"{__name__}.{module_name}"
        module = importlib.import_module(full_module_name)
        
        # Look for LanguageDefinition subclasses
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, LanguageDefinition) and 
                attr is not LanguageDefinition):
                register_language(attr)

def get_lang_def(lang_id: str) -> Optional[Type[LanguageDefinition]]:
    """Get language definition by ID."""
    if not _LANG_REGISTRY:
        load_languages()
    return _LANG_REGISTRY.get(lang_id)

def get_lang_id_by_ext(ext: str) -> Optional[str]:
    """Get language ID by file extension."""
    if not _EXT_TO_LANG:
        load_languages()
    return _EXT_TO_LANG.get(ext.lower())

def get_all_extensions() -> List[str]:
    """Get all supported extensions."""
    if not _EXT_TO_LANG:
        load_languages()
    return list(_EXT_TO_LANG.keys())
