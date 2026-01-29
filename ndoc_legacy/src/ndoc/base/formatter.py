import os
from pathlib import Path

def make_file_link(file_path: Path, root: Path, line: int = None, text: str = None):
    """
    Creates a robust Markdown link for a file.
    
    Args:
        file_path: Absolute path to the file
        root: Project root path
        line: Optional line number
        text: Optional link text. If None, uses "path:line" or "path"
    """
    try:
        rel_path = file_path.relative_to(root)
    except ValueError:
        # If not relative to root, just use name
        rel_path = file_path.name
        
    # Always use forward slashes for Markdown links
    path_str = str(rel_path).replace(os.sep, '/')
    
    # Ensure it starts with ./ for better IDE compatibility if it's not a parent ref
    if not path_str.startswith('./') and not path_str.startswith('../'):
        link_target = f"./{path_str}"
    else:
        link_target = path_str
        
    if line:
        link_target += f"#L{line}"
        default_text = f"{path_str}:{line}"
    else:
        default_text = path_str
        
    link_text = text if text else default_text
    
    return f"[{link_text}]({link_target})"
