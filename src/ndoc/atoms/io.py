"""
Atoms: Input/Output Operations.
副作用隔离层：所有磁盘读写必须在此完成。
"""
import os
import re
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

def update_section(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool:
    """
    更新文件指定标记之间的内容 (Update content between markers).
    
    Args:
        path: 文件路径
        start_marker: 开始标记 (不包含换行符)
        end_marker: 结束标记 (不包含换行符)
        new_content: 新内容
        
    Returns:
        bool: 是否更新成功 (True if updated, False if marker not found or error)
    """
    content = read_text(path)
    if content is None:
        return False

    # 转义标记以用于正则 (Escape markers for regex)
    # 使用 DOTALL 模式匹配跨行内容
    pattern = re.compile(
        f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})",
        re.DOTALL
    )
    
    if not pattern.search(content):
        print(f"Markers not found in {path}: {start_marker} ... {end_marker}")
        return False
    
    # 保留标记，替换中间内容
    # 确保新内容前后有换行，保持整洁
    replacement = f"\\1\n{new_content}\n\\3"
    updated_content = pattern.sub(replacement, content)
    
    if updated_content != content:
        return write_text(path, updated_content)
    
    return True

