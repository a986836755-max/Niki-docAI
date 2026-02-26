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

# DEPRECATED: analyze_dependencies is now delegated to deps_flow.py
# The following functions (analyze_dependencies, calculate_metrics, generate_instability_table, 
# generate_dependency_matrix, build_dependency_report) are kept for compatibility if needed 
# but arch_flow should use deps_flow.

def build_dependency_report(root: Path, config: ProjectConfig) -> str:
    """
    Delegate dependency reporting to deps_flow.
    """
    # 1. Collect Imports (Enhanced)
    import_map = deps_flow.collect_imports(root, config)
    
    # 2. Build Graph (Enhanced)
    graph = deps_flow.build_dependency_graph(import_map)
    
    # 3. Calculate Metrics (Local implementation for now, or move to deps_flow?)
    # Let's use local metric calculation but on the better graph.
    # Note: graph keys are file paths now, not modules.
    # We need to aggregate file graph to module graph for Arch View.
    
    module_graph = defaultdict(set)
    
    for src_file, targets in graph.items():
        src_mod = _get_module_name(Path(src_file))
        if not src_mod: continue
        
        for tgt_file in targets:
            tgt_mod = _get_module_name(Path(tgt_file))
            if tgt_mod and tgt_mod != src_mod:
                module_graph[src_mod].add(tgt_mod)
                
    metrics = calculate_metrics(module_graph)
    
    # 4. Table
    table = generate_instability_table(metrics)
    
    # 5. Graph (Mermaid)
    # Layered by I value
    stable = [m for m, v in metrics.items() if v["i"] < 0.3]
    hub = [m for m, v in metrics.items() if 0.3 <= v["i"] <= 0.7]
    volatile = [m for m, v in metrics.items() if v["i"] > 0.7]
    
    graph_lines = ["graph TD"]
    # Styles
    graph_lines.append("    classDef stable fill:#2ecc71,stroke:#27ae60,color:white;")
    graph_lines.append("    classDef hub fill:#f1c40f,stroke:#f39c12,color:black;")
    graph_lines.append("    classDef volatile fill:#e74c3c,stroke:#c0392b,color:white;")
    
    # Subgraphs
    if volatile:
        graph_lines.append('    subgraph "Volatile Zone (I > 0.7)"')
        for m in volatile:
            graph_lines.append(f"        {m.replace('.', '_')}['{m}']:::volatile")
        graph_lines.append("    end")
        
    if hub:
        graph_lines.append('    subgraph "Hub Zone (0.3 < I < 0.7)"')
        for m in hub:
            graph_lines.append(f"        {m.replace('.', '_')}['{m}']:::hub")
        graph_lines.append("    end")
        
    if stable:
        graph_lines.append('    subgraph "Stable Zone (I < 0.3)"')
        for m in stable:
            graph_lines.append(f"        {m.replace('.', '_')}['{m}']:::stable")
        graph_lines.append("    end")
        
    # Edges
    for src, targets in module_graph.items():
        for dst in targets:
            graph_lines.append(f"    {src.replace('.', '_')} --> {dst.replace('.', '_')}")
            
    mermaid = "\n".join(graph_lines)
    
    # 6. Matrix
    sorted_modules = sorted(metrics.keys())
    matrix = generate_dependency_matrix(module_graph, sorted_modules)
    
    return f"""## 1. Instability Metrics
{table}

## 2. Layered Topology
```mermaid
{mermaid}
```

## 3. Dependency Matrix
{matrix}
"""

def _get_module_name(path: Path) -> str:
    """Helper to convert file path to module name."""
    try:
        # Remove src/ prefix if exists
        parts = path.parts
        if parts[0] == "src":
            parts = parts[1:]
            
        if len(parts) > 1:
            # ndoc/core/fs.py -> ndoc.core
            return ".".join(parts[:2])
        else:
            # root_file.py -> root_file
            return parts[0].rsplit('.', 1)[0]
    except Exception:
        return ""

