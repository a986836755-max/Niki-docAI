"""
Parsing: Dependency Graph Builder.
感知层：依赖图构建器 (Imports & Graph Construction).
"""
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict

from ...core import fs
from ...parsing import scanner
from ...models.config import ProjectConfig

def collect_imports(root_path: Path, config: ProjectConfig = None) -> Dict[str, List[str]]:
    """
    Collect imports from all files in the project.
    Uses 'ndoc.parsing.scanner' (Parallel & Cached).
    """
    import_map = defaultdict(list)
    root = root_path.resolve()
    
    if config is None:
        from ...models.config import ScanConfig
        config = ProjectConfig(scan=ScanConfig(root_path=root))

    # Optimization: Call scanner.scan_project directly
    results = scanner.scan_project(root, config.scan.ignore_patterns)
    
    for file_path, result in results.items():
        try:
            # Normalize path relative to root
            try:
                rel_path = file_path.relative_to(root).as_posix()
            except ValueError:
                continue

            # Use cached imports from ScanResult
            imports = result.imports
            # Even if imports is empty, we record the file so it can be a target
            import_map[rel_path] = imports or []
            
        except Exception as e:
            pass
            
    # DEBUG
    print(f"[DEBUG] builder.collect_imports: Found {len(import_map)} files")
    sample_files = list(import_map.keys())[:3]
    print(f"[DEBUG] Sample files: {sample_files}")
    if sample_files:
        print(f"[DEBUG] Sample imports for {sample_files[0]}: {import_map[sample_files[0]]}")
            
    return import_map

def build_dependency_graph(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]:
    """
    Build internal dependency graph.
    Matches imports to internal files.
    Supports Polyglot (Python, C++, Dart, JS/TS).
    """
    graph = defaultdict(set)
    
    # 1. Build Lookup Indexes
    all_files = set(import_map.keys())
    filename_map = defaultdict(list)
    python_mod_map = {}
    
    for path in all_files:
        filename_map[Path(path).name].append(path)
        
        # Build Python module map if applicable
        if path.endswith('.py'):
            clean_path = path
            if clean_path.startswith('src/'):
                clean_path = clean_path[4:]
            
            clean_path = clean_path[:-3] # remove .py
            if clean_path.endswith('/__init__'):
                clean_path = clean_path[:-9]
                
            mod_name = clean_path.replace('/', '.')
            python_mod_map[mod_name] = path

    # 2. Resolve Imports
    for source_file, imports in import_map.items():
        # Identify source language
        ext = Path(source_file).suffix.lower()
        
        for imp in imports:
            # Fix for potential full-line capture from buggy scanner/cache
            if ext == '.py':
                if len(imp.split()) > 1:
                    imp = imp.strip()
                    if imp.startswith('from '):
                        parts = imp.split()
                        if len(parts) >= 2:
                            imp = parts[1]
                    elif imp.startswith('import '):
                        parts = imp.split()
                        if len(parts) >= 2:
                            imp = parts[1].rstrip(',')

            resolved_target = None
            
            # Strategy A: Python Module Match
            if ext in ('.py', '.pyi'):
                # Try exact module match
                if imp in python_mod_map:
                    resolved_target = python_mod_map[imp]
                # Try parent package match (naive)
                elif '.' in imp and not imp.startswith('.'):
                    parent = imp.rsplit('.', 1)[0]
                    if parent in python_mod_map:
                        resolved_target = python_mod_map[parent]
                # Relative import
                elif imp.startswith('.'):
                    try:
                        source_parts = source_file.replace('\\', '/').split('/')
                        if source_parts[0] == 'src':
                            source_parts = source_parts[1:]
                        
                        current_pkg_parts = source_parts[:-1]
                        
                        dot_count = 0
                        for char in imp:
                            if char == '.':
                                dot_count += 1
                            else:
                                break
                        
                        target_pkg_parts = current_pkg_parts
                        if dot_count > 1:
                            target_pkg_parts = current_pkg_parts[:-(dot_count-1)]
                            
                        suffix = imp[dot_count:]
                        if suffix:
                            target_mod_name = ".".join(target_pkg_parts + [suffix])
                        else:
                            target_mod_name = ".".join(target_pkg_parts)
                            
                        if target_mod_name in python_mod_map:
                            resolved_target = python_mod_map[target_mod_name]
                    except Exception:
                        pass

            # Strategy B: Path/Filename Match (C++, Dart, JS, TS)
            if not resolved_target:
                clean_imp = imp.strip('"\'<>')
                if clean_imp.startswith('package:'):
                    clean_imp = clean_imp.split('/', 1)[-1]

                candidates = filename_map.get(Path(clean_imp).name)
                if candidates:
                    if len(candidates) == 1:
                        resolved_target = candidates[0]
                    else:
                        for c in candidates:
                            if c.endswith(clean_imp):
                                resolved_target = c
                                break
                        if not resolved_target:
                             resolved_target = candidates[0] # Fallback
            
            if resolved_target and resolved_target in all_files:
                if source_file != resolved_target:
                    graph[source_file].add(resolved_target)

    return graph

def get_module_name(path: str) -> str:
    """
    Convert file path to module/package name.
    """
    p = Path(path)
    parts = list(p.parts)
    
    # Remove 'src' prefix if present
    if parts and parts[0] in ('src', 'lib', 'app'):
        parts = parts[1:]
        
    if len(parts) > 1:
        return ".".join(parts[:2])
    elif len(parts) == 1:
        return parts[0].rsplit('.', 1)[0]
    else:
        return "root"

def aggregate_graph(file_graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """
    Aggregate file-level graph to module-level graph.
    """
    module_graph = defaultdict(set)
    
    for src_file, targets in file_graph.items():
        src_mod = get_module_name(src_file)
        
        for tgt_file in targets:
            tgt_mod = get_module_name(tgt_file)
            
            if src_mod != tgt_mod:
                module_graph[src_mod].add(tgt_mod)
                
    return module_graph

def is_core_module(name: str) -> bool:
    """Check if a module is a core business module (not test/debug/scripts)."""
    n = name.lower()
    if n.startswith("tests.") or n.startswith("test.") or ".tests" in n:
        return False
    if n.startswith("debug_") or "debug." in n:
        return False
    if n.startswith("scripts.") or n.startswith("examples."):
        return False
    if n.endswith(".py") and (n.startswith("test_") or "_test" in n):
        return False
    return True
