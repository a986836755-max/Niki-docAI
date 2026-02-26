# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Centralized Language Access**: All AST operations must obtain language instances via `base.get_language()` or `...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: AST Parsing Base.
基础解析能力：Tree-sitter 初始化与核心解析。
"""
from typing import Optional, Dict
from pathlib import Path
from tree_sitter import Language, Parser, Tree
from dataclasses import dataclass, field
from .. import langs
from ...core.capabilities import CapabilityManager

# Cache languages
_LANGUAGES = {}

def get_language(lang_key: str) -> Optional[Language]:
    if lang_key in _LANGUAGES:
        return _LANGUAGES[lang_key]
    
    # Use CapabilityManager to load/install language dynamically
    # By default, we allow interactive installation prompts
    lang_obj = CapabilityManager.get_language(lang_key)
    
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
    try:
        lang = get_language(lang_key)
        if not lang:
            return None
        return Parser(lang)
    except Exception as e:
        # print(f"Failed to create parser for {lang_key}: {e}")
        return None

def parse_code(content: str, file_path: Optional[Path] = None) -> Optional[Tree]:
    if file_path:
        lang_key = get_lang_key(file_path)
    else:
        lang_key = 'python'
        
    if not lang_key:
        return None

    try:
        parser = get_parser(lang_key)
        if not parser:
            return None
            
        return parser.parse(bytes(content, "utf8"))
    except Exception as e:
        # Log error but don't crash
        # print(f"Warning: Failed to parse {file_path}: {e!r}")
        return None

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
