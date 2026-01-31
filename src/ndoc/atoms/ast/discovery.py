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
        if capture['name'] == 'import':
            node = capture['node']
            imports.append(node.text.decode('utf8').strip())
    return list(set(imports))
