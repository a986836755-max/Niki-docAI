"""
Atoms: Semantic Skeleton Generator.
原子能力：代码语义骨架生成。
"""
from typing import Optional, List, Tuple
from tree_sitter import Node
from pathlib import Path
from .base import parse_code, get_lang_key
from .. import langs

def generate_skeleton(content: str, file_path: Optional[str] = None) -> str:
    """
    Generate a semantic skeleton of the code.
    Retains: Class/Function signatures, Docstrings, Decorators.
    Replaces: Function bodies with '...'.
    """
    path_obj = Path(file_path) if file_path else None
    
    # Heuristic for lang key if no path
    lang_key = get_lang_key(path_obj) if path_obj else 'python'
        
    if not lang_key:
        return content[:500] + "\n... (Unknown Language)"

    # Ensure language capability is loaded (Important for C++/Rust which might need local install)
    if path_obj:
        from ndoc.core.capabilities import CapabilityManager
        # Try to ensure the language is available (auto-install if needed)
        CapabilityManager.ensure_languages({lang_key}, auto_install=True)

    tree = parse_code(content, path_obj)
    if not tree:
        return content[:500] + "\n... (Parse Failed)"
    
    return _reconstruct_skeleton(tree.root_node, content.encode('utf-8'), lang_key)

def _reconstruct_skeleton(node: Node, content_bytes: bytes, lang_key: str) -> str:
    """
    Recursively reconstruct code, skipping bodies.
    """
    ranges_to_skip: List[Tuple[int, int]] = []
    
    def visit(n: Node):
        # Check if this node is a function/method body
        if _is_body_node(n, lang_key):
            ranges_to_skip.append((n.start_byte, n.end_byte))
            # Don't recurse into skipped body
            return
            
        for child in n.children:
            visit(child)
            
    visit(node)
    
    # Sort ranges by start position
    ranges_to_skip.sort(key=lambda x: x[0])
    
    # Merge overlapping ranges (though tree structure usually prevents this for bodies)
    merged_ranges = []
    if ranges_to_skip:
        curr_start, curr_end = ranges_to_skip[0]
        for start, end in ranges_to_skip[1:]:
            if start < curr_end:
                curr_end = max(curr_end, end)
            else:
                merged_ranges.append((curr_start, curr_end))
                curr_start, curr_end = start, end
        merged_ranges.append((curr_start, curr_end))
    
    output = []
    current_pos = 0
    
    for start, end in merged_ranges:
        if start < current_pos:
            continue
            
        # Append text before the body
        # Decode only the chunk we need
        chunk = content_bytes[current_pos:start].decode('utf-8', errors='replace')
        output.append(chunk)
        
        # Append ellipsis with a newline for readability
        # Try to infer indentation from previous line?
        # For simplicity, just " ..."
        output.append(" ...")
        
        current_pos = end
        
    # Append remaining text
    output.append(content_bytes[current_pos:].decode('utf-8', errors='replace'))
    
    return "".join(output)

def _is_body_node(node: Node, lang_key: str) -> bool:
    """
    Check if a node represents an implementation body that should be skipped.
    """
    type_name = node.type
    parent = node.parent
    if not parent:
        return False
        
    parent_type = parent.type
    
    if lang_key == 'python':
        # Skip function bodies (block)
        if parent_type in ('function_definition', 'async_function_definition'):
            if type_name == 'block':
                return True
    
    elif lang_key in ('javascript', 'typescript', 'tsx', 'jsx'):
        # Skip function bodies (statement_block)
        if parent_type in ('function_declaration', 'method_definition', 'arrow_function'):
            if type_name == 'statement_block':
                return True
                
    elif lang_key in ('java', 'c_sharp', 'cpp', 'go', 'rust', 'dart'):
        # C-style languages: body is usually a 'block' or 'compound_statement'
        if parent_type in ('method_declaration', 'function_definition', 'function_declaration', 'constructor_declaration'):
            if type_name in ('block', 'compound_statement', 'function_body'):
                return True
                
    return False
