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
Flow: Impact Analysis.
业务流：全链路影响分析。
"""
import subprocess
from pathlib import Path
from typing import List, Set, Dict, Optional
from collections import defaultdict, deque

from ..models.config import ProjectConfig
from ..parsing.deps.builder import collect_imports, build_dependency_graph
from ..parsing import scanner
from ..core.cli import ndoc_command
from ..core.templates import render_document
from ..core import io
from datetime import datetime

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

@ndoc_command(name="impact", help="Analyze impact of changed files (Git aware)", group="Analysis")
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

    # 1. Collect Imports
    # from .deps_flow import collect_imports
    import_map = collect_imports(root, config)
    
    # 2. Build Dependency Graph
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
    impacted_modules = find_impacted_nodes(changed_modules, rev_graph)
    
    if not impacted_modules:
        print("No downstream impact detected.")
        return True
        
    print(f"⚠️  Impact Detected: {len(impacted_modules)} modules affected.")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    changed_list = "\n".join([f"- `{f}`" for f in sorted(changed_files)])
    impacted_list = "\n".join([f"- `{m}`" for m in sorted(impacted_modules)])
    
    report = render_document(
        "impact.md.tpl",
        title="Impact Analysis Report",
        context="Impact | Git Changes",
        tags="",
        timestamp=timestamp,
        changed_files_list=changed_list,
        impacted_modules_list=impacted_list
    )
    
    print("\n" + report)
    
    return True
