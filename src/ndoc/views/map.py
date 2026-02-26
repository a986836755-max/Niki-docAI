"""
View: Map Rendering.
视图层：项目结构树渲染。
"""
from pathlib import Path
from typing import Dict

def format_dir_entry(name: str, level: int) -> str:
    """Format directory entry: * **name/**"""
    indent = "    " * level
    return f"{indent}*   **{name}/**"

def format_file_entry(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str:
    """
    Format file entry: * [`name`](path#L1) - summary
    Uses provided summary cache or skips summary extraction.
    """
    indent = "    " * level
    name = path.name
    
    # Calculate relative path for link
    try:
        rel_path = path.relative_to(root).as_posix()
    except ValueError:
        rel_path = name # Fallback
    
    summary = ""
    if summary_cache and path in summary_cache:
        raw_summary = summary_cache[path]
        if raw_summary:
            # Truncate if too long
            if len(raw_summary) > 50:
                raw_summary = raw_summary[:47] + "..."
            summary = f" - *{raw_summary}*"
    
    # Link with #L1
    return f"{indent}*   [`{name}`]({rel_path}#L1){summary}"
