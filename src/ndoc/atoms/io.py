"""
Atoms: Input/Output Operations.
副作用隔离层：所有磁盘读写必须在此完成。
"""
import os
import re
from pathlib import Path
from typing import List, Optional, Callable, Any

# --- Data Structures (Side Effects as Data) ---

# IO Operation Types (Implicit)
# Read: Path -> Optional[str]
# Write: (Path, Content) -> bool

# --- Engine (Safe Execution Pipeline) ---

def safe_io(operation: Callable[..., Any], error_msg: str, *args, **kwargs) -> Any:
    """
    通用 IO 错误处理包装器 (Generic IO error handling wrapper).
    
    Args:
        operation: IO 函数
        error_msg: 错误消息模板
        
    Returns:
        Result or None/False
    """
    try:
        return operation(*args, **kwargs)
    except Exception as e:
        # Side effect: Print error
        # In a pure FP world, this would return a Result<T, E> monad.
        # For simplicity in this project, we print and return None/False.
        print(error_msg.format(e=e))
        return None

def read_text(path: Path) -> Optional[str]:
    """
    安全读取文件内容 (Safely read file content).
    
    Args:
        path: 文件路径
        
    Returns:
        Optional[str]: 文件内容
    """
    if not path.exists():
        return None
        
    def _read():
        return path.read_text(encoding='utf-8', errors='ignore')
        
    return safe_io(_read, f"Error reading {path}: {{e}}")

def write_text(path: Path, content: str) -> bool:
    """
    安全写入文件内容 (Safely write file content).
    
    Args:
        path: 文件路径
        content: 内容
        
    Returns:
        bool: 是否成功
    """
    def _write():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return True
        
    result = safe_io(_write, f"Error writing {path}: {{e}}")
    return result is True

def read_lines(path: Path) -> List[str]:
    """
    读取文件行列表 (Read file lines).
    
    Args:
        path: 文件路径
        
    Returns:
        List[str]: 行列表
    """
    # Composition: read_text -> splitlines
    content = read_text(path)
    return content.splitlines() if content else []

def append_text(path: Path, content: str) -> bool:
    """
    追加内容到文件 (Append content to file).
    
    Args:
        path: 文件路径
        content: 内容
    """
    def _append():
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
        
    result = safe_io(_append, f"Error appending to {path}: {{e}}")
    return result is True

def update_section(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool:
    """
    更新文件指定标记之间的内容 (Update content between markers).
    Implementation: Regex Transformation Pipeline.
    
    Args:
        path: 文件路径
        start_marker: 开始标记
        end_marker: 结束标记
        new_content: 新内容
    """
    content = read_text(path)
    if content is None:
        return False

    # Data: Regex Pattern
    pattern = re.compile(
        f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})",
        re.DOTALL
    )
    
    # Transformation: Check existence
    if not pattern.search(content):
        print(f"Markers not found in {path}: {start_marker} ... {end_marker}")
        return False
    
    # Transformation: Substitute
    replacement = f"\\1\n{new_content}\n\\3"
    updated_content = pattern.sub(replacement, content)
    
    # Action: Write if changed
    if updated_content != content:
        return write_text(path, updated_content)
    
    return True
