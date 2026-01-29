"""
Atoms: AST Parsing (Tree-sitter Wrapper).
原子能力：AST 解析 (Tree-sitter 封装)。
"""
from typing import List, Optional, Dict, Any, Iterator
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tree_sitter_python as tspython
except ImportError:
    tspython = None

try:
    import tree_sitter_cpp as tscpp
except ImportError:
    tscpp = None

try:
    import tree_sitter_javascript as tsjs
except ImportError:
    tsjs = None
    
try:
    import tree_sitter_typescript as tsts
except ImportError:
    tsts = None

try:
    import tree_sitter_go as tsgo
except ImportError:
    tsgo = None

try:
    import tree_sitter_rust as tsrust
except ImportError:
    tsrust = None

try:
    import tree_sitter_dart as tsdart
except ImportError:
    tsdart = None

from tree_sitter import Language, Parser, Tree, Node

from ..models.context import Symbol
from . import queries

# --- Configuration ---
# Map extension to language key
EXT_MAP = {
    '.py': 'python',
    '.cpp': 'cpp',
    '.c': 'cpp',
    '.h': 'cpp',
    '.hpp': 'cpp',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.go': 'go',
    '.rs': 'rust',
    '.dart': 'dart'
}

# Cache languages
_LANGUAGES = {}

def get_language(lang_key: str) -> Optional[Language]:
    if lang_key in _LANGUAGES:
        return _LANGUAGES[lang_key]
    
    lang_obj = None
    if lang_key == 'python' and tspython:
        lang_obj = Language(tspython.language())
    elif lang_key == 'cpp' and tscpp:
        lang_obj = Language(tscpp.language())
    elif lang_key == 'javascript' and tsjs:
        lang_obj = Language(tsjs.language())
    elif lang_key == 'typescript' and tsts:
        # TypeScript has two dialects: typescript and tsx
        # For simplicity, load standard typescript
        lang_obj = Language(tsts.language_typescript())
    elif lang_key == 'go' and tsgo:
        lang_obj = Language(tsgo.language())
    elif lang_key == 'rust' and tsrust:
        lang_obj = Language(tsrust.language())
    elif lang_key == 'dart' and tsdart:
        lang_obj = Language(tsdart.language())
        
    if lang_obj:
        _LANGUAGES[lang_key] = lang_obj
        
    return lang_obj

# --- Data Structures (Logic as Data) ---

@dataclass
class AstNode:
    """
    通用 AST 节点数据结构 (Generic AST Node Data).
    简化了 Tree-sitter 的 Node，便于序列化和传递。
    """
    type: str
    text: str
    start_point: tuple[int, int]  # (row, col)
    end_point: tuple[int, int]
    children: List['AstNode'] = field(default_factory=list)

    @property
    def start_line(self) -> int:
        return self.start_point[0] + 1

    @property
    def end_line(self) -> int:
        return self.end_point[0] + 1

# --- Engine (Pure Functions) ---

def get_parser(lang_key: str = 'python') -> Optional[Parser]:
    """
    获取解析器实例 (Get Parser Instance).
    """
    lang = get_language(lang_key)
    if not lang:
        return None
        
    parser = Parser(lang)
    return parser

def parse_code(content: str, file_path: Optional[Path] = None) -> Optional[Tree]:
    """
    解析代码生成 CST (Parse code to CST).
    
    Args:
        content: 源代码字符串
        file_path: 文件路径，用于推断语言
        
    Returns:
        Tree: Tree-sitter Tree 对象
    """
    lang_key = None
    if file_path:
        ext = file_path.suffix.lower()
        lang_key = EXT_MAP.get(ext)
    else:
        lang_key = 'python' # Default only if no file_path provided (e.g. testing)
        
    if not lang_key:
        return None

    parser = get_parser(lang_key)
    if not parser:
        return None
        
    # Tree-sitter expects bytes, encoding handled here
    return parser.parse(bytes(content, "utf8"))

def query_tree(tree: Tree, query_scm: str, lang_key: str = 'python') -> List[Dict[str, Node]]:
    """
    使用 S-expression 查询树 (Query Tree using S-expressions).
    Implementation: Query as Data.
    """
    lang = get_language(lang_key)
    if not lang:
        return []
        
    query = lang.query(query_scm)
    captures = query.captures(tree.root_node)
    return [{'name': name, 'node': node} for node, name in captures]


