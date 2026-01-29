"""
Atoms: File System Traversal.
原子能力：文件系统遍历。
"""
import os
from pathlib import Path
from typing import Iterator, List, Set

def should_ignore(name: str, ignore_patterns: List[str]) -> bool:
    """
    检查是否应该忽略该文件/目录 (Check if file/dir should be ignored).
    
    Args:
        name: 文件名/目录名 (Filename or dirname)
        ignore_patterns: 忽略模式列表 (List of ignore patterns)
        
    Returns:
        bool: True if should ignore
    """
    # 简单匹配：如果名字在忽略列表中，或者以 . 开头（且不在白名单中，暂时统一忽略隐藏文件）
    # Simple match: exact match or starts with .
    if name in ignore_patterns:
        return True
    if name.startswith('.') and name != '.':
        # 除非明确需要包含点文件，否则默认忽略
        return True
    return False

def walk_files(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]:
    """
    遍历目录并返回文件路径 (Walk directory and yield file paths).
    
    Args:
        root: 根目录 (Root directory)
        ignore_patterns: 忽略列表 (Ignore patterns)
        extensions: 允许的扩展名列表 (Allowed extensions), e.g. ['.py', '.md']
        
    Yields:
        Path: 文件绝对路径 (Absolute file path)
    """
    if not root.exists():
        return

    # Convert extensions to set for O(1) lookup, ensure lower case
    ext_set = set(e.lower() for e in extensions) if extensions else None

    for entry in os.walk(root):
        dirpath, dirnames, filenames = entry
        
        # Modify dirnames in-place to skip ignored directories
        # list(...) to create a copy for safe iteration while modifying
        for d in list(dirnames):
            if should_ignore(d, ignore_patterns):
                dirnames.remove(d)
        
        for f in filenames:
            if should_ignore(f, ignore_patterns):
                continue
                
            path = Path(dirpath) / f
            
            if ext_set:
                if path.suffix.lower() not in ext_set:
                    continue
            
            yield path

def get_relative_path(path: Path, root: Path) -> str:
    """
    获取相对路径字符串 (Get relative path string).
    
    Args:
        path: 目标路径
        root: 根路径
        
    Returns:
        str: 相对路径字符串 (统一使用 forward slash)
    """
    try:
        rel = path.relative_to(root)
        return rel.as_posix()
    except ValueError:
        return path.as_posix()
