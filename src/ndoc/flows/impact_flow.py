# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Impact Analysis**: This module performs reverse dependency analysis.
# *   **Graph Theory**: Uses BFS on the transposed dependency graph.
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Impact Analysis.
业务流：全链路影响分析。
"""
import subprocess
from pathlib import Path
from typing import List, Set, Dict, Optional
from collections import defaultdict, deque

from ..models.config import ProjectConfig
from .deps_flow import collect_imports, build_dependency_graph
from ..parsing import scanner

def get_changed_files(root: Path) -> List[str]:
    """
    Get list of changed files (staged + unstaged) via Git.
    Returns relative paths as strings.
    """
    changed = set()
    try:
        # Staged
        staged = subprocess.check_output(
            ['git', 'diff', '--name-only', '--cached'], 
            cwd=str(root), text=True
        ).splitlines()
        changed.update(staged)
        
        # Unstaged
        unstaged = subprocess.check_output(
            ['git', 'diff', '--name-only'], 
            cwd=str(root), text=True
        ).splitlines()
        changed.update(unstaged)
        
        # Untracked (optional, but good for new files)
        untracked = subprocess.check_output(
            ['git', 'ls-files', '--others', '--exclude-standard'], 
            cwd=str(root), text=True
        ).splitlines()
        changed.update(untracked)
        
    except Exception as e:
        print(f"Warning: Failed to get git changes: {e}")
        
    return [f for f in changed if f.strip()]

def build_reverse_graph(graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """
    Transpose the dependency graph: Target -> [Sources]
    """
    rev_graph = defaultdict(set)
    for source, targets in graph.items():
        for target in targets:
            rev_graph[target].add(source)
    return rev_graph

def find_impacted_nodes(changed_modules: List[str], rev_graph: Dict[str, Set[str]]) -> Set[str]:
    """
    Find all nodes that depend on the changed modules (Transitive Closure).
    """
    impacted = set()
    queue = deque(changed_modules)
    visited = set(changed_modules)
    
    while queue:
        current = queue.popleft()
        
        # Who depends on current?
        dependents = rev_graph.get(current, set())
        for dep in dependents:
            if dep not in visited:
                visited.add(dep)
                impacted.add(dep)
                queue.append(dep)
                
    return impacted

def run(config: ProjectConfig) -> bool:
    """
    Run Impact Analysis.
    """
    root = config.scan.root_path
    
    # 1. Get changed files
    changed_files = get_changed_files(root)
    if not changed_files:
        print("No changes detected.")
        return True
        
    print(f"Changed files: {len(changed_files)}")
    for f in changed_files[:5]:
        print(f" - {f}")
    if len(changed_files) > 5:
        print(" ...")

    # 2. Build Dependency Graph
    # Reuse deps_flow logic
    import_map = collect_imports(root)
    graph = build_dependency_graph(import_map)
    
    # 3. Map changed files to modules
    # Heuristic: src/ndoc/brain/checker.py -> ndoc.brain.checker
    changed_modules = []
    
    for f in changed_files:
        if not f.endswith('.py'):
            continue
        # Normalize path
        p = f.replace('\\', '/')
        if p.startswith('src/'):
            p = p[4:]
        
        if p.endswith('__init__.py'): # __init__.py -> package
             mod = p.replace('/__init__.py', '').replace('/', '.')
        elif p.endswith('.py'):
             mod = p[:-3].replace('/', '.')
        else:
             mod = p.replace('/', '.')
             
        changed_modules.append(mod)

    # 4. Build Reverse Graph
    rev_graph = build_reverse_graph(graph)
    
    # 5. Analyze Impact
    impacted = find_impacted_nodes(changed_modules, rev_graph)
    
    # 6. Categorize Impact
    direct_impact = set()
    indirect_impact = set()
    entry_points = set()
    tests = set()
    
    for mod in impacted:
        # Is direct?
        is_direct = any(mod in rev_graph.get(c, set()) for c in changed_modules)
        
        if is_direct:
            direct_impact.add(mod)
        else:
            indirect_impact.add(mod)
            
        # Is test?
        if 'test' in mod or 'tests.' in mod:
            tests.add(mod)
            
        # Is entry point? (Heuristic: main, app, cli, or no dependents)
        # Check forward graph: does anyone import this?
        # Actually, entry point means no one imports it (it's a leaf in reverse graph, root in forward)
        # Wait, if no one imports it, it won't be in rev_graph keys unless it was a source in original graph.
        # Let's check: if mod is not a key in rev_graph (no dependents)
        if mod not in rev_graph: 
            entry_points.add(mod)

    print(f"\n=== Impact Analysis ===")
    print(f"Directly Impacted: {len(direct_impact)}")
    for m in sorted(list(direct_impact))[:5]:
        print(f" - {m}")
        
    print(f"Indirectly Impacted: {len(indirect_impact)}")
    
    print(f"\n=== Recommended Tests ({len(tests)}) ===")
    for t in sorted(list(tests)):
        print(f" [TEST] {t}")
        
    print(f"\n=== Affected Entry Points ({len(entry_points)}) ===")
    for e in sorted(list(entry_points)):
        print(f" [ENTRY] {e}")
        
    return True
