"""
Command: Doctor.
"""
import sys
import importlib
import platform
import shutil
from pathlib import Path
from ndoc.models.config import ProjectConfig
from ndoc.core.cli import ndoc_command
from ndoc.core.logger import logger

@ndoc_command(name="doctor", help="Diagnose environment and configuration health", group="Diagnostics")
def run(config: ProjectConfig) -> bool:
    """
    Run Environment Diagnostic.
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

    # 4. Check Project Config
    _check_project_files(config)
    
    print("==================================================")
    if all_passed:
        print("✅ System is ready for Niki-docAI.")
        print("\n💡 Recommended Workflows:")
        print("   - Refresh All Docs:    ndoc all")
        print("   - Check Architecture:  ndoc check")
        print("   - Semantic Context:    ndoc prompt <file> --focus")
        print("   - Search Codebase:     ndoc search \"query\"")
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
