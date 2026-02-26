# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Centralized Language Access**: All AST operations must obtain language instances via `base.get_language()` or `...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: AST Symbol Discovery.
代码发现逻辑：查找调用与导入。
"""
from typing import List
from tree_sitter import Tree
from .base import get_language, query_tree
from .. import langs

def find_calls(tree: Tree, lang_key: str = 'python') -> List[str]:
    lang = get_language(lang_key)
    if not lang:
        return []
        
    lang_def = langs.get_lang_def(lang_key)
    query_scm = getattr(lang_def, 'SCM_CALLS', None) or getattr(lang_def, 'CALL_QUERY', None)
    if not query_scm:
        return []
        
    results = query_tree(tree, query_scm, lang_key)
    
    calls = []
    for capture in results:
        if capture['name'] in ('call', 'call_name'):
            node = capture['node']
            calls.append(node.text.decode('utf8'))
    return list(set(calls))

def find_calls_with_loc(tree: Tree, lang_key: str = 'python') -> List[dict]:
    """
    Find function calls with location info.
    Returns: [{"name": "func_name", "line": 10}, ...]
    """
    lang = get_language(lang_key)
    if not lang:
        return []
        
    lang_def = langs.get_lang_def(lang_key)
    query_scm = getattr(lang_def, 'SCM_CALLS', None) or getattr(lang_def, 'CALL_QUERY', None)
    if not query_scm:
        return []
        
    results = query_tree(tree, query_scm, lang_key)
    
    calls = []
    for capture in results:
        if capture['name'] in ('call', 'call_name'):
            node = capture['node']
            calls.append({
                "name": node.text.decode('utf8'),
                "line": node.start_point[0] + 1
            })
    return calls

def find_imports(tree: Tree, lang_key: str = 'python') -> List[str]:
    lang = get_language(lang_key)
    if not lang:
        return []
        
    lang_def = langs.get_lang_def(lang_key)
    query_scm = getattr(lang_def, 'SCM_IMPORTS', None)
    if not query_scm:
        return []
        
    results = query_tree(tree, query_scm, lang_key)
    
    imports = []
    for capture in results:
        # print(f"DEBUG: capture={capture['name']} node={capture['node'].type} text={capture['node'].text.decode('utf8')}")
        if capture['name'] == 'import':
            node = capture['node']
            raw_text = node.text.decode('utf8').strip()
            # Use language-specific cleaner if available
            if lang_def and hasattr(lang_def, 'clean_import'):
                clean_text = lang_def.clean_import(raw_text)
                imports.append(clean_text)
            else:
                imports.append(raw_text)
    return list(set(imports))
