"""
View: Mermaid Graph Renderer.
视图层：Mermaid 图表渲染。
"""
from typing import Dict, Set

def sanitize_node(name: str) -> str:
    """Sanitize node name for Mermaid."""
    return name.replace('.', '_').replace('/', '_').replace('\\', '_').replace('-', '_')

def simplify_module_name(name: str) -> str:
    """Simplify module name for display (e.g. ndoc.core -> core)."""
    parts = name.split('.')
    if len(parts) > 1 and parts[0] == "ndoc":
        return ".".join(parts[1:])
    return name

def generate_mermaid_graph(graph: Dict[str, Set[str]], metrics: Dict[str, Dict[str, float]], core_only: bool = False, is_core_func=None) -> str:
    """Generate Mermaid flowchart"""
    # Layered by I value
    
    # Filter nodes based on core_only flag
    relevant_nodes = set(graph.keys()) | set(t for targets in graph.values() for t in targets)
    if core_only and is_core_func:
        relevant_nodes = {n for n in relevant_nodes if is_core_func(n)}
    
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
            lines.append(f"        {sanitize_node(m)}['{simplify_module_name(m)}']:::volatile")
        lines.append("    end")
        
    if hub:
        lines.append('    subgraph "Hub Zone (0.3 < I < 0.7)"')
        for m in hub:
            lines.append(f"        {sanitize_node(m)}['{simplify_module_name(m)}']:::hub")
        lines.append("    end")
        
    if stable:
        lines.append('    subgraph "Stable Zone (I < 0.3)"')
        for m in stable:
            lines.append(f"        {sanitize_node(m)}['{simplify_module_name(m)}']:::stable")
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
            lines.append(f"    {sanitize_node(source)} --> {sanitize_node(target)}")
            
    if len(lines) == 1:
        return "*No dependencies detected in this view.*"
        
    return "```mermaid\n" + "\n".join(lines) + "\n```"
