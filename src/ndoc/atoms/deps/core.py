"""
Atoms: Dependency Core Logic.
核心依赖分析流程。
"""
from pathlib import Path
from typing import Dict, List, Set
from .. import fs
from .stats import DEFAULT_IGNORE_PATTERNS
from .manifests import (
    parse_requirements_txt, parse_pyproject_toml, parse_package_json,
    parse_pubspec_yaml, parse_cmake_lists, parse_csproj
)
from .parsers import (
    extract_imports, extract_cpp_includes, extract_dart_imports, extract_csharp_usings
)

SOURCE_PARSERS = {
    '.py': extract_imports,
    '.dart': extract_dart_imports,
    '.cpp': extract_cpp_includes,
    '.h': extract_cpp_includes,
    '.hpp': extract_cpp_includes,
    '.c': extract_cpp_includes,
    '.cc': extract_cpp_includes,
    '.cs': extract_csharp_usings,
}

def extract_dependencies(content: str, file_path: Path) -> List[str]:
    ext = file_path.suffix.lower()
    if ext in SOURCE_PARSERS:
        try:
            return SOURCE_PARSERS[ext](content)
        except Exception:
            return []
    return []

def get_project_dependencies(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]:
    results = {}
    manifest_parsers = {
        'requirements.txt': parse_requirements_txt,
        'pyproject.toml': parse_pyproject_toml,
        'package.json': parse_package_json,
        'pubspec.yaml': parse_pubspec_yaml,
        'CMakeLists.txt': parse_cmake_lists,
    }
    ignores = list(ignore_patterns or DEFAULT_IGNORE_PATTERNS)
    
    for path in fs.walk_files(root_path, ignore_patterns=ignores):
        if path.name in manifest_parsers:
            parser = manifest_parsers[path.name]
            try:
                deps = parser(path)
                if deps:
                    results[fs.get_relative_path(path, root_path)] = deps
            except Exception: pass
        elif path.suffix.lower() == '.csproj':
             try:
                deps = parse_csproj(path)
                if deps:
                    results[fs.get_relative_path(path, root_path)] = deps
             except Exception: pass

        if path.suffix.lower() in SOURCE_PARSERS:
            parser = SOURCE_PARSERS[path.suffix.lower()]
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                deps = parser(content)
                if deps:
                    rel_path = fs.get_relative_path(path, root_path)
                    if rel_path in results:
                        results[rel_path].extend(deps)
                    else:
                        results[rel_path] = deps
            except Exception: pass
    return results
