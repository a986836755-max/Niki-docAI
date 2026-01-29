"""
Atoms: File System Traversal.
原子能力：文件系统遍历。
"""
import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Iterator, List, Set, Pattern, Callable

# --- Data Structures (Logic as Data) ---

@dataclass
class FileFilter:
    """
    文件过滤器配置 (File Filter Configuration).
    """
    ignore_patterns: Set[str] = field(default_factory=set)
    allow_extensions: Set[str] = field(default_factory=set)
    # 预编译的正则列表，用于更复杂的忽略规则 (Pre-compiled regex for complex ignores)
    # 暂时保留扩展性，目前使用精确匹配
    
    @property
    def has_extension_filter(self) -> bool:
        return bool(self.allow_extensions)

# --- Engine (Pipeline) ---

def should_ignore(name: str, filter_config: FileFilter) -> bool:
    """
    检查是否应该忽略 (Check if should ignore).
    Implementation: Table lookup (Set).
    
    Args:
        name: 文件名
        filter_config: 过滤配置
        
    Returns:
        bool: True if ignored
    """
    # 1. Hidden file check (Rule)
    if name.startswith('.') and name != '.':
        return True
        
    # 2. Ignore list lookup (Data)
    return name in filter_config.ignore_patterns


def list_dir(path: Path, filter_config: FileFilter) -> List[Path]:
    """
    列出目录内容并应用过滤 (List directory contents with filtering).
    Returns sorted list: Directories first, then files.
    """
    if not path.is_dir():
        return []

    try:
        entries = path.iterdir()
    except PermissionError:
        return []

    filtered_entries = []
    for entry in entries:
        # Check ignore patterns (common for files and dirs)
        if should_ignore(entry.name, filter_config):
            continue
            
        # Check extensions (files only)
        if entry.is_file() and filter_config.has_extension_filter:
            if entry.suffix.lower() not in filter_config.allow_extensions:
                continue
                
        filtered_entries.append(entry)

    # Sort: Directories first (is_file=False), then files (is_file=True), then by name
    return sorted(filtered_entries, key=lambda x: (x.is_file(), x.name))

def walk_files(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]:
    """
    遍历目录并返回文件路径 (Walk directory and yield file paths).
    Implementation: Generator Pipeline.
    
    Args:
        root: 根目录
        ignore_patterns: 忽略列表
        extensions: 允许的扩展名列表
        
    Yields:
        Path: 文件路径
    """
    if not root.exists():
        return

    # 1. Prepare Data (Config Construction)
    config = FileFilter(
        ignore_patterns=set(ignore_patterns),
        allow_extensions=set(e.lower() for e in extensions) if extensions else set()
    )

    # 2. Execute Pipeline (Walk -> Filter -> Yield)
    for entry in os.walk(root):
        dirpath, dirnames, filenames = entry
        
        # Prune directories (Mutation required by os.walk)
        # Filter logic delegated to engine function
        # Using list comprehension for filtering implies creating new list, 
        # but os.walk requires modifying 'dirnames' in place to prune recursion.
        # We find items to remove first (Query), then remove (Command).
        to_remove = [d for d in dirnames if should_ignore(d, config)]
        for d in to_remove:
            dirnames.remove(d)
        
        # Filter files
        for f in filenames:
            if should_ignore(f, config):
                continue
                
            path = Path(dirpath) / f
            
            # Extension check (Data Lookup)
            if config.has_extension_filter:
                if path.suffix.lower() not in config.allow_extensions:
                    continue
            
            yield path

def get_relative_path(path: Path, root: Path) -> str:
    """
    获取相对路径字符串 (Get relative path string).
    
    Args:
        path: 目标路径
        root: 根路径
        
    Returns:
        str: 相对路径字符串
    """
    try:
        rel = path.relative_to(root)
        return rel.as_posix()
    except ValueError:
        return path.as_posix()
