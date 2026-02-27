# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - POD Only: Models must be Plain Old Data (dataclasses/pydantic). No business logic methods allowed.
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Models: Code Symbol.
模型：代码符号。
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Tag:
    """
    文档/代码标签 (Documentation/Code Tag).
    e.g., @MODULE, !RULE
    Supports attributes: !RULE[CRITICAL], @ADR[CONF=0.8]
    """
    name: str
    args: List[str] = field(default_factory=list)
    line: int = 0
    raw: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict) # New: Tag attributes

@dataclass
class Symbol:
    """
    代码符号 (Code Symbol).
    Extracted from AST (Class, Function, etc.)
    """
    name: str
    kind: str # 'class' | 'function' | 'method'
    line: int
    docstring: Optional[str] = None
    signature: Optional[str] = None # e.g. "(x: int) -> int"
    parent: Optional[str] = None # e.g. "ClassName" for methods/fields
    is_core: bool = False # Whether symbol is marked as @CORE
    visibility: str = "public" # 'public' | 'private' | 'protected'
    lang: str = "unknown" # Language key (e.g., 'python', 'go')
    decorators: List[str] = field(default_factory=list)
    bases: List[str] = field(default_factory=list)
    full_content: str = "" # Full source of the symbol
    path: Optional[str] = None # File path of the symbol
    tags: List[Tag] = field(default_factory=list) # Extracted @TAGS
    test_usages: List[Dict[str, Any]] = field(default_factory=list)  # [{"path": "tests/foo.py", "line": 10}]

    @property
    def is_public(self) -> bool:
        """
        Check if symbol is public.
        1. Check visibility attribute (from AST modifiers)
        2. Check naming convention (Python style _, JS/TS style #, Go style Uppercase)
        """
        # 1. AST visibility takes precedence
        v_lower = self.visibility.lower()
        if 'private' in v_lower or 'protected' in v_lower:
            return False
        
        # 2. Language-specific naming conventions
        if self.lang == 'go':
            # Go: Uppercase means public
            if self.name and self.name[0].isupper():
                return True
            return False

        # Fallback naming convention (Python, JS, etc.)
        # Python: _name, JS/TS: #name
        if self.name.startswith('_') or self.name.startswith('#'):
            return False
            
        return True
