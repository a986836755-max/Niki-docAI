"""
Atoms: AST Parsing (Tree-sitter Wrapper).
原子能力：AST 解析 (Tree-sitter 封装)。
"""
from typing import List, Optional, Dict, Any, Iterator, Type
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

try:
    import tree_sitter_c_sharp as tscsharp
except ImportError:
    tscsharp = None

try:
    import tree_sitter_java as tsjava
except ImportError:
    tsjava = None

from tree_sitter import Language, Parser, Tree, Node

from ..models.context import Symbol
from . import langs

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
        lang_obj = Language(tsts.language_typescript())
    elif lang_key == 'go' and tsgo:
        lang_obj = Language(tsgo.language())
    elif lang_key == 'rust' and tsrust:
        lang_obj = Language(tsrust.language())
    elif lang_key == 'dart' and tsdart:
        lang_obj = Language(tsdart.language())
    elif lang_key == 'c_sharp' and tscsharp:
        lang_obj = Language(tscsharp.language())
    elif lang_key == 'java' and tsjava:
        lang_obj = Language(tsjava.language())
    
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
        
    try:
        parser = Parser(lang)
        return parser
    except ValueError as e:
        print(f"❌ Error creating parser for {lang_key}: {e}")
        return None

def parse_code(content: str, file_path: Optional[Path] = None) -> Optional[Tree]:
    """
    解析代码生成 CST (Parse code to CST).
    """
    lang_key = None
    if file_path:
        ext = file_path.suffix.lower()
        lang_key = langs.get_lang_id_by_ext(ext)
    else:
        lang_key = 'python'
        
    if not lang_key:
        return None

    parser = get_parser(lang_key)
    if not parser:
        return None
        
    return parser.parse(bytes(content, "utf8"))

def query_tree(tree: Tree, query_scm: str, lang_key: str = 'python') -> List[Dict[str, Node]]:
    """
    使用 S-expression 查询树 (Query Tree using S-expressions).
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
    """
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


def _extract_docstring_from_node(node: Node, content_bytes: bytes, lang_key: str = 'python') -> Optional[str]:
    """
    从节点中提取 Docstring (Extract docstring from node).
    """
    lang_def = langs.get_lang_def(lang_key)
    if not lang_def:
        return None
    return lang_def.extract_docstring(node, content_bytes)

def _is_async_function(node: Node, lang_key: str = 'python') -> bool:
    """
    Check if function definition is async.
    """
    lang_def = langs.get_lang_def(lang_key)
    if not lang_def:
        return False
        
    try:
        text = node.text.decode('utf8').strip()
        return lang_def.is_async(text)
    except:
        return False

# --- High-Level Extraction (Business Logic) ---

def _is_inside_function(node: Node) -> bool:
    """
    检查节点是否在函数内部 (Check if node is inside a function).
    """
    curr = node.parent
    while curr:
        if curr.type in ('function_definition', 'async_function_definition', 'method_definition'):
            return True
        curr = curr.parent
    return False


