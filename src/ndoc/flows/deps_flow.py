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
Flow: Dependency Graph Generation.
业务流：生成模块依赖图 (_DEPS.md)。
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

from ..core import fs, io
from ..core.logger import logger
from ..parsing import scanner
from ..models.config import ProjectConfig

# --- Transformations ---

def collect_imports(root_path: Path, config: ProjectConfig = None) -> Dict[str, List[str]]:
    """
    Collect imports from all files in the project.
    Uses 'ndoc.parsing.scanner' (Parallel & Cached) or 'ndoc.parsing.universal' (Fallback).
    """
    import_map = defaultdict(list)
    root = root_path.resolve()
    
    if config is None:
        # Fallback to minimal config if not provided
        # Or better, require config.
        # But for simplicity let's assume caller provides it or we make minimal
        from ..models.config import ScanConfig
        config = ProjectConfig(scan=ScanConfig(root_path=root))

    # Phase 3: Use Scanner for everything
    # This is parallelized and cached.
    # Use unified file scanner to get file list first
    
    # 1. Get all project files using unified scanner
    # This respects gitignore and ignore_patterns
    target_files = []
    for fpath, lang in fs.scan_project_files(root, config.scan.ignore_patterns):
        if lang != 'binary':
            target_files.append(fpath)
            
    # 2. Batch scan using scanner (which is parallelized internally if we use scan_project, 
    # but scan_project does its own walking. 
    # Let's use scanner.scan_project but pass it the file list if possible? 
    # Currently scanner.scan_project takes root and ignores.
    # It internally uses fs.walk_files. 
    # We should update scanner.scan_project to use fs.scan_project_files too!
    # For now, let's trust scanner.scan_project to be efficient enough or update it later.
    # Actually, we can just use the result from scan_project directly.
    
    # Let's rely on scanner.scan_project for now as it handles caching well.
    # But we can optimize it later to use scan_project_files.
    
    # Optimization: Call scanner.scan_project directly
    results = scanner.scan_project(root, config.scan.ignore_patterns)
    
    for file_path, result in results.items():
        # Process all scanned files
        # Language agnostic: scanner extracts imports for all supported languages
        try:
            # Normalize path relative to root
            try:
                rel_path = file_path.relative_to(root).as_posix()
            except ValueError:
                # File outside root?
                continue

            # Use cached imports from ScanResult
            imports = result.imports
            # Even if imports is empty, we record the file so it can be a target
            import_map[rel_path] = imports or []
            
        except Exception as e:
            # print(f"Error processing {file_path}: {e}")
            pass
            
    return import_map

