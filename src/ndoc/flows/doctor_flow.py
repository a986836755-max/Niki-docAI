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
from ..parsing.deps import stats
from ..core.cli import ndoc_command
from ..core.templates import get_template

@ndoc_command(name="doctor", help="Diagnose environment and configuration health", group="Diagnostics")
def run(config: ProjectConfig) -> bool:
    """
    运行环境诊断 (Run Environment Diagnostic).
    """
    template = get_template("doctor_report.tpl")
    
    # Capture logs for template
    tree_sitter_logs = []
    project_checks = []
    
    # ... (Logic to fill logs) ...
    # This refactoring is complex because print() calls are scattered.
    # For now, we keep logic but use template for structured output if feasible.
    # Actually, the original code prints incrementally which is better for CLI feedback.
    # Maybe we just template the "Recommended Workflows" part?
    
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
    # Scan project languages first
    print(f"  [INFO] Scanning project for required languages...")
    project_langs = stats.detect_languages(config.scan.root_path, config.scan.ignore_patterns)
    required_langs = set(project_langs.keys())
    
    if not _check_tree_sitter_bindings(required_langs):
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
        print("\n💡 Recommended Workflows (推荐工作流):")
        print("   - Refresh All Docs:    ndoc all")
        print("   - Check Architecture:  ndoc check")
        print("   - Analyze Deps:        ndoc deps")
        print("   - Semantic Context:    ndoc prompt <file> --focus")
        print("   - Search Codebase:     ndoc search \"query\"")
        print("   - Quality Checks:      ndoc lint / typecheck")
        return True
    else:
        print("❌ System has issues. Please fix errors above.")
        return False

from ..core.logger import logger

def _pass(msg: str):
    logger.info(f"  [OK] {msg}")

def _fail(msg: str):
    logger.error(f"  [FAIL] {msg}")

def _warn(msg: str):
    logger.warning(f"  [WARN] {msg}")

def _check_import(module_name: str) -> bool:
    capabilities.CapabilityManager._init_local_lib()
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def _check_tree_sitter_bindings(required_langs: set = None) -> bool:
    if required_langs is None:
        required_langs = set()
        
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
        errors = []
        
        for lang_name in sorted(CapabilityManager.LANGUAGE_PACKAGES.keys()):
            if lang_name == 'python': continue
            
            # Check if language is required by project
            is_required = lang_name in required_langs
            
            # If required, allow interaction (check_only=False)
            # If not required, silent check (check_only=True)
            # Note: For doctor flow, we might want to check existing installation status first
            # but here we rely on get_language to handle loading
            
            try:
                # If required, force a load check
                check_only = not is_required
                l = CapabilityManager.get_language(lang_name, auto_install=False, check_only=check_only)
                
                if l:
                    installed.append(lang_name)
                    # Runtime Parsing Check (Smoke Test)
                    if is_required:
                        p = Parser(l)
                        p.parse(b"") # Dummy parse
                        _pass(f"Language '{lang_name}' verified (Load + Parse)")
                else:
                    if is_required:
                        missing.append(lang_name)
                        _warn(f"Required language '{lang_name}' is missing.")
            except Exception as e:
                errors.append(f"{lang_name}: {e}")
                if is_required:
                    _fail(f"Language '{lang_name}' failed to load: {e}")
                
        if installed:
            print(f"  [OK] Installed languages: {', '.join(installed)}")
        
        if missing:
            print(f"  [WARN] Missing required languages: {', '.join(missing)}")
            
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
