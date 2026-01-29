"""
Atoms: Input/Output Operations.
副作用隔离层：所有磁盘读写必须在此完成。
"""
import os
from pathlib import Path
from typing import List, Optional

def read_text(path: Path) -> Optional[str]:
    """
    安全读取文件内容 (Safely read file content).

    Args:
        path: 文件路径 (File path)

    Returns:
        Optional[str]: 文件内容，如果读取失败返回 None
    """
    if not path.exists():
        return None
    
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def write_text(path: Path, content: str) -> bool:
    """
    安全写入文件内容 (Safely write file content).

    Args:
        path: 文件路径 (File path)
        content: 要写入的内容 (Content to write)

    Returns:
        bool: 是否写入成功 (Success status)
    """
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error writing {path}: {e}")
        return False

def read_lines(path: Path) -> List[str]:
    """
    读取文件行列表 (Read file lines).

    Args:
        path: 文件路径 (File path)

    Returns:
        List[str]: 行列表 (List of lines)
    """
    content = read_text(path)
    if content is None:
        return []
    return content.splitlines()

def append_text(path: Path, content: str) -> bool:
    """
    追加内容到文件 (Append content to file).

    Args:
        path: 文件路径
        content: 内容
    """
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error appending to {path}: {e}")
        return False