def build_dependency_graph(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]:
    """
    Build internal dependency graph.
    Matches imports to internal files.
    Supports Polyglot (Python, C++, Dart, JS/TS).
    """
    graph = defaultdict(set)
    
    # 1. Build Lookup Indexes
    # - Exact path lookup: "src/utils.py" -> "src/utils.py"
    # - Filename lookup: "utils.py" -> ["src/utils.py", "tests/utils.py"]
    # - Python Module lookup: "ndoc.utils" -> "src/ndoc/utils.py"
    
    all_files = set(import_map.keys())
    filename_map = defaultdict(list)
    python_mod_map = {}
    
    for path in all_files:
        filename_map[Path(path).name].append(path)
        
        # Build Python module map if applicable
        if path.endswith('.py'):
            clean_path = path
            if clean_path.startswith('src/'):
                clean_path = clean_path[4:]
            
            clean_path = clean_path[:-3] # remove .py
            if clean_path.endswith('/__init__'):
                clean_path = clean_path[:-9]
                
            mod_name = clean_path.replace('/', '.')
            python_mod_map[mod_name] = path
            # print(f"DEBUG: Mapped {mod_name} -> {path}")

    # 2. Resolve Imports
    processed_count = 0
    for source_file, imports in import_map.items():
        processed_count += 1
        # Identify source language
        ext = Path(source_file).suffix.lower()
        
        for imp in imports:
            # Fix for potential full-line capture from buggy scanner/cache
            # E.g. "from ndoc.models.config import ProjectConfig" -> "ndoc.models.config"
            if ext == '.py':
                # print(f"DEBUG: Checking fix for '{imp}'")
                if len(imp.split()) > 1:
                    imp = imp.strip()
                    if imp.startswith('from '):
                        parts = imp.split()
                        if len(parts) >= 2:
                            imp = parts[1]
                    elif imp.startswith('import '):
                        parts = imp.split()
                        if len(parts) >= 2:
                            imp = parts[1].rstrip(',')

            resolved_target = None
            
            # Strategy A: Python Module Match
            if ext in ('.py', '.pyi'):
                # Try exact module match
                if imp in python_mod_map:
                    resolved_target = python_mod_map[imp]
                # Try parent package match (naive)
                elif '.' in imp and not imp.startswith('.'):
                    # Check if parent package exists (e.g. from 'ndoc.core.utils' -> 'ndoc.core')
                    parent = imp.rsplit('.', 1)[0]
                    if parent in python_mod_map:
                        resolved_target = python_mod_map[parent]
                # If "ndoc.core.fs" not found, maybe "ndoc.core"?
                # But imports are usually precise.
                # Problem: from . import x -> Relative import
                elif imp.startswith('.'):
                    # Resolve relative import
                    # source: src/ndoc/core/fs.py
                    # imp: .io -> src/ndoc/core/io.py
                    # imp: ..models -> src/ndoc/models
                    try:
                        # 1. Determine current package depth
                        # src/ndoc/core/fs.py -> package: ndoc.core
                        source_parts = source_file.replace('\\', '/').split('/')
                        if source_parts[0] == 'src':
                            source_parts = source_parts[1:]
                        
                        # Remove filename
                        current_pkg_parts = source_parts[:-1]
                        
                        # 2. Parse relative import dots
                        # . -> 1, .. -> 2
                        dot_count = 0
                        for char in imp:
                            if char == '.':
                                dot_count += 1
                            else:
                                break
                        
                        target_pkg_parts = current_pkg_parts
                        if dot_count > 1:
                            target_pkg_parts = current_pkg_parts[:-(dot_count-1)]
                            
                        # 3. Construct target module name
                        suffix = imp[dot_count:]
                        if suffix:
                            target_mod_name = ".".join(target_pkg_parts + [suffix])
                        else:
                            # from . import ... (importing from __init__)
                            target_mod_name = ".".join(target_pkg_parts)
                            
                        if target_mod_name in python_mod_map:
                            resolved_target = python_mod_map[target_mod_name]
                    except Exception:
                        pass
                
                # Fallback: Try match any suffix
                if not resolved_target and '.' in imp:
                    # imp: ndoc.core.fs
                    # map keys: ndoc.core.fs
                    pass

            # Strategy B: Path/Filename Match (C++, Dart, JS, TS)
            # Imports often look like: "utils.h", "./utils", "package:app/utils.dart"
            if not resolved_target:
                # 1. Clean import string (remove quotes, package: prefix)
                clean_imp = imp.strip('"\'<>')
                if clean_imp.startswith('package:'):
                    # Dart: package:my_app/utils.dart -> lib/utils.dart
                    # We don't know the package name easily, so let's match the suffix
                    clean_imp = clean_imp.split('/', 1)[-1] # utils.dart

                # 2. Try exact filename match
                candidates = filename_map.get(Path(clean_imp).name)
                if candidates:
                    if len(candidates) == 1:
                        resolved_target = candidates[0]
                    else:
                        # Ambiguous: Try to match path suffix
                        # If import is "core/utils.h", we look for "src/core/utils.h"
                        # Prioritize candidates that end with the full clean_imp path
                        for c in candidates:
                            # Simple suffix check
                            if c.endswith(clean_imp):
                                resolved_target = c
                                break
                        
                        # If no suffix match, just pick first? No, risky.
                        if not resolved_target:
                             resolved_target = candidates[0] # Fallback
            
            # Strategy C: Relative Import (JS/TS/Dart)
            # "../utils" -> resolve relative to source_file
            if not resolved_target and (imp.startswith('./') or imp.startswith('../')):
                try:
                    # Resolve relative path
                    # source: src/ui/view.ts (str)
                    # imp: ../model/user
                    
                    # 1. Get source dir
                    src_dir = Path(source_file).parent
                    
                    # 2. Resolve target path
                    target_path_guess = (src_dir / imp).resolve()
                    
                    # But we are working with relative paths string in import_map keys...
                    # And we don't have absolute paths easily here without root.
                    # Wait, source_file is relative string.
                    # We can use pathlib on relative paths? Yes.
                    
                    # src/ui/view.ts -> parent src/ui
                    # src/ui + ../model/user -> src/model/user
                    
                    target_rel = (Path(source_file).parent / imp).as_posix()
                    # Normalize: remove ..
                    # Path('src/ui/../model/user').resolve() needs existing file?
                    # No, strict=False. But resolve() makes it absolute.
                    
                    # Let's use simple normpath equivalent logic or just check if it exists in all_files
                    # But we don't know the extension!
                    # "user" -> "user.ts", "user.js", "user/index.ts"
                    
                    possible_exts = ['.ts', '.js', '.tsx', '.jsx', '.dart', '.py']
                    
                    # Try to match against all_files
                    # This is O(N) per import, slow.
                    # Optimization: Check if target_rel + ext in all_files
                    
                    # We need a robust way to normalize relative path string
                    # import os.path
                    # norm = os.path.normpath(target_rel).replace('\\', '/')
                    
                    # For now, let's skip complex relative resolution if Strategy B caught it by filename.
                    pass
                except:
                    pass

            if resolved_target and resolved_target in all_files:
                # Add edge: source -> target
                # Use simplified names for graph clarity? Or full paths?
                # Let's use full paths for precision, render simplified later.
                if source_file != resolved_target:
                    graph[source_file].add(resolved_target)

    return graph

