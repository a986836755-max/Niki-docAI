"""
Atoms: AST Symbol Extraction.
符号提取核心逻辑。
"""
from typing import List, Optional
from pathlib import Path
from tree_sitter import Tree
from .base import get_language
from .utils import (
    truncate, _get_parent_name, _is_inside_function, 
    _extract_docstring_from_node, _is_async_function,
    MAX_VALUE_LENGTH, MAX_CONTENT_LENGTH
)
from ..text_utils import extract_tags_from_text
from ...models.context import Symbol
from .. import langs

def extract_symbols(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]:
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
        visibility_text = ""

        # ... (rest of the logic remains same, but Symbol should include path)
        # Note: We'll update the loop at the end to include path if available

        # Pre-extract visibility/modifiers
        for capture_name, capture_node in captures.items():
            if capture_name == 'visibility':
                v_nodes = capture_node if isinstance(capture_node, list) else [capture_node]
                visibility_text = " ".join([v.text.decode('utf8').strip() for v in v_nodes])
                break
        
        # C# modifiers fallback
        if not visibility_text and lang_key == 'c_sharp':
            target_node = None
            if 'class_def' in captures: target_node = captures['class_def']
            elif 'func_def' in captures: target_node = captures['func_def']
            elif 'struct_def' in captures: target_node = captures['struct_def']
            if isinstance(target_node, list): target_node = target_node[0]
            if target_node:
                for child in target_node.children:
                    if child.type == 'modifier':
                        visibility_text += child.text.decode('utf8') + " "
                visibility_text = visibility_text.strip()

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
            
            if lang_key == 'python':
                bases_node = node.child_by_field_name('superclasses')
                if bases_node:
                    for base in bases_node.children:
                        if base.type in ('identifier', 'attribute'):
                            bases.append(base.text.decode('utf8'))
            elif lang_key == 'c_sharp':
                if 'bases' in captures:
                    bases_node = captures['bases'][0] if isinstance(captures['bases'], list) else captures['bases']
                    for child in bases_node.children:
                        if child.type == 'base_type':
                            bases.append(child.text.decode('utf8'))
            parent_name = _get_parent_name(node, lang_key)

        elif 'struct_def' in captures:
            node = captures['struct_def'][0] if isinstance(captures['struct_def'], list) else captures['struct_def']
            kind = 'struct'
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
            parent_name = _get_parent_name(node, lang_key)

        elif 'enum_def' in captures:
            node = captures['enum_def'][0] if isinstance(captures['enum_def'], list) else captures['enum_def']
            kind = 'enum'
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
            parent_name = _get_parent_name(node, lang_key)

        elif 'record_def' in captures:
            node = captures['record_def'][0] if isinstance(captures['record_def'], list) else captures['record_def']
            kind = 'record'
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
                
            params_node = captures.get('params')[0] if isinstance(captures.get('params'), list) else captures.get('params')
            ret_node = captures.get('ret')[0] if isinstance(captures.get('ret'), list) else captures.get('ret')
                
            params_text = params_node.text.decode('utf8') if params_node else None
            ret_text = ret_node.text.decode('utf8') if ret_node else None
            signature = lang_def.format_signature(params_text, ret_text)
            parent_name = _get_parent_name(node, lang_key)

        elif 'field_def' in captures:
            node = captures['field_def'][0] if isinstance(captures['field_def'], list) else captures['field_def']
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
                value_text = truncate(val_node.text.decode('utf8').strip(), MAX_VALUE_LENGTH)
            
            if type_text and value_text:
                signature = f"{type_text} = {value_text}" if type_text.startswith(':') else f": {type_text} = {value_text}"
            elif type_text:
                signature = type_text if type_text.startswith(':') else f": {type_text}"
            elif value_text:
                signature = f" = {value_text}"
            parent_name = _get_parent_name(node, lang_key)

        elif 'property_def' in captures:
            node = captures['property_def'][0] if isinstance(captures['property_def'], list) else captures['property_def']
            kind = 'property'
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
            ret_node = captures.get('ret')[0] if isinstance(captures.get('ret'), list) else captures.get('ret')
            ret_text = ret_node.text.decode('utf8') if ret_node else None
            signature = lang_def.format_signature(None, ret_text)
            parent_name = _get_parent_name(node, lang_key)

        elif 'namespace_def' in captures:
            node = captures['namespace_def'][0] if isinstance(captures['namespace_def'], list) else captures['namespace_def']
            kind = 'namespace'
            if 'name' in captures:
                name = captures['name'][0].text.decode('utf8')
            parent_name = None

        if node and name:
            docstring = _extract_docstring_from_node(node, content_bytes, lang_key)
            if parent_name and kind == 'function': kind = 'method'
            if parent_name and kind == 'async_function': kind = 'async_method'
            if parent_name and name == parent_name and kind in ('function', 'method', 'async_function', 'async_method'):
                name = f"{name}()"

            is_core = docstring and "@CORE" in docstring
            visibility = visibility_text if visibility_text else lang_def.get_visibility(captures, content_bytes)
            
            # Extract tags from docstring
            tags = extract_tags_from_text(docstring, node.start_point[0] + 1) if docstring else []

            sym = Symbol(
                name=name, kind=kind, line=node.start_point[0] + 1,
                docstring=docstring, signature=signature if signature else None,
                parent=parent_name, is_core=is_core, visibility=visibility,
                lang=lang_key, decorators=decorators, bases=bases,
                full_content=truncate(node.text.decode('utf8'), MAX_CONTENT_LENGTH),
                path=str(file_path) if file_path else None,
                tags=tags
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