def node_to_data(node: Node, include_children: bool = False) -> AstNode:
    """
    将 Tree-sitter Node 转换为纯数据对象 (Convert Node to Data).
    """
    data = AstNode(
        type=node.type,
        text=node.text.decode("utf8"),
        start_point=node.start_point,
        end_point=node.end_point
    )
    if include_children:
        data.children = [node_to_data(child, True) for child in node.children]
    return data

# --- Helpers ---

def _get_parent_name(node: Node, lang_key: str = 'python') -> Optional[str]:
    """
    获取父级类名 (Get parent class name).
    Walks up the tree to find enclosing class_definition.
    """
    curr = node.parent
    
    # Language specific class node types
    class_types = {
        'python': ['class_definition'],
        'cpp': ['class_specifier', 'struct_specifier'],
        'javascript': ['class_declaration'],
        'typescript': ['class_declaration', 'interface_declaration'],
        'go': ['type_declaration', 'type_spec'], # Go is tricky, usually type X struct
        'rust': ['struct_item', 'trait_item', 'impl_item']
    }
    
    target_types = class_types.get(lang_key, ['class_definition'])
    
    while curr:
        if curr.type in target_types:
            # Find name node
            name_node = curr.child_by_field_name('name')
            
            # Special handling for Go type specs
            if lang_key == 'go' and curr.type == 'type_declaration':
                 # Go: type Name struct { ... }
                 # type_declaration -> type_spec -> name
                 # We might be inside type_spec already if using query
                 pass
            
            if name_node:
                return name_node.text.decode('utf8')
                
            # Fallback for some languages where name might be different
            # e.g. C++ class_specifier -> name is type_identifier
        curr = curr.parent
    return None

def _extract_docstring_from_node(node: Node, content_bytes: bytes) -> Optional[str]:
    """
    从节点中提取 Docstring (Extract docstring from node).
    """
    # Look for block -> expression_statement -> string
    block = node.child_by_field_name('body')
    if not block:
        return None
        
    for child in block.children:
        if child.type == 'expression_statement':
            # Check if it contains a string
            if child.child_count > 0 and child.children[0].type == 'string':
                string_node = child.children[0]
                # Remove quotes
                raw = string_node.text.decode('utf8')
                if raw.startswith('"""') or raw.startswith("'''"):
                    return raw[3:-3]
                elif raw.startswith('"') or raw.startswith("'"):
                    return raw[1:-1]
    return None

def _is_async_function(node: Node, lang_key: str = 'python') -> bool:
    """
    Check if function definition is async.
    """
    try:
        text = node.text.decode('utf8').strip()
        if lang_key in ('python', 'javascript', 'typescript'):
            return text.startswith('async ')
        # C++/Go/Rust usually handle async differently (e.g. library based or keywords)
        # Rust has async fn
        if lang_key == 'rust':
            return text.startswith('async ')
        return False
    except:
        return False

# --- High-Level Extraction (Business Logic) ---

