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

from ..parsing import scanner
from ..atoms import fs, io, deps
from ..models.config import ProjectConfig

# --- Transformations ---

def collect_imports(root: Path) -> Dict[str, List[str]]:
    """
    Collect imports from all Python files.
    Returns: Dict[RelativePath, List[ImportedModule]]
    """
    import_map = {}
    
    # Only scan .py files
    # Ignore common artifacts
    ignore = {'.git', '__pycache__', 'venv', 'env', 'node_modules', 'dist', 'build', 'site-packages'}
    
    # Use scanner.scan_project which is now parallel and cached (Phase 3 Optimized)
    # This handles incremental updates via cache checking
    results = scanner.scan_project(root, list(ignore))
    
    for file_path, result in results.items():
        # Process all scanned files that have imports
        # Language agnostic: scanner extracts imports for all supported languages
        try:
            # Use cached imports from ScanResult
            imports = result.imports
            if not imports:
                continue
            
            # Normalize path relative to root
            try:
                rel_path = file_path.relative_to(root).as_posix()
            except ValueError:
                # File outside root?
                continue
                
            import_map[rel_path] = imports
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

    # 2. Resolve Imports
    for source_file, imports in import_map.items():
        # Identify source language
        ext = Path(source_file).suffix.lower()
        
        for imp in imports:
            resolved_target = None
            
            # Strategy A: Python Module Match
            if ext == '.py':
                # Try exact module match
                if imp in python_mod_map:
                    resolved_target = python_mod_map[imp]
                # Try parent package match (naive)
                elif '.' in imp:
                    parent = imp.rsplit('.', 1)[0]
                    if parent in python_mod_map:
                         resolved_target = python_mod_map[parent]

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
                        best_match = None
                        max_overlap = 0
                        for c in candidates:
                            # Simple suffix check
                            if c.endswith(clean_imp):
                                resolved_target = c
                                break
            
            # Strategy C: Relative Import (JS/TS/Dart)
            # "../utils" -> resolve relative to source_file
            if not resolved_target and (imp.startswith('./') or imp.startswith('../')):
                try:
                    # Resolve relative path
                    # This is tricky without real FS, but we have source_file path
                    # source: src/ui/view.ts, imp: ../model/user
                    # -> src/model/user
                    # Then we need to add extensions (.ts, .js, .tsx etc)
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

def generate_mermaid_graph(graph: Dict[str, Set[str]]) -> str:
    """Generate Mermaid flowchart"""
    lines = ["graph TD"]
    
    # Sort for stability
    for source in sorted(graph.keys()):
        targets = sorted(list(graph[source]))
        for target in targets:
            # Avoid self-loops
            if source == target:
                continue
            lines.append(f"    {source} --> {target}")
            
    if len(lines) == 1:
        return "*No internal dependencies detected.*"
        
    return "```mermaid\n" + "\n".join(lines) + "\n```"

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

def run(config: ProjectConfig) -> bool:
    """Execute the Deps Flow"""
    target_file = config.scan.root_path / "_DEPS.md"
    
    print(f"Scanning dependencies in {config.scan.root_path}...")
    import_map = collect_imports(config.scan.root_path)
    
    # Build the raw dependency graph
    raw_graph = defaultdict(set)
    # Re-implement simple graph building logic here to ensure we have the graph object
    # Or refactor build_dependency_graph to return it properly (it already does)
    graph = build_dependency_graph(import_map)
    
    # Check for circular dependencies
    cycles = find_circular_dependencies(graph)
    if cycles:
        print(f"\n⚠️  Found {len(cycles)} circular dependencies:")
        for cycle in cycles:
            print(f"   - Cycle: {' -> '.join(cycle)} -> {cycle[0]}")
    
    mermaid = generate_mermaid_graph(graph)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# Dependency Graph
> 最后更新 (Last Updated): {timestamp}

> Auto-generated by Niki-docAI.

## Module Graph (Internal)

{mermaid}

> **Note**: Detailed per-file dependencies (Raw Imports) have been moved to local `_AI.md` files to keep this view clean.
"""
    
    io.write_text(target_file, content)
    return True
