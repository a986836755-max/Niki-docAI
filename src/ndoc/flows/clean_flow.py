"""
Flow: Clean / Reset.
业务流：清理/重置生成的文档 (Clean/Reset Generated Docs).
"""
import os
from pathlib import Path
from typing import List, Optional
from ndoc.models.config import ProjectConfig

# List of auto-generated filenames to clean
GENERATED_FILES = [
    "_AI.md",
    "_MAP.md",
    "_TECH.md",
    "_DEPS.md",
    "_NEXT.md",
    # _ARCH.md is typically manual or hybrid, avoiding delete for safety unless confirmed
]

def run(config: ProjectConfig, target: str = None, force: bool = False) -> bool:
    """
    Execute Clean Flow.
    :param config: Project Configuration
    :param target: Optional target path (file or directory). If None, cleans project root artifacts and recursive _AI.md.
    :param force: If True, bypass confirmation.
    """
    root_path = config.scan.root_path
    target_path = Path(target).resolve() if target else root_path

    # Security check: Ensure target is within project root
    try:
        target_path.relative_to(root_path)
    except ValueError:
        print(f"❌ Error: Target '{target}' is outside project root.")
        return False

    files_to_delete: List[Path] = []

    if target_path.is_file():
        # Case 1: Target is a specific file
        if target_path.name in GENERATED_FILES or target_path.name.endswith(".md"): # Allow deleting any md if explicitly targeted?
             # Safer: Only delete if it looks like our artifact or user explicitly asks
             # For "reset specific document", we trust the user's path.
             files_to_delete.append(target_path)
    elif target_path.is_dir():
        # Case 2: Target is a directory
        # If root, we look for global artifacts AND recursive _AI.md
        # If subdir, we look for artifacts in that dir AND recursive _AI.md
        
        print(f"Scanning for artifacts in {target_path}...")
        
        # 1. Look for top-level artifacts in this dir
        for fname in GENERATED_FILES:
            f = target_path / fname
            if f.exists():
                files_to_delete.append(f)
        
        # 2. Look for recursive _AI.md in subdirectories
        # Using rglob for _AI.md
        for p in target_path.rglob("_AI.md"):
            if p not in files_to_delete:
                files_to_delete.append(p)
                
    if not files_to_delete:
        print(f"✨ No generated artifacts found in {target_path}")
        return True

    print(f"Found {len(files_to_delete)} files to delete:")
    for f in files_to_delete[:10]:
        print(f"  - {f.relative_to(root_path)}")
    if len(files_to_delete) > 10:
        print(f"  ... and {len(files_to_delete) - 10} more")

    if not force:
        confirm = input("⚠️  Are you sure you want to delete these files? [y/N] ").strip().lower()
        if confirm != 'y':
            print("❌ Operation cancelled.")
            return False

    deleted_count = 0
    for f in files_to_delete:
        try:
            os.remove(f)
            deleted_count += 1
            # print(f"Deleted {f.name}")
        except Exception as e:
            print(f"❌ Failed to delete {f}: {e}")

    print(f"✅ Successfully cleaned {deleted_count} files.")
    return True
