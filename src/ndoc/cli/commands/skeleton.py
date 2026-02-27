"""
Command: Skeleton Generator.
"""
from pathlib import Path
from ndoc.core.cli import ndoc_command
from ndoc.core import io
from ndoc.parsing.ast import skeleton

@ndoc_command(name="skeleton", help="Generate semantic skeleton of a file", group="Analysis")
def run(target: str) -> bool:
    """
    Generate skeleton for a specific file.
    """
    if not target:
        print("Error: 'skeleton' command requires a file path (target).")
        return False
        
    path = Path(target)
    if not path.exists():
        print(f"Error: File not found: {path}")
        return False
        
    content = io.read_text(path)
    if content:
        print(skeleton.generate_skeleton(content, str(path)))
        return True
    return False