def extract_symbols(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]:
    """
    提取所有顶级符号 (Extract all top-level symbols).
    """
    lang_key = 'python'
    if file_path:
        ext = file_path.suffix.lower()
        lang_key = langs.get_lang_id_by_ext(ext) or 'python'
        
    lang_obj = get_language(lang_key)
    if not lang_obj:
        return []
        
    lang_def = langs.get_lang_def(lang_key)
    if not lang_def or not lang_def.SCM_QUERY:
        return []
    
    query = lang_obj.query(lang_def.SCM_QUERY)
    matches = query.matches(tree.root_node)
    
    unique_symbols = {}
    
    for match in matches:
        captures = match[1]
        
        node = None
        kind = "unknown"
        name = ""
        signature = ""
        decorators = []
        bases = []
        parent_name = None
        docstring = None

        if 'deco' in captures:
            deco_nodes = captures['deco']
            if not isinstance(deco_nodes, list): deco_nodes = [deco_nodes]
            for deco in deco_nodes:
                decorators.append(deco.text.decode('utf8').strip())

        if 'class_def' in captures:
            node = captures['class_def'][0] if isinstance(captures['class_def'], list) else captures['class_def']
            kind = 'class'
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
            
            # Extract bases for Python
            if lang_key == 'python':
                bases_node = node.child_by_field_name('superclasses')
                if bases_node:
                    # superclasses: (argument_list (identifier) (identifier))
                    for base in bases_node.children:
                        if base.type in ('identifier', 'attribute'):
                            bases.append(base.text.decode('utf8'))

            parent_name = _get_parent_name(node, lang_key)

        elif 'struct_def' in captures:
            node = captures['struct_def'][0] if isinstance(captures['struct_def'], list) else captures['struct_def']
            kind = 'struct'
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
            parent_name = _get_parent_name(node, lang_key)

        elif 'func_def' in captures:
            node = captures['func_def'][0] if isinstance(captures['func_def'], list) else captures['func_def']
            kind = 'function'
            if _is_async_function(node, lang_key):
                kind = 'async_function'
            
            for deco_text in decorators:
                if '@property' in deco_text: kind = 'property'
                elif '@classmethod' in deco_text: kind = 'classmethod'
                elif '@staticmethod' in deco_text: kind = 'staticmethod'
            
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
                
            params_node = None
            ret_node = None
            if 'params' in captures:
                params_node = captures['params'][0] if isinstance(captures['params'], list) else captures['params']
            if 'ret' in captures:
                ret_node = captures['ret'][0] if isinstance(captures['ret'], list) else captures['ret']
                
            params_text = params_node.text.decode('utf8') if params_node else None
            ret_text = ret_node.text.decode('utf8') if ret_node else None
            signature = lang_def.format_signature(params_text, ret_text)
            
            parent_name = _get_parent_name(node, lang_key)

        elif 'field_def' in captures:
            node = captures['field_def'][0] if isinstance(captures['field_def'], list) else captures['field_def']
            
            # Skip local variables inside functions
            if _is_inside_function(node):
                continue
                
            kind = 'variable'
            if 'field_name' in captures:
                name = captures['field_name'][0].text.decode('utf8')
            
            type_text = ""
            value_text = ""
            if 'field_type' in captures:
                type_node = captures['field_type'][0] if isinstance(captures['field_type'], list) else captures['field_type']
                type_text = type_node.text.decode('utf8').strip()
            if 'field_value' in captures:
                val_node = captures['field_value'][0] if isinstance(captures['field_value'], list) else captures['field_value']
                value_text = val_node.text.decode('utf8').strip()
            
            if type_text and value_text:
                signature = f"{type_text} = {value_text}" if type_text.startswith(':') else f": {type_text} = {value_text}"
            elif type_text:
                signature = type_text if type_text.startswith(':') else f": {type_text}"
            elif value_text:
                signature = f" = {value_text}"
                
            parent_name = _get_parent_name(node, lang_key)

        if node and name:
            docstring = _extract_docstring_from_node(node, content_bytes, lang_key)
            if parent_name and kind == 'function': kind = 'method'
            if parent_name and kind == 'async_function': kind = 'async_method'
            if parent_name and name == parent_name and kind in ('function', 'method', 'async_function', 'async_method'):
                name = f"{name}()"

            is_core = docstring and "@CORE" in docstring
            visibility = lang_def.get_visibility(captures, content_bytes)

            sym = Symbol(
                name=name,
                kind=kind,
                line=node.start_point[0] + 1,
                docstring=docstring,
                signature=signature if signature else None,
                parent=parent_name,
                is_core=is_core,
                visibility=visibility,
                lang=lang_key,
                decorators=decorators,
                bases=bases,
                full_content=node.text.decode('utf8')
            )
            
            node_id = node.start_byte
            if node_id in unique_symbols:
                existing = unique_symbols[node_id]
                if existing.kind in ('function', 'method') and sym.kind in ('property', 'classmethod', 'staticmethod'):
                    unique_symbols[node_id] = sym
                elif sym.signature and not existing.signature:
                    unique_symbols[node_id] = sym
            else:
                unique_symbols[node_id] = sym
                
    return sorted(unique_symbols.values(), key=lambda s: s.line)
