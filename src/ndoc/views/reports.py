"""
View: Report Tables.
视图层：表格报告渲染。
"""
from typing import Dict, List, Set
from .mermaid import simplify_module_name

def generate_instability_table(metrics: Dict[str, Dict[str, float]], is_core_func=None) -> str:
    lines = []
    lines.append("| Module | Ca (In) | Ce (Out) | Instability (I) | Role |")
    lines.append("| :--- | :---: | :---: | :---: | :--- |")
    
    sorted_modules = sorted(metrics.items(), key=lambda x: x[1]["i"])
    
    for module, m in sorted_modules:
        if is_core_func and not is_core_func(module):
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

def generate_dependency_matrix(graph: Dict[str, Set[str]], modules: List[str], is_core_func=None) -> str:
    # Filter core modules only if func provided
    if is_core_func:
        core_modules = [m for m in modules if is_core_func(m)]
    else:
        core_modules = modules
    
    if not core_modules:
        return "*No core modules found.*"
        
    lines = []
    # Header - Simplify names
    headers = [simplify_module_name(m) for m in core_modules]
    
    lines.append("| From \\ To | " + " | ".join(headers) + " |")
    lines.append("| :--- | " + " | ".join([":---:" for _ in headers]) + " |")
    
    for src in core_modules:
        row = [f"**{simplify_module_name(src)}**"]
        for dst in core_modules:
            if src == dst:
                row.append("·")
            elif dst in graph.get(src, set()):
                row.append("X") # Strong dependency
            else:
                row.append(" ")
        lines.append("| " + " | ".join(row) + " |")
        
    return "\n".join(lines)
