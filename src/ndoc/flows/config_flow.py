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
Flow: Configuration Loading.
业务流：从 _RULES.md 加载项目配置 (Documentation as Configuration).
"""
import re
from pathlib import Path
from typing import List
from datetime import datetime

from ..models.config import ProjectConfig, ScanConfig
from ..core import io
from ..core.templates import get_template, render_document

def load_project_config(root_path: Path) -> ProjectConfig:
    """
    加载项目配置 (Load Project Configuration).
    Priority: _RULES.md > Default
    """
    # 1. Initialize with Defaults
    # We start with the default ScanConfig defined in models/config.py
    # But we want to allow _RULES.md to extend/override.
    
    # Create base config
    scan_config = ScanConfig(root_path=root_path)
    config = ProjectConfig(scan=scan_config, name=root_path.name)
    
    # 2. Load from _RULES.md
    rules_file = root_path / "_RULES.md"
    
    if rules_file.exists():
        print(f"Loading configuration from {rules_file.name}...")
        _parse_rules(rules_file, config)
    else:
        print(f"No {rules_file.name} found. Using default configuration.")
        # Optional: Auto-create? Let's leave that to a separate init step or user action.
        # But for "Documentation as Configuration", maybe we should create it if missing?
        # User asked for "Documentation as Configuration" scheme.
        # Let's create it if it doesn't exist to encourage usage, similar to Syntax Flow?
        # Or maybe just let the user know.
        pass

    return config

def ensure_rules_file(root_path: Path, force: bool = False) -> bool:
    """
    确保 _RULES.md 存在 (Ensure _RULES.md exists).
    :param force: If True, overwrite existing file.
    """
    rules_file = root_path / "_RULES.md"
    if force or not rules_file.exists():
        if force:
             print(f"Restoring default Rules Configuration at {rules_file.name}...")
        else:
             print(f"Creating default Rules Configuration at {rules_file.name}...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = render_document(
            "rules.md.tpl",
            title="Project Rules",
            context="Configuration | @TAGS: @CONFIG @RULES",
            tags="",
            timestamp=timestamp
        )
        return io.write_text(rules_file, content)
    return False

def ensure_guide_file(root_path: Path, force: bool = False) -> bool:
    """
    确保 _GUIDE.md 存在 (Ensure _GUIDE.md exists).
    This file instructs AI how to use Niki-docAI tools.
    """
    guide_file = root_path / "_GUIDE.md"
    if force or not guide_file.exists():
        if force:
             print(f"Updating AI Guide at {guide_file.name}...")
        else:
             print(f"Creating AI Guide at {guide_file.name}...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = render_document(
            "guide.md.tpl",
            title="AI Context Guide (Niki-docAI)",
            context="Guide | Instructions",
            tags="",
            timestamp=timestamp
        )
        return io.write_text(guide_file, content)
    return False

def _parse_rules(file_path: Path, config: ProjectConfig) -> None:
    """
    解析规则文件并更新配置对象 (Parse rules file and update config).
    """
    content = io.read_text(file_path)
    if not content:
        return

    # Parsing Logic:
    # Look for list items with tags: - `!TAG`: args...
    # Support - or * bullet.
    # Support `!TAG`, **!TAG**, or !TAG.
    
    # Regex breakdown:
    # ^\s*[-*]\s*          : Line start, bullet (- or *)
    # (?:[`'\"*]{1,2})?    : Optional wrapper (`, ", ', **, *) - non-capturing
    # (![A-Z_]+)           : TAG (Group 1)
    # (?:[`'\"*]{1,2})?    : Optional wrapper close
    # \s*:\s*              : Separator
    # (.*)$                : Args (Group 2)
    pattern = re.compile(r"^\s*[-*]\s*(?:[`'\"*]{1,2})?(![A-Z_]+)(?:[`'\"*]{1,2})?\s*:\s*(.*)$", re.MULTILINE)
    
    ignore_set = set(config.scan.ignore_patterns)
    include_set = set(config.scan.extensions)
    lint_cmds: List[str] = list(config.lint_commands)
    typecheck_cmds: List[str] = list(config.typecheck_commands)
    
    found_ignore = False
    found_include = False
    found_lint = False
    found_typecheck = False

    def _parse_command_list(raw: str) -> List[str]:
        return [part.strip() for part in raw.split(";") if part.strip()]
    
    for match in pattern.finditer(content):
        tag = match.group(1)
        args_str = match.group(2).strip()
        
        # Split args by comma
        args = [a.strip().rstrip('/') for a in args_str.split(',') if a.strip()]
        
        if tag == "!IGNORE":
            if not found_ignore:
                # If user defines ignore, should we replace defaults or append?
                # Usually configuration implies "this is the list". 
                # But defaults like .git are rarely removed.
                # Let's adopt "Append/Extend" strategy if it's the first time we see it in file?
                # Or maybe "Replace" is cleaner for "Configuration".
                # Let's go with: If !IGNORE is present, we start with a clean slate (except maybe critical ones?)
                # Actually, safest is to Add to defaults. If user wants to un-ignore, that's harder.
                # Let's use Union for now.
                pass
            ignore_set.update(args)
            found_ignore = True
            
        elif tag == "!INCLUDE":
            # If user specifies extensions, usually they want ONLY these.
            if not found_include:
                 # If this is the first include tag, clear default empty (which means all)
                 # But wait, config.scan.extensions default is empty list (all).
                 pass
            include_set.update(args)
            found_include = True
        elif tag == "!LINT":
            lint_cmds = _parse_command_list(args_str)
            found_lint = True
        elif tag == "!TYPECHECK":
            typecheck_cmds = _parse_command_list(args_str)
            found_typecheck = True
        
        # Template Configuration
        elif tag == "!TEMPLATE_DIR":
            # !TEMPLATE_DIR: .ndoc/templates
            if args:
                path_str = args[0]
                # Resolve relative to project root
                resolved = (config.scan.root_path / path_str).resolve()
                if resolved.exists() and resolved.is_dir():
                    config.template.base_dir = resolved
                else:
                    print(f"Warning: Template directory {path_str} not found.")

        elif tag == "!TEMPLATE_HEADER":
            if args:
                config.template.header = args[0]

        elif tag == "!TEMPLATE_FOOTER":
            if args:
                config.template.footer = args[0]

        elif tag == "!TEMPLATE_OVERRIDE":
            # !TEMPLATE_OVERRIDE: ai.md.tpl=custom_ai.tpl, header.py.tpl=custom_header.tpl
            for arg in args:
                if "=" in arg:
                    key, val = arg.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    # Resolve val relative to root or template dir? 
                    # Let's assume relative to root if it looks like a path, or just a name?
                    # If base_dir is set, maybe relative to that?
                    # For flexibility, let's treat it as a path relative to root.
                    resolved_val = (config.scan.root_path / val).resolve()
                    config.template.overrides[key] = resolved_val
            
    # Update Config
    if found_ignore:
        config.scan.ignore_patterns = sorted(list(ignore_set))
        
    if found_include:
        config.scan.extensions = sorted(list(include_set))
        
    if found_lint:
        config.lint_commands = lint_cmds
        
    if found_typecheck:
        config.typecheck_commands = typecheck_cmds
        
    # Debug info
    # print(f"  Loaded {len(config.scan.ignore_patterns)} ignore patterns")
    # print(f"  Loaded {len(config.scan.extensions)} extensions")
