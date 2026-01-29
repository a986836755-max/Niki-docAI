import re
import sys
import ast
from pathlib import Path
from ndoc.core import console
from ndoc.core import config

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
    
    # C++ Pattern: #include "path/to/module/..." or <module/...>
    # We broaden this to catch any mention of another module's name in include/import
    include_pattern = re.compile(r'#include\s+["<]([^">]+)[">]')
    
    # Dart Pattern: import 'package:module/...' or relative
    dart_import_pattern = re.compile(r"import\s+['\"]([^'\"]+)['\"]")
    
    for module in modules:
        module_path = root / module
        if not module_path.exists():
            continue
            
        # Scan files in this module
        for file_path in module_path.rglob("*"):
            suffix = file_path.suffix
            
            try:
                # C/C++
                if suffix in {'.h', '.hpp', '.cpp', '.c', '.cc'}:
                    content = file_path.read_text(encoding='utf-8', errors='replace')
                    matches = include_pattern.findall(content)
                    for match in matches:
                        # match is the include path, e.g. "ndoc/core/utils.h"
                        # Check if it starts with any other module name
                        parts = match.replace('\\', '/').split('/')
                        if parts[0] in modules and parts[0] != module:
                            deps[module].add(parts[0])
                            
                # Python
                elif suffix == '.py':
                    content = file_path.read_text(encoding='utf-8', errors='replace')
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            imported_names = []
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imported_names.append(alias.name)
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imported_names.append(node.module)
                            
                            for name in imported_names:
                                # name is like "ndoc.core.utils" or "os"
                                # We split by dot and check if any part matches a known module
                                parts = name.split('.')
                                for part in parts:
                                    if part in modules and part != module:
                                        deps[module].add(part)
                                        # Once we find the module dependency in the path, we stop
                                        # e.g. ndoc.core.utils -> matches 'core', we're done
                                        break
                    except SyntaxError:
                        # Skip files with syntax errors (e.g. templates)
                        pass
                    except Exception:
                        pass
                            
                # Dart
                elif suffix == '.dart':
                    content = file_path.read_text(encoding='utf-8', errors='replace')
                    matches = dart_import_pattern.findall(content)
                    for match in matches:
                        # package:module_name/...
                        if match.startswith('package:'):
                            pkg_name = match.split(':')[1].split('/')[0]
                            if pkg_name in modules and pkg_name != module:
                                deps[module].add(pkg_name)
            except: pass
                
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
        with open(arch_file, "w", encoding="utf-8") as f:
            f.write(content)
        console.success(f"Created {arch_file}")
        return

    # File exists: Smart Update
    content = arch_file.read_text(encoding='utf-8')
    
    # 1. Try to find existing markers
    pattern = re.compile(f"{re.escape(config.MARKER_START)}.*?{re.escape(config.MARKER_END)}", re.DOTALL)
    
    if pattern.search(content):
        # Markers found: Replace content inside
        new_content = pattern.sub(new_block, content)
        if new_content != content:
            arch_file.write_text(new_content, encoding='utf-8')
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
            arch_file.write_text(new_content, encoding='utf-8')
            console.success(f"Migrated {arch_file} to use auto-doc markers.")
        else:
            # 3. Fallback: Append/Insert safely
            console.warning(f"Could not find auto-doc markers or standard graph block in {arch_file}.")
            console.warning("Appending new graph to the end of file to avoid overwriting user content.")
            
            new_content = content + "\n\n" + "## Auto-Generated Graph\n" + new_block
            arch_file.write_text(new_content, encoding='utf-8')