# --- Helper for Module Aggregation ---

def _is_core_module(name: str) -> bool:
    """Check if a module is a core business module (not test/debug/scripts)."""
    # Normalize
    n = name.lower()
    if n.startswith("tests.") or n.startswith("test.") or ".tests" in n:
        return False
    if n.startswith("debug_") or "debug." in n:
        return False
    if n.startswith("scripts.") or n.startswith("examples."):
        return False
    if n.endswith(".py") and (n.startswith("test_") or "_test" in n):
        # Top level test files
        return False
    return True

def _simplify_module_name(name: str) -> str:
    """Simplify module name for display (e.g. ndoc.core -> core)."""
    parts = name.split('.')
    # If all modules start with same prefix (e.g. ndoc), remove it
    if len(parts) > 1 and parts[0] == "ndoc":
        return ".".join(parts[1:])
    return name

def _get_module_name(path: str) -> str:
    """
    Convert file path to module/package name.
    Aggregation Rules:
    - Same directory -> Same module
    - 'src/ndoc/core/io.py' -> 'ndoc.core' (2 levels deep if src exists)
    - 'src/utils.py' -> 'utils'
    """
    p = Path(path)
    parts = list(p.parts)
    
    # Remove 'src' prefix if present
    if parts and parts[0] in ('src', 'lib', 'app'):
        parts = parts[1:]
        
    # Remove filename if it's not a top-level file in src
    # Actually, we want to group by Directory.
    # But if we have 'src/main.py', that's a module itself.
    # If we have 'src/core/io.py', that belongs to 'core'.
    
    if len(parts) > 1:
        # Group by parent directory
        # ndoc/core/io.py -> ndoc.core
        # ndoc/flows/deps_flow.py -> ndoc.flows
        
        # Check if parent is a package (has __init__.py)? 
        # We don't check file system here for performance, just assume structure.
        # Use first 2 levels for granularity?
        # ndoc.core, ndoc.flows
        
        # If deeply nested: ndoc/parsing/ast/base.py -> ndoc.parsing.ast?
        # Let's try 2 levels for now as requested.
        return ".".join(parts[:2])
    elif len(parts) == 1:
        # Top level file
        return parts[0].rsplit('.', 1)[0]
    else:
        return "root"

