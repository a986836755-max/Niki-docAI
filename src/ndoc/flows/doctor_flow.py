# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: New flows (like `capability_flow.py`) must be registered in `entry.py` to ensure ...
# *   **Auto-Provisioning**: `capability_flow` acts as the project's "immune system", proactively detecting and install...
# *   **Doctor Integration**: `doctor_flow` should reuse the `CapabilityManager` logic to verify system health, rather ...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: System Diagnostics.
业务流：环境诊断 (Environment Doctor).
"""
import sys
import importlib
import platform
import shutil
from pathlib import Path
from typing import List, Tuple

from ..models.config import ProjectConfig
from ..core import capabilities
from ..core.capabilities import CapabilityManager
from ..parsing import langs

def run(config: ProjectConfig) -> bool:
    """
    运行环境诊断 (Run Environment Diagnostic).
    """
    print(f"\n🩺 Niki-docAI Doctor (v2.0.0)")
    print("==================================================")
    
    all_passed = True
    
    # 1. System Info
    print(f"OS: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    
    # 2. Check Python Version
    if sys.version_info < (3, 9):
        _fail("Python version < 3.9")
        all_passed = False
    else:
        _pass("Python version >= 3.9")

    # 3. Check Dependencies
    dependencies = [
        ("watchdog", "Watchdog (File Monitor)"),
        ("tree_sitter", "Tree-sitter (Parser Core)"),
        ("colorama", "Colorama (Terminal Color)"),
    ]
    
    for module_name, display_name in dependencies:
        if _check_import(module_name):
            _pass(f"{display_name} installed")
        else:
            _fail(f"{display_name} NOT found")
            all_passed = False

    # 4. Check Tree-sitter Functionality
    if not _check_tree_sitter_bindings():
        all_passed = False

    # 5. Check CLI Tools (Optional)
    # git is useful
    if shutil.which("git"):
        _pass("Git CLI found")
    else:
        _warn("Git CLI not found (Version control features disabled)")

    # 6. Check Project Config
    _check_project_files(config)

    print("==================================================")
    if all_passed:
        print("✅ System is ready for Niki-docAI.")
        return True
    else:
        print("❌ System has issues. Please fix errors above.")
        return False

def _pass(msg: str):
    print(f"  [OK] {msg}")

def _fail(msg: str):
    print(f"  [FAIL] {msg}")

def _warn(msg: str):
    print(f"  [WARN] {msg}")

def _check_import(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def _check_tree_sitter_bindings() -> bool:
    try:
        from tree_sitter import Parser
        
        print("  [INFO] Checking Tree-sitter capability mechanism...")
        
        # 1. Check Python binding as baseline smoke test (ensure core mechanism works)
        # We try to install Python binding if missing because it's the host language
        py_lang = CapabilityManager.get_language('python', auto_install=True)
        if not py_lang:
            _fail("Tree-sitter Python binding failed (Core mechanism issue)")
            return False
            
        parser = Parser(py_lang)
        _pass("Core binding (Python) verified")
        
        # 2. Check other registered languages
        installed = []
        missing = []
        
        for lang_name in sorted(CapabilityManager.LANGUAGE_PACKAGES.keys()):
            if lang_name == 'python': continue
            
            l = CapabilityManager.get_language(lang_name, auto_install=False)
            if l:
                installed.append(lang_name)
            else:
                missing.append(lang_name)
                
        if installed:
            print(f"  [OK] Installed languages: {', '.join(installed)}")
        
        if missing:
            print(f"  [INFO] Available (Not Installed): {', '.join(missing)}")
            
        return True
    except Exception as e:
        _fail(f"Tree-sitter binding error: {e}")
        return False

def _check_project_files(config: ProjectConfig):
    root = config.scan.root_path
    print(f"\nProject Check ({root.name}):")
    
    # Check _RULES.md
    if (root / "_RULES.md").exists():
        _pass("_RULES.md found")
    else:
        _warn("_RULES.md missing (Will use defaults)")

    # Check _SYNTAX.md
    if (root / "_SYNTAX.md").exists():
        _pass("_SYNTAX.md found")
    else:
        _warn("_SYNTAX.md missing (Run 'ndoc all' to generate)")
