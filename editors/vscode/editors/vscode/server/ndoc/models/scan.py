# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - POD Only: Models must be Plain Old Data (dataclasses/pydantic). No business logic methods allowed.
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Models for Scan Results.
扫描结果的数据模型 (DOD: Data Only).
"""
from dataclasses import dataclass, field
from typing import List, Dict, Pattern, Optional, Any
from .symbol import Tag, Symbol
from .context import Section

@dataclass
class TokenRule:
    """
    词法分析规则 (Lexical Analysis Rule).
    """
    name: str
    pattern: Pattern
    group_map: Dict[str, int]  # Map logical names to regex groups

@dataclass
class ScanResult:
    """
    扫描结果 (Scan Result).
    纯数据结构，无业务逻辑。
    """
    tags: List[Tag] = field(default_factory=list)
    sections: Dict[str, Section] = field(default_factory=dict)
    symbols: List[Symbol] = field(default_factory=list)
    docstring: str = ""
    summary: str = ""
    todos: List[dict] = field(default_factory=list)  # Captured TODOs
    memories: List[dict] = field(default_factory=list) # Captured Memories (!RULE, !WARN)
    decisions: List[dict] = field(default_factory=list) # Captured @DECISION
    intents: List[str] = field(default_factory=list) # Captured @INTENT
    lessons: List[dict] = field(default_factory=list) # Captured @LESSON
    calls: List[str] = field(default_factory=list)  # Captured calls
    imports: List[str] = field(default_factory=list)  # Captured imports
    tokens: Dict[str, int] = field(default_factory=dict) # Token frequency map for LSP
    is_core: bool = False # Whether file is marked as @CORE
