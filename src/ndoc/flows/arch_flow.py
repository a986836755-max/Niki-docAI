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
Flow: Architecture Overview Generation.
业务流：生成项目架构全景图 (_ARCH.md)。
合并原有的 Map, Deps, Tech Flow。
"""
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict

from ..core import fs, io
from ..core.logger import logger
from ..parsing import scanner, deps
from ..models.config import ProjectConfig
from . import deps_flow

# --- Imports from new Refactored Modules ---
from ..parsing.deps import builder
from ..core import graph as graph_algo
from ..views import mermaid, reports
from ..core.cli import ndoc_command
from ..core.templates import render_document

# --- MAP LOGIC ---

def format_dir_entry(name: str, level: int) -> str:
    indent = "    " * level
    return f"{indent}*   **{name}/**"

def format_file_entry(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str:
    indent = "    " * level
    name = path.name
    try:
        rel_path = path.relative_to(root).as_posix()
    except ValueError:
        rel_path = name
    
    summary = ""
    if summary_cache and path in summary_cache:
        raw_summary = summary_cache[path]
        if raw_summary:
            if len(raw_summary) > 50:
                raw_summary = raw_summary[:47] + "..."
            summary = f" - *{raw_summary}*"
    
    return f"{indent}*   [`{name}`]({rel_path}#L1){summary}"

def extract_file_summary(path: Path) -> str:
    try:
        content = io.read_head(path, 4096)
        if content:
            docstring = scanner.extract_docstring(content)
            return scanner.extract_summary(content, docstring) or ""
    except Exception:
        pass
    return ""

def build_tree_lines(current_path: Path, root: Path, ignore_patterns: List[str], level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]:
    lines = []
    filter_config = fs.FileFilter(ignore_patterns=set(ignore_patterns))
    entries = fs.list_dir(current_path, filter_config, root=root)

    for entry in entries:
        if entry.is_dir():
            lines.append(format_dir_entry(entry.name, level))
            if level < 3: # Limit depth for Arch view
                lines.extend(build_tree_lines(entry, root, ignore_patterns, level + 1, summary_cache))
        else:
            lines.append(format_file_entry(entry, root, level, summary_cache))
            
    return lines

# --- DEPS LOGIC ---

# (Delegated to deps_flow)

# --- TECH LOGIC ---

def generate_bom_section(root: Path, ignore_patterns: List[str]) -> str:
    """
    Generate Bill of Materials (BOM) section for _DEPS.md.
    Focus on manifest files (requirements.txt, package.json, etc.)
    """
    lines = []
    # Use deps.core to parse manifests
    # We want to specifically look for manifest files
    
    # 1. Python (requirements.txt, pyproject.toml)
    py_deps = []
    for f in fs.walk_files(root, ignore_patterns):
        if f.name == "requirements.txt":
            py_deps.extend(deps.core.parse_requirements_txt(f))
        elif f.name == "pyproject.toml":
            py_deps.extend(deps.core.parse_pyproject_toml(f))
    
    if py_deps:
        lines.append("### 🐍 Python (Pip)")
        # Deduplicate
        py_deps = sorted(list(set(py_deps)))
        for dep in py_deps:
            lines.append(f"*   `{dep}`")
        lines.append("")

    # 2. Node.js (package.json)
    js_deps = []
    for f in fs.walk_files(root, ignore_patterns):
        if f.name == "package.json":
            js_deps.extend(deps.core.parse_package_json(f))
            
    if js_deps:
        lines.append("### 📦 Node.js (NPM)")
        js_deps = sorted(list(set(js_deps)))
        for dep in js_deps:
            lines.append(f"*   `{dep}`")
        lines.append("")

    # 3. Dart (pubspec.yaml)
    dart_deps = []
    for f in fs.walk_files(root, ignore_patterns):
        if f.name == "pubspec.yaml":
            dart_deps.extend(deps.core.parse_pubspec_yaml(f))
            
    if dart_deps:
        lines.append("### 🎯 Dart (Pub)")
        dart_deps = sorted(list(set(dart_deps)))
        for dep in dart_deps:
            lines.append(f"*   `{dep}`")
        lines.append("")

    # 4. C# (csproj)
    cs_deps = []
    for f in fs.walk_files(root, ignore_patterns):
        if f.suffix.lower() == ".csproj":
            cs_deps.extend(deps.core.parse_csproj(f))

    if cs_deps:
        lines.append("### 🔷 C# (NuGet)")
        cs_deps = sorted(list(set(cs_deps)))
        for dep in cs_deps:
            lines.append(f"*   `{dep}`")
        lines.append("")

    # 5. Go (go.mod)
    go_deps = []
    for f in fs.walk_files(root, ignore_patterns):
        if f.name == "go.mod":
            go_deps.extend(deps.core.parse_go_mod(f))
            
    if go_deps:
        lines.append("### 🐹 Go (Go Modules)")
        go_deps = sorted(list(set(go_deps)))
        for dep in go_deps:
            lines.append(f"*   `{dep}`")
        lines.append("")

    # 6. Rust (Cargo.toml)
    rust_deps = []
    for f in fs.walk_files(root, ignore_patterns):
        if f.name == "Cargo.toml":
            rust_deps.extend(deps.core.parse_cargo_toml(f))
            
    if rust_deps:
        lines.append("### 🦀 Rust (Cargo)")
        rust_deps = sorted(list(set(rust_deps)))
        for dep in rust_deps:
            lines.append(f"*   `{dep}`")
        lines.append("")
        
    if not lines:
        lines.append("*   *(No third-party dependencies detected)*")
        
    return "\n".join(lines)

def generate_tech_section(root: Path, ignore_patterns: List[str]) -> str:
    lines = []
    lines.append("### 1. Languages")
    languages = deps.stats.detect_languages(root, set(ignore_patterns))
    if not languages:
        lines.append("*   *(No recognizable code files found)*")
    else:
        for lang, pct in languages.items():
            bar_len = int(pct / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f"*   **{lang}**: `{bar}` {pct}%")
            
    lines.append("")
    # Dependencies moved to _DEPS.md
    return "\n".join(lines)

# --- MAIN FLOW ---

@ndoc_command(name="arch", help="Generate Architecture Overview (_ARCH.md)", group="Granular")
def run(config: ProjectConfig) -> bool:
    """Execute Arch Flow"""
    root = config.scan.root_path
    
    logger.info(f"Generating Architecture Overview in {root}...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Tech Stack & BOM -> _ARCH.md
    tech_content = generate_tech_section(root, config.scan.ignore_patterns)
    bom_content = generate_bom_section(root, config.scan.ignore_patterns)
    
    arch_file = root / "_ARCH.md"
    
    arch_content = render_document(
        "arch.md.tpl",
        title="Project Architecture",
        context="Architecture | Space View",
        tags="",
        timestamp=timestamp,
        tech_content=tech_content,
        bom_content=bom_content
    )
    io.write_text(arch_file, arch_content)
    logger.info(f"✅ Architecture Overview updated: {arch_file.name}")
    
    # 2. File Map -> Handled by map_flow.py separately
    
    # 3. Dependencies -> _DEPS.md (Delegated to deps_flow)
    # This ensures consistency between 'ndoc deps' and 'ndoc arch'
    logger.info(f"Generating Dependency Graph (Delegating to deps_flow)...")
    deps_flow.run(config)

    return True
