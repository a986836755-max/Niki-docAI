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
        # Only process Python files for import map
        if file_path.suffix == '.py':
            try:
                # Use cached imports from ScanResult
                imports = result.imports
                
                # Normalize path relative to root
                rel_path = file_path.relative_to(root).as_posix()
                import_map[rel_path] = imports
            except Exception as e:
                # print(f"Error processing {file_path}: {e}")
                pass
            
    return import_map

def build_dependency_graph(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]:
    """
    Build internal dependency graph.
    Matches imports to internal files.
    """
    # Create a map of "possible module names" to file paths
    # e.g. "ndoc/atoms/fs.py" -> "ndoc.atoms.fs"
    
    # We need to guess the module root.
    # If src/ndoc exists, usually 'ndoc' is the root package.
    # For now, we'll try to match "import X" to a file path.
    
    # Simple heuristic:
    # 1. Convert all file paths to dotted notation (removing .py, src/)
    # 2. Check if import matches.
    
    graph = defaultdict(set)
    
    # Helper to convert path to module
    # e.g. src/ndoc/atoms/fs.py -> ndoc.atoms.fs
    path_to_mod = {}
    mod_to_path = {}
    
    for path in import_map.keys():
        # Remove 'src/' prefix if present for module naming
        clean_path = path
        if clean_path.startswith('src/'):
            clean_path = clean_path[4:]
        
        if clean_path.endswith('.py'):
            clean_path = clean_path[:-3]
        elif clean_path.endswith('__init__.py'):
            clean_path = clean_path[:-11] # strip /__init__
            
        module_name = clean_path.replace('/', '.')
        path_to_mod[path] = module_name
        mod_to_path[module_name] = path

    for file_path, imports in import_map.items():
        source_mod = path_to_mod.get(file_path)
        if not source_mod:
            continue
            
        for imp in imports:
            # Check if 'imp' is one of our internal modules
            # Exact match
            if imp in mod_to_path:
                graph[source_mod].add(imp)
                continue
            
            # Parent match (e.g. import ndoc.atoms -> ndoc.atoms.fs ?) 
            # Usually we import specific modules.
            
            # Check sub-modules (e.g. from ndoc import atoms -> ndoc.atoms)
            # This is hard without full resolution.
            # Let's stick to simple prefix matching for now.
            
            # If import starts with project root package?
            # We assume the first part of the module name is the package.
            root_pkg = source_mod.split('.')[0]
            if imp.startswith(root_pkg):
                 # It's likely internal, but maybe we didn't scan it (e.g. generated?)
                 pass

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
