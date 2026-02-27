# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **RULE**: @LAYER(core) CANNOT_IMPORT @LAYER(ui) --> [context_flow.py:198](context_flow.py#L198)
# *   **RULE**: @FORBID(hardcoded_paths) --> [context_flow.py:199](context_flow.py#L199)
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Self-Update Flow.
更新流：自我更新流程。
"""
import subprocess
import sys
from pathlib import Path
from typing import Optional
from ..core import fs
from ..core.logger import logger
from ..core.cli import ndoc_command

def _is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()

def run() -> bool:
    """
    Execute self-update via git pull.
    """
    # Determine source root
    # This file is in src/ndoc/flows/update_flow.py
    # Root is ../../../
    current_file = Path(__file__).resolve()
    src_root = current_file.parent.parent.parent
    repo_root = src_root.parent
    
    # Verify it is a git repo
    if not _is_git_repo(repo_root):
        # Fallback: maybe src_root is the repo root? (unlikely structure but check)
        if _is_git_repo(src_root):
            repo_root = src_root
        else:
            print(f"❌ Not a git repository (checked {repo_root}). Cannot self-update.")
            print("ℹ️  Please update manually via 'git pull' or 'pip install -U'.")
            return False
            
    print(f"🔄 Updating Niki-docAI from {repo_root}...")
    
    try:
        # Check for local changes first to warn user
        status = subprocess.run(["git", "status", "--porcelain"], cwd=repo_root, capture_output=True, text=True)
        if status.stdout.strip():
            print("⚠️  Warning: You have uncommitted changes.")
            # We continue, as git pull might merge or autostash if configured, 
            # but usually it will fail if conflict. Let git handle it.
            
        # Execute git pull
        result = subprocess.run(["git", "pull"], cwd=repo_root, text=True)
        
        if result.returncode == 0:
            print("✅ Code updated successfully.")
            
            # Check if dependencies might need update (simple heuristic)
            # We don't run pip automatically to avoid permission issues or breaking venv, 
            # but we can advise.
            print("ℹ️  If dependencies changed, run: pip install -e .")
            return True
        else:
            print("❌ Update failed.")
            return False
            
    except Exception as e:
        print(f"❌ Error during update: {e}")
        return False
