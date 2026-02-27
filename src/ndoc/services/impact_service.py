"""
Impact Service (Kernel-as-a-Service).
Analyzes the impact of file changes using the ECS Dependency Graph.
"""
import subprocess
from pathlib import Path
from typing import List, Set, Dict, Optional, Any
from collections import defaultdict, deque
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType, Component
# We need access to the Dependency Graph.
# The DependencySensorPlugin populates the context with dependencies.
# Ideally, we should have a standard GraphComponent or similar.
# For now, let's assume the DependencySensorPlugin has done its job and we can query the context.

class ImpactService:
    def __init__(self, context: KernelContext, root_path: Path):
        self.context = context
        self.root_path = root_path

    def get_changed_files(self) -> List[str]:
        """
        Get list of changed files (staged + unstaged) via Git.
        Returns relative paths as strings.
        """
        changed = set()
        try:
            # Staged
            staged = subprocess.check_output(
                ['git', 'diff', '--name-only', '--cached'], 
                cwd=str(self.root_path), text=True
            ).splitlines()
            changed.update(staged)
            
            # Unstaged
            unstaged = subprocess.check_output(
                ['git', 'diff', '--name-only'], 
                cwd=str(self.root_path), text=True
            ).splitlines()
            changed.update(unstaged)
            
            # Untracked (optional, but good for new files)
            untracked = subprocess.check_output(
                ['git', 'ls-files', '--others', '--exclude-standard'], 
                cwd=str(self.root_path), text=True
            ).splitlines()
            changed.update(untracked)
            
        except Exception as e:
            print(f"Warning: Failed to get git changes: {e}")
            
        return [f for f in changed if f.strip()]

    def _build_reverse_dependency_graph(self) -> Dict[str, Set[str]]:
        """
        Builds a reverse graph (Provider -> Consumers) from the Kernel Context.
        This relies on how DependencySensorPlugin stores data.
        Currently, DependencySensorPlugin uses `context.pm.hook.ndoc_process_dependencies`
        which likely populates a `DependencyComponent` or updates `GraphComponent`.
        
        Let's check `DependencySensorPlugin` implementation.
        It uses `collect_imports` and `build_dependency_graph` internally,
        and then likely stores it in `context.metadata` or similar?
        
        Wait, `DependencySensorPlugin.ndoc_process_dependencies` implementation:
        It calls `collect_imports` then `build_dependency_graph`.
        Then it sets `context.graph = graph`.
        
        So we can access `context.graph` directly if we run the sensor!
        """
        if hasattr(self.context, 'graph'):
            # context.graph is likely Forward Graph (Consumer -> Providers)
            # We need Reverse Graph (Provider -> Consumers)
            graph = self.context.graph
            rev_graph = defaultdict(set)
            for source, targets in graph.items():
                for target in targets:
                    rev_graph[target].add(source)
            return rev_graph
        else:
            print("⚠️  Dependency Graph not found in Context. Did you run analysis?")
            return {}

    def analyze_impact(self, changed_files: List[str]) -> Dict[str, Any]:
        """
        Analyze impact of changed files.
        Returns a dict with details.
        """
        if not changed_files:
            return {"changed": [], "impacted": []}

        # 1. Map changed files to modules/nodes in the graph
        # The graph keys in `DependencySensorPlugin` are typically module names (e.g. "ndoc.core.utils")
        # We need to convert file paths to module names using the same logic as the sensor.
        
        # We can reuse the logic from the sensor if available, or duplicate it.
        # Let's duplicate the simple heuristic for now as it was in the flow.
        
        changed_modules = []
        for f in changed_files:
            # Normalize path
            p = f.replace('\\', '/')
            # Heuristic: strip 'src/' if present
            if p.startswith('src/'):
                p = p[4:]
            
            if p.endswith('__init__.py'):
                 mod = p.replace('/__init__.py', '').replace('/', '.')
            elif p.endswith('.py'):
                 mod = p[:-3].replace('/', '.')
            else:
                 mod = p.replace('/', '.')
                 
            changed_modules.append(mod)

        # 2. Build Reverse Graph
        rev_graph = self._build_reverse_dependency_graph()
        
        # 3. BFS for Impact
        impacted = set()
        queue = deque(changed_modules)
        visited = set(changed_modules) # Don't re-visit changed nodes as "impacted" (they are the source)
        
        while queue:
            current = queue.popleft()
            
            # Who depends on current?
            dependents = rev_graph.get(current, set())
            for dep in dependents:
                if dep not in visited:
                    visited.add(dep)
                    impacted.add(dep)
                    queue.append(dep)
                    
        return {
            "changed_files": changed_files,
            "changed_modules": changed_modules,
            "impacted_modules": sorted(list(impacted))
        }