def extract_symbols(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]:
    """
    提取所有顶级符号 (Extract all top-level symbols).
    Implementation: Query Pipeline.
    """
    # Determine language
    lang_key = 'python'
    if file_path:
        ext = file_path.suffix.lower()
        lang_key = EXT_MAP.get(ext, 'python')
        
    # Get Language Object
    lang_obj = get_language(lang_key)
    if not lang_obj:
        return []
        
    # Get Query SCM
    query_scm = queries.QUERY_MAP.get(lang_key)
    if not query_scm:
        # If no query for this language, return empty
        return []
    
    query = lang_obj.query(query_scm)
    matches = query.matches(tree.root_node)
    
    unique_symbols = {} # Map[start_byte, Symbol]
    
    for match in matches:
        captures = match[1]
        
        node = None
        kind = "unknown"
        name = ""
        signature = ""
        decorators = []
        parent_name = None
        docstring = None

        # Collect decorators first
        if 'deco' in captures:
            deco_nodes = captures['deco']
            if not isinstance(deco_nodes, list):
                deco_nodes = [deco_nodes]
            for deco in deco_nodes:
                decorators.append(deco.text.decode('utf8').strip())

        # 1. Handle Class Definitions
        if 'class_def' in captures:
            node = captures['class_def'][0] if isinstance(captures['class_def'], list) else captures['class_def']
            kind = 'class'
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
            parent_name = _get_parent_name(node, lang_key)

        # 2. Handle Function Definitions
        elif 'func_def' in captures:
            node = captures['func_def'][0] if isinstance(captures['func_def'], list) else captures['func_def']
            kind = 'function'
            
            # Check async
            if _is_async_function(node, lang_key):
                kind = 'async_function'
            
            # Check decorators for kind override (Python specific mostly)
            for deco_text in decorators:
                if '@property' in deco_text:
                    kind = 'property'
                elif '@classmethod' in deco_text:
                    kind = 'classmethod'
                elif '@staticmethod' in deco_text:
                    kind = 'staticmethod'
            
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
                
            # Signature extraction
            params_node = None
            ret_node = None
            
            if 'params' in captures:
                params_node = captures['params'][0] if isinstance(captures['params'], list) else captures['params']
            if 'ret' in captures:
                ret_node = captures['ret'][0] if isinstance(captures['ret'], list) else captures['ret']
                
            if params_node:
                p_text = params_node.text.decode('utf8')
                p_text = " ".join(p_text.split()) # Clean newlines
                signature = p_text
            
            if ret_node:
                r_text = ret_node.text.decode('utf8')
                signature += f" -> {r_text}"
            
            # Go specific: func (r Receiver) Name()
            # We might need better query to capture receiver as parent, but for now logic is simple
            
            parent_name = _get_parent_name(node, lang_key)

        # 3. Handle Field/Variable Definitions
        elif 'field_def' in captures:
            node = captures['field_def'][0] if isinstance(captures['field_def'], list) else captures['field_def']
            kind = 'variable'
            
            if 'field_name' in captures:
                name = captures['field_name'][0].text.decode('utf8')
            
            # Signature for fields: type = value
            type_text = ""
            value_text = ""
            
            if 'field_type' in captures:
                type_node = captures['field_type'][0] if isinstance(captures['field_type'], list) else captures['field_type']
                type_text = type_node.text.decode('utf8')
            
            if 'field_value' in captures:
                val_node = captures['field_value'][0] if isinstance(captures['field_value'], list) else captures['field_value']
                value_text = val_node.text.decode('utf8')
            
            if type_text and value_text:
                signature = f": {type_text} = {value_text}"
            elif type_text:
                signature = f": {type_text}"
            elif value_text:
                signature = f" = {value_text}"
                
            parent_name = _get_parent_name(node, lang_key)

        if node and name:
            # Extract docstring if not already done (for classes/functions)
            if kind in ('class', 'function', 'async_function', 'method', 'classmethod', 'staticmethod', 'property'):
                docstring = _extract_docstring_from_node(node, content_bytes)
            
            # Determine effective kind (method vs function)
            if parent_name and kind == 'function':
                kind = 'method'
            if parent_name and kind == 'async_function':
                kind = 'async_method'

            # Prevent recursion/collision for constructors or same-named methods
            # If a method has the same name as its parent (common in C++ constructors),
            # append '()' to the name to distinguish it in the hierarchy map.
            if parent_name and name == parent_name and kind in ('function', 'method', 'async_function', 'async_method'):
                name = f"{name}()"

            sym = Symbol(
                name=name,
                kind=kind,
                line=node.start_point[0] + 1,
                docstring=docstring,
                signature=signature if signature else None,
                parent=parent_name
            )
            
            # De-duplication logic
            node_id = node.start_byte
            if node_id in unique_symbols:
                existing = unique_symbols[node_id]
                # Priority: property/classmethod > function/method
                if existing.kind in ('function', 'method') and sym.kind in ('property', 'classmethod', 'staticmethod'):
                    unique_symbols[node_id] = sym
                elif sym.signature and not existing.signature:
                    unique_symbols[node_id] = sym
            else:
                unique_symbols[node_id] = sym
                
    # Sort by line number
    symbols = sorted(unique_symbols.values(), key=lambda s: s.line)
    return symbols
