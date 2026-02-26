"""
Models: Context Models.
模型：上下文模型。
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
from .symbol import Symbol, Tag

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
    imports: List[str] = field(default_factory=list) # Extracted imports
    docstring: Optional[str] = None
    description: Optional[str] = None # Added for compatibility
    is_core: bool = False # Whether file is marked as @CORE
    memories: List[Dict[str, Any]] = field(default_factory=list) # Extracted memories (!RULE, !WARN)
    
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
