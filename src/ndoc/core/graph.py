"""
Core: Graph Algorithms.
核心层：图算法与度量计算。
"""
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from pathlib import Path

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
