"""
Atoms: File System Traversal.
原子能力：文件系统遍历。
"""
import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Iterator, List, Set, Pattern, Callable, Optional
import pathspec

# --- Data Structures (Logic as Data) ---

@dataclass
class FileFilter:
    """
    文件过滤器配置 (File Filter Configuration).
    """
    ignore_patterns: Set[str] = field(default_factory=set)
    allow_extensions: Set[str] = field(default_factory=set)
    spec: Optional[pathspec.PathSpec] = None

    @property
    def has_extension_filter(self) -> bool:
        return bool(self.allow_extensions)

# --- Engine (Pipeline) ---

def load_gitignore(root: Path) -> Optional[pathspec.PathSpec]:
    """Load .gitignore from root directory."""
    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                return pathspec.PathSpec.from_lines('gitwildmatch', f)
        except Exception:
            pass
    return None

def should_ignore(path: Path, filter_config: FileFilter, root: Path = None) -> bool:
    """
    检查是否应该忽略 (Check if should ignore).
    Implementation: Table lookup (Set) + Gitignore (PathSpec).
    """
    name = path.name
    
    # 1. Hidden file check (Rule)
    if name.startswith('.') and name != '.':
        return True
        
    # 2. Ignore list lookup (Data)
    if name in filter_config.ignore_patterns:
        return True

    # 3. .gitignore check (Logic as Data)
    if filter_config.spec and root:
        try:
            rel_path = path.relative_to(root).as_posix()
            if filter_config.spec.match_file(rel_path):
                return True
        except ValueError:
            pass
            
    return False

def list_dir(path: Path, filter_config: FileFilter, root: Path = None) -> List[Path]:
    """
    列出目录内容并应用过滤 (List directory contents with filtering).
    Returns sorted list: Directories first, then files.
    """
    if not path.is_dir():
        return []

    # Auto-load gitignore if not provided and we are at root
    if not filter_config.spec and root and path == root:
        filter_config.spec = load_gitignore(root)

    try:
        entries = path.iterdir()
    except PermissionError:
        return []

    filtered_entries = []
    for entry in entries:
        # Check ignore patterns
        if should_ignore(entry, filter_config, root):
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
    # Load gitignore if available
    config.spec = load_gitignore(root)

    for entry in os.walk(root):
        dirpath, dirnames, filenames = entry
        curr_dir = Path(dirpath)
        
        # Prune directories
        to_remove = []
        for d in dirnames:
            d_path = curr_dir / d
            if should_ignore(d_path, config, root):
                to_remove.append(d)
        
        for d in to_remove:
            dirnames.remove(d)
        
        # Filter files
        for f in filenames:
            f_path = curr_dir / f
            if should_ignore(f_path, config, root):
                continue
                
            # Extension check (Data Lookup)
            if config.has_extension_filter:
                if f_path.suffix.lower() not in config.allow_extensions:
                    continue
            
            yield f_path

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
