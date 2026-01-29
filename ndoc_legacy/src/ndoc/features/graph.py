import re
import sys
from pathlib import Path
from ndoc.core import console, config
from ndoc.base import io, parser

def get_engine_modules(root):
    """Returns a list of module names found in the root directory."""
    modules = []
    
    # Generic scan: Treat all immediate subdirectories as potential modules
    # Except for ignored ones
    if root.exists():
        for item in root.iterdir():
            if item.is_dir() and not item.name.startswith(".") and item.name not in config.IGNORE_DIRS:
                modules.append(item.name)
                
    return sorted(list(set(modules)))

def scan_module_deps(root, modules):
    """
    Scans dependencies between modules.
    Returns a dict: { "module_name": set(["dep_module_1", "dep_module_2"]) }
    """
    deps = {m: set() for m in modules}
    
    for module in modules:
        module_path = root / module
        if not module_path.exists():
            continue
            
        # Scan files in this module
        for file_path in module_path.rglob("*"):
            if not file_path.is_file():
                continue

            imports = parser.parse_imports(file_path)
            
            for imp in imports:
                # 1. Try exact match (e.g. Dart package name)
                if imp in modules and imp != module:
                    deps[module].add(imp)
                    continue
                    
                # 2. Try splitting by / (C++ include path)
                parts_slash = imp.replace('\\', '/').split('/')
                if parts_slash[0] in modules and parts_slash[0] != module:
                    deps[module].add(parts_slash[0])
                    continue
                    
                # 3. Try splitting by . (Python module path)
                # Only if it looks like a python module path (no slashes)
                if '/' not in imp:
                    parts_dot = imp.split('.')
                    for part in parts_dot:
                        if part in modules and part != module:
                            deps[module].add(part)
                            # Once found, we assume dependency is established
                            break
                
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

def cmd_graph(root, scan_path=None):
    """
    Generates _ARCH.md with the dependency graph.
    root: The project root where _ARCH.md will be generated.
    scan_path: The directory to scan for modules (defaults to root if None).
    """
    console.step("Generating Architecture Graph...")
    
    scan_dir = root / scan_path if scan_path else root
    if not scan_dir.exists():
        console.error(f"Scan directory does not exist: {scan_dir}")
        return

    modules = get_engine_modules(scan_dir)
    if not modules:
        console.warning(f"No modules found in {scan_dir}.")
        return

    console.info(f"Found {len(modules)} modules: {', '.join(modules)}")
    
    deps = scan_module_deps(scan_dir, modules)
    mermaid_graph = generate_mermaid_graph(deps)
    
    arch_file = root / "_ARCH.md"
    
    # Prepare the new block with markers
    new_block = f"{config.MARKER_START}\n```mermaid\n{mermaid_graph}\n```\n{config.MARKER_END}"
    
    if not arch_file.exists():
        # Create new from template
        content = config.ARCH_TEMPLATE.format(
            version=config.TOOLCHAIN_VERSION,
            mermaid_graph=mermaid_graph
        )
        io.write_text_safe(arch_file, content)
        console.success(f"Created {arch_file}")
        return

    # File exists: Smart Update
    content = io.read_text_safe(arch_file)
    
    # 1. Try to find existing markers
    pattern = re.compile(f"{re.escape(config.MARKER_START)}.*?{re.escape(config.MARKER_END)}", re.DOTALL)
    
    if pattern.search(content):
        # Markers found: Replace content inside
        new_content = pattern.sub(new_block, content)
        if new_content != content:
            io.write_text_safe(arch_file, new_content)
            console.success(f"Updated graph in {arch_file} (preserved user edits)")
        else:
            console.info(f"Graph in {arch_file} is up to date.")
    else:
        # 2. No markers found (Legacy migration)
        # Look for the old mermaid block pattern
        legacy_pattern = re.compile(r"```mermaid\n.*?\n```", re.DOTALL)
        if legacy_pattern.search(content):
            # Replace old block with new block (which includes markers)
            new_content = legacy_pattern.sub(new_block, content)
            io.write_text_safe(arch_file, new_content)
            console.success(f"Migrated {arch_file} to use auto-doc markers.")
        else:
            # 3. Fallback: Append/Insert safely
            console.warning(f"Could not find auto-doc markers or standard graph block in {arch_file}.")
            console.warning("Appending new graph to the end of file to avoid overwriting user content.")
            
            new_content = content + "\n\n" + "## Auto-Generated Graph\n" + new_block
            io.write_text_safe(arch_file, new_content)
