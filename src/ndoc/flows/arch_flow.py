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
from concurrent.futures import ThreadPoolExecutor

from ..core import fs, io
from ..parsing import scanner, deps, universal
from ..models.config import ProjectConfig

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
            if level < 2: # Limit depth for Arch view
                lines.extend(build_tree_lines(entry, root, ignore_patterns, level + 1, summary_cache))
        else:
            lines.append(format_file_entry(entry, root, level, summary_cache))
            
    return lines

# --- DEPS LOGIC ---

def analyze_dependencies(root: Path, ignore_patterns: List[str]) -> Dict[str, Set[str]]:
    """
    Analyze internal dependencies (Module A -> Module B).
    Returns a graph: { "ndoc.core": {"ndoc.utils"}, ... }
    """
    # 1. Map files to modules
    module_graph = defaultdict(set)
    file_to_module = {}
    
    for path in fs.walk_files(root, ignore_patterns):
        # Support all languages defined in _LANGS.json
        lang = universal.get_language_for_file(path)
        if not lang:
            continue
            
        # Determine module name (Generic logic)
        try:
            rel = path.relative_to(root)
            # Remove src/ prefix if exists for cleaner module names
            if rel.parts[0] == "src":
                rel = rel.relative_to("src")
                
            parts = rel.parts
            if len(parts) > 1:
                # ndoc/core/fs.py -> ndoc.core
                # editors/vscode/src/extension.ts -> editors.vscode
                module = ".".join(parts[:2])
            else:
                module = parts[0].rsplit('.', 1)[0]
            
            file_to_module[path] = module
        except ValueError:
            continue

    # 2. Extract imports
    for path, current_module in file_to_module.items():
        try:
            content = io.read_text(path)
            if not content:
                continue
                
            # Use universal adapter to extract imports
            imports = universal.extract_imports(content, path)
            
            for imported_name in imports:
                # Check if imported_name matches any of our known modules
                # e.g. 'ndoc.core.fs' matches 'ndoc.core'
                
                # Simple prefix match against known modules
                # We need to normalize imported names to potential module names
                # Python: from ndoc.core import fs -> ndoc.core
                # JS: import ... from './utils' -> relative
                
                # Handle Relative Imports (Generic)
                if imported_name.startswith('.'):
                    # Resolve relative path? Too complex without full context
                    continue
                    
                # Handle Absolute Imports
                # Try to match against keys in file_to_module values
                # This is O(N*M), optimize?
                # Optimization: Create a set of known modules
                
                # Check if import starts with any known module prefix
                # e.g. import 'ndoc.core' starts with 'ndoc'
                
                # Heuristic: split by dot or slash
                parts = imported_name.replace('/', '.').split('.')
                if len(parts) >= 1:
                    candidate = parts[0]
                    if len(parts) >= 2:
                        candidate = f"{parts[0]}.{parts[1]}"
                        
                    # If candidate is a known internal module
                    if candidate in file_to_module.values() and candidate != current_module:
                        module_graph[current_module].add(candidate)
                        
        except Exception:
            pass
            
    return module_graph

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

def build_dependency_report(root: Path, ignore_patterns: List[str]) -> str:
    # 1. Analyze
    graph = analyze_dependencies(root, ignore_patterns)
    metrics = calculate_metrics(graph)
    
    # 2. Table
    table = generate_instability_table(metrics)
    
    # 3. Graph (Mermaid)
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
    for src, targets in graph.items():
        for dst in targets:
            graph_lines.append(f"    {src.replace('.', '_')} --> {dst.replace('.', '_')}")
            
    mermaid = "\n".join(graph_lines)
    
    # 4. Matrix
    # Sort modules for matrix (same as table or alphabetical?)
    # Alphabetical might be easier to lookup
    sorted_modules = sorted(metrics.keys())
    matrix = generate_dependency_matrix(graph, sorted_modules)
    
    return f"""## 1. Instability Metrics
{table}

## 2. Layered Topology
```mermaid
{mermaid}
```

## 3. Dependency Matrix
{matrix}
"""

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
    
    print(f"Generating Architecture Overview in {root}...")
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
    print(f"✅ Architecture Overview updated: {arch_file.name}")
    
    # 2. File Map -> _MAP.md
    print(f"Generating Project Map...")
    all_files = list(fs.walk_files(root, config.scan.ignore_patterns))
    summary_cache = {}
    if all_files:
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(extract_file_summary, all_files))
            summary_cache = dict(zip(all_files, results))
            
    map_lines = build_tree_lines(root, root, config.scan.ignore_patterns, summary_cache=summary_cache)
    map_body = "\n".join(map_lines)
    
    map_content = f"""# Project Map
> @CONTEXT: Map | File Tree
> 最后更新 (Last Updated): {timestamp}

## File Structure
{map_body}

---
*Generated by Niki-docAI*
"""
    map_file = root / "_MAP.md"
    io.write_text(map_file, map_content)
    print(f"✅ Project Map updated: {map_file.name}")

    # 3. Dependencies -> _DEPS.md
    print(f"Generating Dependency Graph...")
    report_content = build_dependency_report(root, config.scan.ignore_patterns)
    
    deps_content = f"""# Dependency Graph
> @CONTEXT: Dependencies | Graph
> 最后更新 (Last Updated): {timestamp}

{report_content}

---
*Generated by Niki-docAI*
"""
    deps_file = root / "_DEPS.md"
    io.write_text(deps_file, deps_content)
    print(f"✅ Dependency Graph updated: {deps_file.name}")

    return True
