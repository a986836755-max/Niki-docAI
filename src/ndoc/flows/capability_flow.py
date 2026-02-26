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
Flow: Capability Auto-Discovery and Installation.
业务流：自动检测项目语言并安装所需能力 (Auto-Install Capabilities).
"""
from typing import Set
from pathlib import Path
from ..core import fs, capabilities
from ..parsing import langs
from ..models.config import ProjectConfig
from ..core.cli import ndoc_command

@ndoc_command(name="caps", help="Manage project capabilities", group="Core")
def run(config: ProjectConfig, auto_install: bool = True) -> bool:
    """
    Scan project for file extensions and ensure corresponding languages are installed.
    """
    print(f"Scanning project capabilities in {config.scan.root_path}...")
    
    # 1. Collect all extensions in the project
    extensions: Set[str] = set()
    
    # Use existing walk_files with default ignore patterns
    files = fs.walk_files(config.scan.root_path, config.scan.ignore_patterns)
    
    for file_path in files:
        ext = file_path.suffix.lower()
        if ext:
            extensions.add(ext)
            
    # 2. Map extensions to languages
    required_languages: Set[str] = set()
    for ext in extensions:
        lang_id = langs.get_lang_id_by_ext(ext)
        if lang_id:
            required_languages.add(lang_id)
            
    if not required_languages:
        print("ℹ️  No supported languages detected.")
        return True
        
    # 3. Ensure capabilities are installed
    # This will trigger batch installation if needed
    capabilities.CapabilityManager.ensure_languages(required_languages, auto_install=auto_install)
    
    # 4. Ensure optional packages (like chromadb) are installed if needed
    # We can check config or just try to install if missing
    # For now, let's proactively ensure chromadb if user wants full features
    if auto_install:
        capabilities.CapabilityManager.ensure_package("chromadb", auto_install=True)
    
    return True

def check_single_file(file_path: Path, auto_install: bool = True):
    """
    Check capability for a single file (used in Watch mode).
    """
    ext = file_path.suffix.lower()
    lang_id = langs.get_lang_id_by_ext(ext)
    
    if lang_id:
        capabilities.CapabilityManager.ensure_languages({lang_id}, auto_install=auto_install)