def aggregate_graph(file_graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """
    Aggregate file-level graph to module-level graph.
    """
    module_graph = defaultdict(set)
    
    for src_file, targets in file_graph.items():
        src_mod = _get_module_name(src_file)
        
        for tgt_file in targets:
            tgt_mod = _get_module_name(tgt_file)
            
            if src_mod != tgt_mod:
                module_graph[src_mod].add(tgt_mod)
                
    return module_graph

# --- Metrics ---

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
    # Filter only Core Modules for this table? Or keep all?
    # User asked to optimize display. Let's keep all but separate or mark them?
    # Let's show Core Modules first, then others?
    # Or just show all sorted by I.
    
    sorted_modules = sorted(metrics.items(), key=lambda x: x[1]["i"])
    
    for module, m in sorted_modules:
        if not _is_core_module(module):
            continue
            
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
    # Filter core modules only
    core_modules = [m for m in modules if _is_core_module(m)]
    
    if not core_modules:
        return "*No core modules found.*"
        
    lines = []
    # Header - Simplify names
    headers = [_simplify_module_name(m) for m in core_modules]
    
    lines.append("| From \\ To | " + " | ".join(headers) + " |")
    lines.append("| :--- | " + " | ".join([":---:" for _ in headers]) + " |")
    
    for src in core_modules:
        row = [f"**{_simplify_module_name(src)}**"]
        for dst in core_modules:
            if src == dst:
                row.append("·")
            elif dst in graph.get(src, set()):
                row.append("X") # Strong dependency
            else:
                row.append(" ")
        lines.append("| " + " | ".join(row) + " |")
        
    return "\n".join(lines)

def generate_mermaid_graph(graph: Dict[str, Set[str]], metrics: Dict[str, Dict[str, float]], core_only: bool = False) -> str:
    """Generate Mermaid flowchart"""
    # Layered by I value
    
    # Filter nodes based on core_only flag
    relevant_nodes = set(graph.keys()) | set(t for targets in graph.values() for t in targets)
    if core_only:
        relevant_nodes = {n for n in relevant_nodes if _is_core_module(n)}
    
    stable = [m for m in relevant_nodes if metrics.get(m, {}).get("i", 0) < 0.3]
    hub = [m for m in relevant_nodes if 0.3 <= metrics.get(m, {}).get("i", 0) <= 0.7]
    volatile = [m for m in relevant_nodes if metrics.get(m, {}).get("i", 0) > 0.7]

    lines = ["graph TD"]
    # Styles
    lines.append("    classDef stable fill:#2ecc71,stroke:#27ae60,color:white;")
    lines.append("    classDef hub fill:#f1c40f,stroke:#f39c12,color:black;")
    lines.append("    classDef volatile fill:#e74c3c,stroke:#c0392b,color:white;")

    # Subgraphs
    if volatile:
        lines.append('    subgraph "Volatile Zone (I > 0.7)"')
        for m in volatile:
            lines.append(f"        {_sanitize_node(m)}['{_simplify_module_name(m)}']:::volatile")
        lines.append("    end")
        
    if hub:
        lines.append('    subgraph "Hub Zone (0.3 < I < 0.7)"')
        for m in hub:
            lines.append(f"        {_sanitize_node(m)}['{_simplify_module_name(m)}']:::hub")
        lines.append("    end")
        
    if stable:
        lines.append('    subgraph "Stable Zone (I < 0.3)"')
        for m in stable:
            lines.append(f"        {_sanitize_node(m)}['{_simplify_module_name(m)}']:::stable")
        lines.append("    end")
    
    # Edges
    sorted_sources = sorted([n for n in graph.keys() if n in relevant_nodes])
    for source in sorted_sources:
        targets = sorted(list(graph[source]))
        for target in targets:
            if target not in relevant_nodes:
                continue
            # Avoid self-loops
            if source == target:
                continue
            lines.append(f"    {_sanitize_node(source)} --> {_sanitize_node(target)}")
            
    if len(lines) == 1:
        return "*No dependencies detected in this view.*"
        
    return "```mermaid\n" + "\n".join(lines) + "\n```"

def _sanitize_node(name: str) -> str:
    """Sanitize node name for Mermaid."""
    return name.replace('.', '_').replace('/', '_').replace('\\', '_').replace('-', '_')

def find_circular_dependencies(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """
    Find circular dependencies (Strongly Connected Components) using Tarjan's Algorithm.
    Returns a list of cycles (each cycle is a list of node names).
    """
    index = 0
    stack = []
    indices = {}
    lowlinks = {}
    on_stack = set()
    cycles = []
    
    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        
        # Consider successors of v
        if v in graph:
            for w in graph[v]:
                if w not in indices:
                    # Successor w has not yet been visited; recurse on it
                    strongconnect(w)
                    lowlinks[v] = min(lowlinks[v], lowlinks[w])
                elif w in on_stack:
                    # Successor w is in stack and hence in the current SCC
                    lowlinks[v] = min(lowlinks[v], indices[w])
        
        # If v is a root node, pop the stack and generate an SCC
        if lowlinks[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            
            # SCC of size > 1 implies a cycle
            if len(scc) > 1:
                cycles.append(scc)
            # Self-loop check (if size is 1)
            elif len(scc) == 1:
                node = scc[0]
                if node in graph and node in graph[node]:
                    cycles.append(scc)

    for node in list(graph.keys()):
        if node not in indices:
            strongconnect(node)
            
    return cycles

def run(config: ProjectConfig, target: str = None) -> bool:
    """
    Execute Dependency Flow.
    :param target: Optional target directory to filter the dependency graph.
    """
    logger.info("Generating Dependency Graph...")
    root_path = config.scan.root_path
    
    # 1. Collect Imports
    import_map = collect_imports(root_path, config)
    
    # 2. Build Graph
    graph = build_dependency_graph(import_map)
    
    # 3. Filter Graph (if target is provided)
    if target:
        target_path = Path(target).resolve()
        try:
            # Get relative path of target from root
            # e.g. target="src/ndoc/core" -> rel_target="src/ndoc/core"
            rel_target = target_path.relative_to(root_path).as_posix()
            
            logger.info(f"Filtering graph for target: {rel_target}")
            
            # Filter nodes: Keep nodes that are INSIDE the target directory
            # OR are directly connected to nodes inside (1-hop neighborhood)
            filtered_graph = defaultdict(set)
            
            nodes_in_scope = {n for n in graph.keys() if n.startswith(rel_target)}
            
            if not nodes_in_scope:
                logger.warning(f"No files found in target scope: {rel_target}")
                return False
                
            for source in nodes_in_scope:
                # Include outgoing edges
                targets = graph.get(source, set())
                filtered_graph[source] = targets
                
                # Include incoming edges?
                # Usually we want to see what 'source' depends on.
                # If we want to see what depends on 'source', we need reverse graph.
                # Let's keep it simple: Show outgoing dependencies of the target scope.
            
            graph = filtered_graph
            
            # Write to a local _DEPS.md inside the target directory?
            # Or overwrite global? User asked to "create local document".
            # So we should write to target_path / "_DEPS.md"
            target_file = target_path / "_DEPS.md"
            logger.info(f"Dependency Graph (Scoped) updated: {target_file}")
            
        except ValueError:
            logger.error(f"Error: Target {target} is not inside project root.")
            return False
    else:
        target_file = root_path / "_DEPS.md"
        logger.info(f"Dependency Graph updated: {target_file.name}")

    # Calculate Metrics
    # Use Aggregated Graph for Metrics & Visualization
    agg_graph = aggregate_graph(graph)
    
    metrics = calculate_metrics(agg_graph)
    table = generate_instability_table(metrics)
    sorted_modules = sorted(metrics.keys())
    # Matrix might be too large for full project, but let's include it for now or limit it?
    # If modules > 50, matrix is huge.
    matrix = ""
    if len(sorted_modules) < 50:
        matrix = generate_dependency_matrix(agg_graph, sorted_modules)
    else:
        matrix = "*Matrix omitted due to size (> 50 modules).*"

    # Check for circular dependencies (File Level - True Deadlocks)
    file_cycles = find_circular_dependencies(graph)
    
    # Check for circular dependencies (Module Level - Arch Issues)
    mod_cycles = find_circular_dependencies(agg_graph)
    
    cycle_report = ""
    if file_cycles:
        cycle_report += f"\n⚠️  **Found {len(file_cycles)} file-level circular dependencies** (Potential Deadlocks):\n"
        for cycle in file_cycles[:5]: # Limit to 5
            cycle_report += f"   - `{' -> '.join([Path(c).name for c in cycle])} -> {Path(cycle[0]).name}`\n"
        if len(file_cycles) > 5:
            cycle_report += "   - ... (see logs for full list)\n"
            
    if mod_cycles:
        cycle_report += f"\n⚠️  **Found {len(mod_cycles)} module-level circular dependencies** (Architectural Issues):\n"
        for cycle in mod_cycles[:5]:
            cycle_report += f"   - `{' -> '.join(cycle)} -> {cycle[0]}`\n"

    # Generate Two Mermaid Graphs
    # 1. Core Architecture (Filtered)
    mermaid_core = generate_mermaid_graph(agg_graph, metrics, core_only=True)
    
    # 2. Full Relations (Optional, or Test/Debug Relations)
    # Actually, user might want to see full picture too?
    # Let's keep it simple: Core Graph is main.
    # Maybe add a "Full Graph" in a collapsed section? 
    # Or just "Test & Debug Relations" which shows nodes NOT in core?
    
    # Let's just generate the Core Graph for now as requested "Optimization".
    # And maybe a full graph below.
    mermaid_full = generate_mermaid_graph(agg_graph, metrics, core_only=False)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# Dependency Graph
> 最后更新 (Last Updated): {timestamp}

> Auto-generated by Niki-docAI.

## 1. Instability Metrics (Core Modules)
{table}

{cycle_report}

## 2. Core Architecture (Aggregated)
> Showing only core business modules. Tests and debug tools are hidden.
{mermaid_core}

## 3. Dependency Matrix (Core Modules)
{matrix}

## 4. Full Graph (All Modules)
<details>
<summary>Click to expand full graph (including tests & debug tools)</summary>

{mermaid_full}

</details>

> **Note**: This view is aggregated by module/package. Detailed per-file dependencies are available in local `_AI.md` files.
"""
    
    io.write_text(target_file, content)
    return True
