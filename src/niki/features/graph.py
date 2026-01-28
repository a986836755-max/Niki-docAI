import re
import sys
from pathlib import Path
from niki.core import console
from niki.core import config

def get_engine_modules(root):
    """Returns a list of module names found in engine/modules."""
    modules_dir = root / "engine" / "modules"
    if not modules_dir.exists():
        return []
    
    modules = []
    for item in modules_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            modules.append(item.name)
    return modules

def scan_module_deps(root, modules):
    """
    Scans dependencies between modules.
    Returns a dict: { "module_name": set(["dep_module_1", "dep_module_2"]) }
    """
    deps = {m: set() for m in modules}
    
    # Regex to capture: #include "modules/target_module/..."
    # We allow both " and < just in case, though " is standard for local includes.
    include_pattern = re.compile(r'#include\s+["<]modules/([^/]+)/.*[">]')
    
    modules_dir = root / "engine" / "modules"
    
    for module in modules:
        module_path = modules_dir / module
        # Scan all C++ files
        for file_path in module_path.rglob("*"):
            if file_path.suffix not in {'.h', '.hpp', '.cpp', '.c', '.cc'}:
                continue
                
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = include_pattern.findall(content)
                    for target_module in matches:
                        if target_module != module and target_module in modules:
                            deps[module].add(target_module)
            except Exception as e:
                console.warning(f"Failed to read {file_path}: {e}")
                
    return deps

def generate_mermaid_graph(deps):
    """Converts dependency dict to Mermaid graph syntax."""
    lines = ["graph TD;"]
    
    # Sort for deterministic output
    sorted_modules = sorted(deps.keys())
    
    for module in sorted_modules:
        targets = sorted(list(deps[module]))
        if not targets:
            # Standalone node
            lines.append(f"    {module};")
        else:
            for target in targets:
                lines.append(f"    {module}-->{target};")
                
    return "\n".join(lines)

def cmd_graph(root):
    """Generates _ARCH.md with the dependency graph."""
    console.step("Generating Architecture Graph...")
    
    modules = get_engine_modules(root)
    if not modules:
        console.warning("No modules found in engine/modules.")
        return

    console.info(f"Found {len(modules)} modules: {', '.join(modules)}")
    
    deps = scan_module_deps(root, modules)
    mermaid_graph = generate_mermaid_graph(deps)
    
    arch_file = root / "_ARCH.md"
    content = config.ARCH_TEMPLATE.format(
        version=config.TOOLCHAIN_VERSION,
        mermaid_graph=mermaid_graph
    )
    
    with open(arch_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    console.success(f"Generated {arch_file}")
