"""
Flow: Configuration Loading.
业务流：从 _RULES.md 加载项目配置 (Documentation as Configuration).
"""
import re
from pathlib import Path
from typing import List, Set

from ndoc.models.config import ProjectConfig, ScanConfig
from ndoc.atoms import io

# Default Rules Template
RULES_TEMPLATE = """# Project Rules
> @CONTEXT: Configuration | @TAGS: @CONFIG @RULES

## Scanning Rules (扫描规则)
> 定义哪些文件应该被忽略或包含。

- `!IGNORE`: .git, .vscode, .idea, __pycache__, node_modules, dist, build, .venv, venv
- `!INCLUDE`: .py, .md, .json, .js, .ts, .html, .css, .yml, .yaml, .toml

## Documentation Style (文档风格)
> 定义生成的文档样式。

- `!LANG`: Chinese (zh-CN)

## ALM & Memory Rules (ALM与记忆规则)
> 定义项目生命周期与自动归档规则。

- `MEMORY文档对齐`: 定期更新_MEMORY.md，每当_NEXT.md中一项功能/模块完成，将其归档入_MEMORY.md。
- `交付即更新`: 在完成代码修改后，习惯性运行 `ndoc all`，确保改动被即时索引。
- `语义化文档补完`: 在开发完成后，主动编辑 `_AI.md` 填充设计意图与调用约束，确保文档具有“人类可读的语义”。
- `标签与元数据对齐`: 根据模块引入的新技术栈，动态更新 `_AI.md` 顶部的 `@TAGS`。

## Special Keywords (特殊关键字)
> 用于控制特定目录的文档生成行为。

- `@AGGREGATE`: **Recursive Aggregation**. 当目录包含此标记时，不为子目录生成单独的 `_AI.md`，而是将其内容递归聚合到父级 `_AI.md` 中。
- `@CHECK_IGNORE`: **Audit Ignore**. 当目录包含此标记时，完全跳过该目录及其子目录的 `_AI.md` 生成。
"""

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
        return io.write_text(rules_file, RULES_TEMPLATE)
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
    
    found_ignore = False
    found_include = False
    
    for match in pattern.finditer(content):
        tag = match.group(1)
        args_str = match.group(2).strip()
        
        # Split args by comma
        args = [a.strip() for a in args_str.split(',') if a.strip()]
        
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
            
    # Update Config
    if found_ignore:
        config.scan.ignore_patterns = sorted(list(ignore_set))
        
    if found_include:
        config.scan.extensions = sorted(list(include_set))
        
    # Debug info
    # print(f"  Loaded {len(config.scan.ignore_patterns)} ignore patterns")
    # print(f"  Loaded {len(config.scan.extensions)} extensions")
