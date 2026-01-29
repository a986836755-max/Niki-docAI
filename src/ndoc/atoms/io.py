"""
Atoms: Input/Output Operations.
副作用隔离层：所有磁盘读写必须在此完成。
"""
import os
import re
from pathlib import Path
from typing import List, Optional, Callable, Any
from datetime import datetime
import difflib

# Global Flag for Dry Run
# This is a simple state injection for cross-cutting concern
_DRY_RUN_MODE = False

def set_dry_run(enabled: bool):
    """
    Set Dry Run mode globally.
    """
    global _DRY_RUN_MODE
    _DRY_RUN_MODE = enabled

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
    If Dry Run is enabled, prints diff instead of writing.
    
    Args:
        path: 文件路径
        content: 内容
        
    Returns:
        bool: 是否成功 (In dry run, returns True if diff generated)
    """
    if _DRY_RUN_MODE:
        old_content = read_text(path) or ""
        if old_content == content:
            # print(f"  [DryRun] No changes for {path.name}")
            return True
        
        print(f"\n📝 [DryRun] Changes for {path.name}:")
        diff = difflib.unified_diff(
            old_content.splitlines(), 
            content.splitlines(), 
            fromfile=f"a/{path.name}", 
            tofile=f"b/{path.name}",
            lineterm=""
        )
        has_diff = False
        for line in diff:
            has_diff = True
            # Simple color simulation if terminal supports it, or just plain text
            if line.startswith('+') and not line.startswith('+++'):
                print(f"\033[32m{line}\033[0m") # Green
            elif line.startswith('-') and not line.startswith('---'):
                print(f"\033[31m{line}\033[0m") # Red
            else:
                print(line)
        if not has_diff:
            print(f"  (New file content length: {len(content)})")
        return True

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
    if _DRY_RUN_MODE:
        print(f"\n📝 [DryRun] Appending to {path.name}:")
        print(f"\033[32m{content}\033[0m")
        return True

    def _append():
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return safe_io(_append, f"Error appending to {path}: {{e}}")

def update_section(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool:
    """
    更新文件中的特定区块 (Update specific section in file).
    
    Args:
        path: 文件路径
        start_marker: 开始标记
        end_marker: 结束标记
        new_content: 新内容
    """
    content = read_text(path)
    if not content:
        # File doesn't exist or is empty? 
        # For update_section, usually we expect file to exist.
        # But if not, maybe we should return False or handle gracefully?
        # Let's assume it should exist.
        return False
        
    pattern = re.compile(
        f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})", 
        re.DOTALL
    )
    
    if not pattern.search(content):
        # Markers not found. Append? Or fail?
        # DOD: If markers missing, we can't update section.
        print(f"⚠️  Markers not found in {path.name}")
        return False
        
    updated_content = pattern.sub(f"\\1\n{new_content}\n\\3", content)
    
    return write_text(path, updated_content)

def update_header_timestamp(path: Path) -> bool:
    """
    更新文件头部的最后更新时间 (Update Last Updated timestamp in header).
    Target format: > 最后更新 (Last Updated): YYYY-MM-DD HH:MM:SS
    """
    content = read_text(path)
    if not content:
        return False
        
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_line = f"> 最后更新 (Last Updated): {timestamp}"
    
    # Regex to find existing timestamp (Capture group for replacement)
    # Match > 最后更新 (Last Updated): .* until end of line
    pattern = r"^(> 最后更新 \(Last Updated\):).*$"
    
    if re.search(pattern, content, re.MULTILINE):
        # Update existing
        new_content = re.sub(pattern, ts_line, content, flags=re.MULTILINE)
    else:
        # Insert if missing.
        # Strategy: Insert after @CONTEXT or @TAGS line, or after H1.
        
        # 1. Try after @CONTEXT
        context_pattern = r"^(> @CONTEXT:.*)$"
        if re.search(context_pattern, content, re.MULTILINE):
            new_content = re.sub(context_pattern, f"\\1\n{ts_line}", content, flags=re.MULTILINE)
        else:
            # 2. Try after H1 (# Title)
            h1_pattern = r"^(# .*)$"
            if re.search(h1_pattern, content, re.MULTILINE):
                new_content = re.sub(h1_pattern, f"\\1\n{ts_line}", content, flags=re.MULTILINE)
            else:
                # 3. Just prepend to file
                new_content = f"{ts_line}\n{content}"
    
    return write_text(path, new_content)
