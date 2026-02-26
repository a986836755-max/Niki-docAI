# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: `capabilities.py` implements the "Kernel + Plugins" architecture. Do not hardcode...
# *   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
# *   **Enhanced Symbol Context**: `scanner.py` 在重建缓存符号时必须确保 `path` 属性被正确填充，否则会导致下游 CLI 工具 (如 `lsp` 指令) 在解析相对路径时崩溃。
# *   **LSP Service Hotness**: `lsp.py` 提供轻量级引用计数。该计数基于全局词频统计，虽然不是 100% 精确的定义引用，但在大规模 codebase 中能有效反映符号的“热度”和影响力。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: Input/Output Operations.
副作用隔离层：所有磁盘读写必须在此完成。
"""
import os
import re
from pathlib import Path
from typing import List, Optional, Callable, Any, Union
from datetime import datetime
import difflib

# Global Flag for Dry Run
# This is a simple state injection for cross-cutting concern
_DRY_RUN_MODE = False

def set_dry_run(enabled: bool) -> None:
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

def safe_io(operation: Callable[..., Any], error_msg: str, *args: Any, **kwargs: Any) -> Any:
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

def read_head(path: Path, n_bytes: int = 2048) -> Optional[str]:
    """
    读取文件头部内容 (Read file head content).
    Useful for quick scanning without loading huge files.
    """
    if not path.exists():
        return None
        
    def _read():
        with open(path, 'rb') as f:
            chunk = f.read(n_bytes)
            return chunk.decode('utf-8', errors='ignore')
            
    return safe_io(_read, f"Error reading head of {path}: {{e}}")

def write_text(path: Path, content: str) -> bool:
    """
    安全写入文件内容 (Safely write file content).
    If Dry Run is enabled, prints diff instead of writing.
    
    Args:
        path: 文件路径
        content: 写入内容
        
    Returns:
        bool: 是否执行了写入操作
    """
    # 1. Compare-Before-Write (Optimized)
    if path.exists():
        try:
            current_content = path.read_text(encoding='utf-8', errors='ignore')
            # Normalize line endings for comparison if needed, 
            # but usually exact match is preferred.
            if current_content == content:
                return False  # Skip write if content is identical
        except Exception:
            # If read fails, proceed to write (better safe than sorry)
            pass

    if _DRY_RUN_MODE:
        print(f"[DRY-RUN] Would write to {path}")
        # Show simple diff
        if path.exists():
            try:
                old = path.read_text(encoding='utf-8', errors='ignore').splitlines()
                new = content.splitlines()
                diff = difflib.unified_diff(old, new, fromfile=str(path), tofile="new")
                for line in diff:
                    print(line)
            except Exception:
                print("(Cannot generate diff)")
        else:
            print("(New file)")
        return True

    def _write():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return True

    return safe_io(_write, f"Error writing {path}: {{e}}") or False

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
        return False
        
    # Pattern: START_MARKER .* END_MARKER
    # Use re.DOTALL to match newlines
    # Use re.escape only for markers to avoid regex issues
    pattern = re.compile(
        f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})", 
        re.DOTALL
    )
    
    match = pattern.search(content)
    if not match:
        # Markers not found.
        # print(f"⚠️  Markers not found in {path.name}")
        return False
        
    # Construct replacement string
    # We replace group 2 (inner content)
    # We must ensure new_content doesn't contain backslashes that re.sub interprets as escapes
    
    # Using lambda for replacement avoids backslash hell
    def replacer(m):
        return f"{m.group(1)}\n{new_content}\n{m.group(3)}"
        
    updated_content = pattern.sub(replacer, content)
    
    # Only write if changed
    if updated_content != content:
        return write_text(path, updated_content)
    return True

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

def delete_file(path: Path) -> bool:
    """
    安全删除文件 (Safely delete file).
    
    Args:
        path: 文件路径
        
    Returns:
        bool: 是否成功
    """
    if _DRY_RUN_MODE:
        if path.exists():
            print(f"❌ [DryRun] Would delete: {path}")
        return True

    def _delete():
        if path.exists():
            path.unlink()
        return True
    
    return safe_io(_delete, f"Error deleting {path}: {{e}}") is True