def calculate_metrics(graph: Dict[str, Set[str]]) -> Dict[str, Dict[str, float]]:
    """
    Calculate Ca, Ce, Instability (I).
    """
    metrics = defaultdict(lambda: {"ca": 0, "ce": 0, "i": 0.0})
    all_modules = set(graph.keys()) | set(t for targets in graph.values() for t in targets)
    
    for module in all_modules:
        # Ce: Efferent Coupling (Outgoing)
        ce = len(graph.get(module, []))
        metrics[module]["ce"] = ce
        
        # Ca: Afferent Coupling (Incoming)
        ca = 0
        for other, targets in graph.items():
            if module in targets:
                ca += 1
        metrics[module]["ca"] = ca
        
        # I: Instability = Ce / (Ca + Ce)
        if ca + ce > 0:
            metrics[module]["i"] = round(ce / (ca + ce), 2)
        else:
            metrics[module]["i"] = 0.0 # Isolated
            
    return metrics

def generate_instability_table(metrics: Dict[str, Dict[str, float]]) -> str:
    lines = []
    lines.append("| Module | Ca (In) | Ce (Out) | Instability (I) | Role |")
    lines.append("| :--- | :---: | :---: | :---: | :--- |")
    
    # Sort by Instability (Stable to Volatile)
    sorted_modules = sorted(metrics.items(), key=lambda x: x[1]["i"])
    
    for module, m in sorted_modules:
        i = m["i"]
        role = ""
        if i < 0.3:
            role = "Foundation" # Core
        elif i > 0.7:
            role = "Volatile" # Logic/UI
        else:
            role = "Hub" # Middle
            
        lines.append(f"| `{module}` | {m['ca']} | {m['ce']} | **{i:.2f}** | {role} |")
        
    return "\n".join(lines)

def generate_dependency_matrix(graph: Dict[str, Set[str]], modules: List[str]) -> str:
    lines = []
    # Header
    headers = [m.split('.')[-1] for m in modules]
    lines.append("| From \\ To | " + " | ".join(headers) + " |")
    lines.append("| :--- | " + " | ".join([":---:" for _ in modules]) + " |")
    
    for src in modules:
        row = [f"**{src.split('.')[-1]}**"]
        for dst in modules:
            if src == dst:
                row.append("·")
            elif dst in graph.get(src, set()):
                row.append("X") # Strong dependency
            else:
                row.append(" ")
        lines.append("| " + " | ".join(row) + " |")
        
    return "\n".join(lines)

# def build_dependency_report(root: Path, ignore_patterns: List[str]) -> str:
#     # 1. Analyze
#     # graph = analyze_dependencies(root, ignore_patterns)
#     pass

def build_dependency_mermaid(root: Path) -> str:
    # Legacy placeholder, replaced by build_dependency_report
    return ""

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

def run(config: ProjectConfig) -> bool:
    """Execute Arch Flow"""
    root = config.scan.root_path
    
    logger.info(f"Generating Architecture Overview in {root}...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Tech Stack & BOM -> _ARCH.md
    tech_content = generate_tech_section(root, config.scan.ignore_patterns)
    bom_content = generate_bom_section(root, config.scan.ignore_patterns)
    
    arch_file = root / "_ARCH.md"
    arch_content = f"""# Project Architecture
> @CONTEXT: Architecture | Space View
> 最后更新 (Last Updated): {timestamp}

## 1. Technology Stack
{tech_content}

## 2. Third-Party Dependencies (BOM)
{bom_content}

---
*Generated by Niki-docAI*
"""
    io.write_text(arch_file, arch_content)
    logger.info(f"✅ Architecture Overview updated: {arch_file.name}")
    
    # 2. File Map -> Handled by map_flow.py separately
    # Removed from arch_flow to avoid duplicate generation and conflicts.
    # logger.info(f"Generating Project Map...")
    # ... (Logic moved to map_flow)
    
    # 3. Dependencies -> _DEPS.md
    logger.info(f"Generating Dependency Graph...")
    report_content = build_dependency_report(root, config)
    
    deps_content = f"""# Dependency Graph
> @CONTEXT: Dependencies | Graph
> 最后更新 (Last Updated): {timestamp}

{report_content}

---
*Generated by Niki-docAI*
"""
    deps_file = root / "_DEPS.md"
    io.write_text(deps_file, deps_content)
    logger.info(f"✅ Dependency Graph updated: {deps_file.name}")

    return True
