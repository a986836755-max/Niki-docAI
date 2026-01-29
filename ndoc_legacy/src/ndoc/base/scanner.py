import os
from pathlib import Path
from ndoc.core import config

def get_ignore_dirs():
    """Returns a set of directories to ignore."""
    # Combine config ignores with standard ignores
    return set(config.IGNORE_DIRS).union({'.git', '__pycache__', 'venv', 'node_modules', '.idea', '.vscode'})

def walk_project_dirs(root: Path):
    """
    Generator that yields directory paths in the project, respecting ignore rules.
    """
    ignore_dirs = get_ignore_dirs()
    
    for current_root, dirs, files in os.walk(root):
        # Filter ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        yield Path(current_root)

def walk_project_files(root: Path, extensions=None):
    """
    Generator that yields file paths in the project, respecting ignore rules.
    
    Args:
        root: Project root Path
        extensions: Optional list/tuple of extensions to include (e.g., ('.py', '.md'))
    """
    ignore_dirs = get_ignore_dirs()
    
    for current_root, dirs, files in os.walk(root):
        # Filter ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        for file in files:
            # Skip common junk files
            if file.startswith('.'):
                continue
            
            # Skip specific files
            if file.endswith('.pyc'):
                continue

            if extensions:
                if isinstance(extensions, (list, tuple)):
                    if not file.endswith(tuple(extensions)):
                        continue
                elif not file.endswith(extensions):
                    continue
                
            yield Path(current_root) / file
