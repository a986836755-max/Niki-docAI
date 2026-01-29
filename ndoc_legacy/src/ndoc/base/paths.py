import os
from pathlib import Path

def get_project_root():
    """Returns the project root directory by searching upwards for markers."""
    cwd = Path.cwd()
    
    # Markers that identify the project root
    markers = ["pyproject.toml", "_RULES.md", ".git"]
    
    # Check current directory and parents
    for path in [cwd] + list(cwd.parents):
        for marker in markers:
            if (path / marker).exists():
                return path
                
    # Fallback to CWD if nothing found (e.g. fresh init)
    return cwd

def ensure_directory(path):
    """Ensures a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)
