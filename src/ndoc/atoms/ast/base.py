"""
Atoms: AST Parsing Base.
基础解析能力：Tree-sitter 初始化与核心解析。
"""
from typing import Optional, Dict
from pathlib import Path
from tree_sitter import Language, Parser, Tree
from dataclasses import dataclass, field
from .. import langs

# Cache languages
_LANGUAGES = {}

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

@dataclass
class AstNode:
    """
    通用 AST 节点数据结构 (Generic AST Node Data).
    """
    type: str
    text: str
    start_point: tuple[int, int]  # (row, col)
    end_point: tuple[int, int]
    children: list['AstNode'] = field(default_factory=list)

    @property
    def start_line(self) -> int:
        return self.start_point[0] + 1

    @property
    def end_line(self) -> int:
        return self.end_point[0] + 1

def get_parser(lang_key: str = 'python') -> Optional[Parser]:
    lang = get_language(lang_key)
    if not lang:
        return None
    try:
        return Parser(lang)
    except Exception:
        return None

def parse_code(content: str, file_path: Optional[Path] = None) -> Optional[Tree]:
    if file_path:
        lang_key = get_lang_key(file_path)
    else:
        lang_key = 'python'
        
    if not lang_key:
        return None

    parser = get_parser(lang_key)
    if not parser:
        return None
        
    return parser.parse(bytes(content, "utf8"))

def get_lang_key(file_path: Path) -> Optional[str]:
    """
    根据文件后缀获取语言标识符 (Get language ID by extension).
    """
    ext = file_path.suffix.lower()
    return langs.get_lang_id_by_ext(ext)

def query_tree(tree: Tree, query_scm: str, lang_key: str = 'python') -> list[dict]:
    lang = get_language(lang_key)
    if not lang:
        return []
        
    query = lang.query(query_scm)
    captures = query.captures(tree.root_node)
    
    results = []
    if isinstance(captures, dict):
        for name, nodes in captures.items():
            for node in nodes:
                results.append({'name': name, 'node': node})
    else:
        for node, name in captures:
            results.append({'name': name, 'node': node})
    return results
