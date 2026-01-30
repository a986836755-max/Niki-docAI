"""
Models: Context Models.
模型：上下文模型。
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any

@dataclass
class Tag:
    """
    文档/代码标签 (Documentation/Code Tag).
    e.g., @MODULE, !RULE
    """
    name: str
    args: List[str] = field(default_factory=list)
    line: int = 0
    raw: str = ""

@dataclass
class Section:
    """
    文档片段 (Document Section).
    Captured from <!-- NIKI_NAME_START --> ... <!-- NIKI_NAME_END -->
    """
    name: str
    content: str
    raw: str
    start_pos: int
    end_pos: int

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

@dataclass
class FileContext:
    """
    文件上下文 (File Context).
    """
    path: Path
    rel_path: str
    content: Optional[str] = None
    
    # Analysis Results
    tags: List[Tag] = field(default_factory=list)
    sections: Dict[str, Section] = field(default_factory=dict)
    symbols: List[Symbol] = field(default_factory=list) # Extracted symbols
    docstring: Optional[str] = None
    is_core: bool = False # Whether file is marked as @CORE
    
    # AST Data (Optional, lazy loaded)
    ast_tree: Any = None # Optional[Tree] from tree-sitter
    
    # 提取的元数据 (Extracted Metadata)
    # Computed from tags/docstring
    title: Optional[str] = None
    description: Optional[str] = None
    
    @property
    def has_content(self) -> bool:
        return self.content is not None

@dataclass
class DirectoryContext:
    """
    目录上下文 (Directory Context).
    """
    path: Path
    files: List[FileContext] = field(default_factory=list)
    subdirs: List[Path] = field(default_factory=list)
    
    @property
    def name(self) -> str:
        return self.path.name
