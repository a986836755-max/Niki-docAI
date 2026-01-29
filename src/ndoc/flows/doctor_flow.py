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

from ndoc.models.config import ProjectConfig

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
        ("tree_sitter_python", "Tree-sitter Python Grammar"),
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
        from tree_sitter import Language, Parser
        import tree_sitter_python
        
        # Try to initialize
        PY_LANGUAGE = Language(tree_sitter_python.language())
        parser = Parser(PY_LANGUAGE)
        
        _pass("Tree-sitter bindings working")
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
