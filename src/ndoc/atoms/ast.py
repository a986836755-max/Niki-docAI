"""
Atoms: AST Parsing (Tree-sitter Wrapper).
原子能力：AST 解析 (Tree-sitter 封装)。
"""
from typing import List, Optional, Dict, Any, Iterator
from dataclasses import dataclass, field
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Tree, Node

from ..models.context import Symbol

# --- Configuration ---
PY_LANGUAGE = Language(tspython.language())

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

def get_parser() -> Parser:
    """
    获取解析器实例 (Get Parser Instance).
    """
    parser = Parser(PY_LANGUAGE)
    return parser

def parse_code(content: str) -> Tree:
    """
    解析代码生成 CST (Parse code to CST).
    
    Args:
        content: 源代码字符串
        
    Returns:
        Tree: Tree-sitter Tree 对象
    """
    parser = get_parser()
    # Tree-sitter expects bytes, encoding handled here
    return parser.parse(bytes(content, "utf8"))

def query_tree(tree: Tree, query_scm: str) -> List[Dict[str, Node]]:
    """
    使用 S-expression 查询树 (Query Tree using S-expressions).
    Implementation: Query as Data.
    
    Args:
        tree: Tree 对象
        query_scm: S-expression 查询语句
        
    Returns:
        List[Dict[str, Node]]: 匹配的捕获组 (List of capture dicts)
        e.g. [{'name': Node, 'definition': Node}, ...]
    """
    query = PY_LANGUAGE.query(query_scm)
    captures = query.captures(tree.root_node)
    
    # Tree-sitter's captures API returns a list of (Node, str) tuples.
    # We need to group them by match pattern if we want structured data,
    # but captures() flattens everything.
    # However, for simple extraction (like "get all classes"), a flat list of nodes is fine.
    # But wait, we want to know WHICH capture name it matched (e.g. @name vs @class).
    
    # Improved return format: List of (capture_name, Node)
    # We can't easily group by "match instance" without `matches()` API.
    # Let's use `matches()` instead of `captures()` for structured extraction.
    
    results = []
    matches = query.matches(tree.root_node)
    for match in matches:
        # match is (match_id, {capture_name: [Node, ...]}) (in older bindings)
        # or just a match object.
        # Let's check the latest binding behavior. 
        # Assuming standard behavior: match is a dictionary of capture_name -> [Node] or Node.
        
        # In tree-sitter 0.23+ bindings, matches() returns iterator of Match.
        # Match.captures is a dict { capture_name: Node | [Node] }.
        
        # Let's use a safe extraction assuming we get a dict-like structure from `matches`.
        # Actually, `matches` returns `list[tuple[int, dict[str, Node | list[Node]]]]` in some versions.
        # Let's stick to `captures` for now as it is simpler for flat lists, 
        # but for associating Name with Class, we need structure.
        
        # Let's assume we want to extract definitions.
        # A simple approach is iterating matches.
        pass
        
    # Fallback to simple capture list for now, let the caller process.
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

# --- High-Level Extraction (Business Logic) ---

def extract_symbols(tree: Tree, content_bytes: bytes) -> List[Symbol]:
    """
    提取所有顶级符号 (Extract all top-level symbols).
    Implementation: Query Pipeline.
    """
    symbols = []
    
    # 1. Extract Classes and Functions
    # We query for definition nodes AND their names.
    # Note: 'decorator' field might vary by tree-sitter version or grammar version.
    # In standard python grammar, it's usually (decorated_definition (decorator) definition)
    # But let's check if we can query decorated_definition.
    
    # Revised strategy: 
    # Use simple definition queries first.
    # If we need decorators, we check parent node or use a broader query.
    
    query_scm = """
    (class_definition
      name: (identifier) @name
    ) @class_def
    
    (function_definition
      name: (identifier) @name
      parameters: (parameters) @params
      return_type: (type)? @ret
    ) @func_def
    
    (decorated_definition
      (decorator) @deco
      (function_definition
        name: (identifier) @name
        parameters: (parameters) @params
        return_type: (type)? @ret
      ) @func_def
    )
    """
    
    query = PY_LANGUAGE.query(query_scm)
    matches = query.matches(tree.root_node)
    
    unique_symbols = {} # Map[start_byte, Symbol]
    
    for match in matches:
        # match is tuple: (pattern_index, capture_dict)
        # capture_dict: { 'name': [Node], 'class_def': [Node], ... }
        captures = match[1]
        
        node = None
        kind = "unknown"
        name = ""
        signature = ""
        decorators = []

        # Collect decorators first
        if 'deco' in captures:
            deco_nodes = captures['deco']
            if not isinstance(deco_nodes, list):
                deco_nodes = [deco_nodes]
            
            for deco in deco_nodes:
                decorators.append(deco.text.decode('utf8').strip())

        if 'class_def' in captures:
            node = captures['class_def'][0] if isinstance(captures['class_def'], list) else captures['class_def']
            kind = 'class'
        elif 'func_def' in captures:
            node = captures['func_def'][0] if isinstance(captures['func_def'], list) else captures['func_def']
            kind = 'function'
            
            # Check decorator for @property or @classmethod or @staticmethod
            for deco_text in decorators:
                if '@property' in deco_text:
                    kind = 'property'
                elif '@classmethod' in deco_text:
                    kind = 'classmethod'
                elif '@staticmethod' in deco_text:
                    kind = 'staticmethod'
            
            # Extract signature components
            params_node = None
            ret_node = None
            
            if 'params' in captures:
                params_node = captures['params'][0] if isinstance(captures['params'], list) else captures['params']
            
            if 'ret' in captures:
                ret_node = captures['ret'][0] if isinstance(captures['ret'], list) else captures['ret']
                
            if params_node:
                # Clean newlines from params for compact display
                p_text = params_node.text.decode('utf8')
                p_text = " ".join(p_text.split())
                signature = p_text
                
            if ret_node:
                r_text = ret_node.text.decode('utf8')
                signature += f" -> {r_text}"
            
        if 'name' in captures:
            name_node = captures['name'][0] if isinstance(captures['name'], list) else captures['name']
            name = name_node.text.decode('utf8')
            
        if node and name:
            # Try to find docstring (first expression statement string in block)
            docstring = _extract_docstring_from_node(node, content_bytes)
            
            sym = Symbol(
                name=name,
                kind=kind,
                line=node.start_point[0] + 1,
                docstring=docstring,
                signature=signature if signature else None
            )
            
            # De-duplication logic
            # Prioritize specific kinds (property/classmethod) over generic function
            node_id = node.start_byte
            if node_id in unique_symbols:
                existing = unique_symbols[node_id]
                # If existing is generic 'function' and new is specific, overwrite
                if existing.kind == 'function' and sym.kind in ('property', 'classmethod', 'staticmethod'):
                    unique_symbols[node_id] = sym
                # If new has signature and existing doesn't, overwrite (unlikely with this logic but safe)
                elif sym.signature and not existing.signature:
                     unique_symbols[node_id] = sym
            else:
                unique_symbols[node_id] = sym
                
    # Sort by line number
    symbols = sorted(unique_symbols.values(), key=lambda s: s.line)
    return symbols

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

# --- Predefined Queries (Logic as Data) ---

QUERY_CLASSES = """
(class_definition
  name: (identifier) @name
) @class
"""

QUERY_FUNCTIONS = """
(function_definition
  name: (identifier) @name
) @function
"""
