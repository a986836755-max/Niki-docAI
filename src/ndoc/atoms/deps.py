
"""
Atom: Dependency Parser.
原子能力：依赖文件解析与语言统计。
"""
from pathlib import Path
from typing import Dict, List, Set, Counter
import re
import configparser
import json
import ast
from . import fs

# --- Configuration (Logic as Data) ---

DEFAULT_IGNORE_PATTERNS = {
    '.git', '.vscode', '.idea', '__pycache__', 
    'node_modules', 'venv', 'env', '.env', 
    'dist', 'build', 'target', 'out', 
    '.dart_tool', '.pub-cache', 
    'coverage', 'tmp', 'temp'
}

# --- Language Stats ---

LANGUAGE_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React',
    '.tsx': 'React TS',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'Sass',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.sh': 'Shell',
    '.bat': 'Batch',
    '.ps1': 'PowerShell',
    '.rs': 'Rust',
    '.go': 'Go',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'C/C++ Header',
    '.hpp': 'C++ Header',
    '.dart': 'Dart',
    '.cmake': 'CMake',
    '.cs': 'C#',
    '.csproj': 'C# Project',
}

def detect_languages(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]:
    """
    扫描项目文件扩展名，统计语言占比 (Scan project for language statistics).
    Uses recursive scan with pruning for performance.
    
    Returns:
        Dict[Language, Percentage]
    """
    stats = Counter()
    total_files = 0
    
    # Use default ignore patterns if not provided
    ignores = list(ignore_patterns or DEFAULT_IGNORE_PATTERNS)
    
    # Use fs.walk_files for consistent ignoring and pruning
    for path in fs.walk_files(root_path, ignore_patterns=ignores):
        ext = path.suffix.lower()
        if ext in LANGUAGE_EXTENSIONS:
            lang = LANGUAGE_EXTENSIONS[ext]
            stats[lang] += 1
            total_files += 1
    
    if total_files == 0:
        return {}
        
    return {lang: round((count / total_files) * 100, 1) for lang, count in stats.most_common()}

# --- Dependency Parsing ---

def extract_imports(content: str) -> List[str]:
    """
    Extract imported module names from Python code using AST.
    Returns list of module names (e.g., 'os', 'ndoc.atoms').
    Handles 'import x', 'from x import y'.
    """
    imports = set()
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
                    # Also add the full module if it's from a package
                    # e.g., "from ndoc.flows import map_flow" -> "ndoc.flows.map_flow"
                    for alias in node.names:
                        imports.add(f"{node.module}.{alias.name}")
    except SyntaxError:
        # Fallback to regex if AST fails (e.g. invalid syntax in some files)
        # import x, y
        for match in re.finditer(r"^\s*import\s+([\w.,\s]+)", content, re.MULTILINE):
            for part in match.group(1).split(','):
                imports.add(part.strip())
        # from x import y
        for match in re.finditer(r"^\s*from\s+([\w.]+)\s+import\s+", content, re.MULTILINE):
            imports.add(match.group(1))
    except Exception:
        pass
    return list(imports)

def parse_requirements_txt(file_path: Path) -> List[str]:
    """Parse requirements.txt"""
    deps = []
    if not file_path.exists():
        return deps
        
    try:
        content = file_path.read_text(encoding='utf-8')
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Simple cleanup of version specifiers to get package name
            # e.g., "pandas>=1.0.0" -> "pandas"
            # Handle "pkg @ url" or "git+https..."
            if line.startswith(('git+', 'http', 'svn+')):
                deps.append(line)
                continue
                
            match = re.match(r'^([a-zA-Z0-9_\-\.]+)', line)
            if match:
                deps.append(line) # Keep full spec for info
    except Exception:
        pass
    return deps

def parse_pyproject_toml(file_path: Path) -> List[str]:
    """Parse pyproject.toml (Poetry/Flit/Setuptools)"""
    deps = []
    if not file_path.exists():
        return deps
    
    try:
        # Simple TOML parsing without external lib for now (std lib tomllib in 3.11+)
        # Fallback to regex for older python if needed, or just reading text
        # Assuming [tool.poetry.dependencies] or [project.dependencies]
        content = file_path.read_text(encoding='utf-8')
        
        # Very rough extraction for robustness without toml lib
        in_dep_section = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                if section in ['tool.poetry.dependencies', 'project.dependencies']:
                    in_dep_section = True
                else:
                    in_dep_section = False
                continue
            
            if in_dep_section and '=' in line:
                key = line.split('=')[0].strip()
                if key and key != 'python':
                    deps.append(key)
    except Exception:
        pass
    return deps

def parse_package_json(file_path: Path) -> List[str]:
    """Parse package.json"""
    deps = []
    if not file_path.exists():
        return deps
        
    try:
        data = json.loads(file_path.read_text(encoding='utf-8'))
        dependencies = data.get('dependencies', {})
        dev_dependencies = data.get('devDependencies', {})
        
        # Combine
        for name, ver in dependencies.items():
            deps.append(f"{name} ({ver})")
        for name, ver in dev_dependencies.items():
            deps.append(f"{name} (dev: {ver})")
            
    except Exception:
        pass
    return deps

def parse_pubspec_yaml(file_path: Path) -> List[str]:
    """
    Parse pubspec.yaml for Dart/Flutter dependencies.
    Extracts dependencies and dev_dependencies.
    """
    deps = []
    if not file_path.exists():
        return deps

    try:
        content = file_path.read_text(encoding='utf-8')
        # Simple YAML parsing without external lib to avoid extra dependencies
        # Looks for "dependencies:" and "dev_dependencies:" sections
        
        lines = content.splitlines()
        current_section = None
        
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
                
            # Check indentation to ensure we are at top level or child level
            indent = len(line) - len(line.lstrip())
            
            if stripped == 'dependencies:':
                current_section = 'deps'
                continue
            elif stripped == 'dev_dependencies:':
                current_section = 'dev_deps'
                continue
            elif stripped.endswith(':') and indent == 0:
                # Other top-level sections
                current_section = None
                continue
                
            if current_section and indent > 0:
                # It's a dependency entry: "name: version" or "name:"
                if ':' in stripped:
                    name = stripped.split(':')[0].strip()
                    # Skip sdk entries or path/git dependencies for simplicity or include them
                    # e.g., flutter:
                    #         sdk: flutter
                    deps.append(name if current_section == 'deps' else f"{name} (dev)")
    except Exception:
        pass
    return deps

def parse_cmake_lists(file_path: Path) -> List[str]:
    """
    Parse CMakeLists.txt for C++ dependencies.
    Extracts FetchContent_Declare and find_package.
    """
    deps = []
    if not file_path.exists():
        return deps
        
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Regex for find_package(Name ...)
        # Case insensitive for cmake commands
        find_pkg_matches = re.findall(r'find_package\s*\(\s*([A-Za-z0-9_]+)', content, re.IGNORECASE)
        for name in find_pkg_matches:
            deps.append(f"find_package: {name}")
            
        # Regex for FetchContent_Declare(Name ...)
        fetch_matches = re.findall(r'FetchContent_Declare\s*\(\s*([A-Za-z0-9_]+)', content, re.IGNORECASE)
        for name in fetch_matches:
            deps.append(f"FetchContent: {name}")
            
    except Exception:
        pass
    return deps

def extract_cpp_includes(content: str) -> List[str]:
    """
    Extract #include directives from C++ code.
    Returns list of included files/libs.
    """
    includes = set()
    try:
        # Match #include <vector> or #include "my_header.h"
        # Allow spaces between # and include
        matches = re.findall(r'#\s*include\s*[<"]([^>"]+)[>"]', content)
        for inc in matches:
            includes.add(inc)
    except Exception:
        pass
    return sorted(list(includes))

def extract_dart_imports(content: str) -> List[str]:
    """
    Extract imports from Dart code.
    Matches: import 'package:foo/foo.dart'; or import 'file.dart';
    """
    imports = set()
    # Matches: import "..." or import '...'
    # Capture group 1: the path
    pattern = re.compile(r"^\s*import\s+['\"](.*?)['\"]", re.MULTILINE)
    
    for match in pattern.finditer(content):
        path = match.group(1)
        # Clean up package: prefix if desired, but keeping it is often better for clarity
        imports.add(path)
        
    return list(imports)

def extract_csharp_usings(content: str) -> List[str]:
    """
    Extract usings from C# code.
    Matches: using System; using Foo.Bar;
    """
    usings = set()
    # Matches: using Namespace;
    pattern = re.compile(r"^\s*using\s+([\w\.]+)\s*;", re.MULTILINE)
    
    for match in pattern.finditer(content):
        usings.add(match.group(1))
        
    return list(usings)

def parse_csproj(file_path: Path) -> List[str]:
    """
    Parse .csproj files for PackageReference.
    """
    deps = set()
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        # Matches: <PackageReference Include="PackageName" ... />
        pattern = re.compile(r'<PackageReference\s+Include="([^"]+)"', re.MULTILINE)
        for match in pattern.finditer(content):
            deps.add(match.group(1))
    except Exception:
        pass
    return list(deps)

# Mapping of file extensions to parser functions
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
    """
    Generic dependency extractor based on file extension.
    Dispatch to specific parser based on file suffix.
    """
    ext = file_path.suffix.lower()
    if ext in SOURCE_PARSERS:
        try:
            return SOURCE_PARSERS[ext](content)
        except Exception:
            return []
    return []

def get_project_dependencies(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]:
    """
    Detect and parse dependency files recursively.
    Uses fs.walk_files for efficient pruning.
    Returns: Dict[RelativeFilePath, List[Dependency]]
    """
    results = {}
    
    # Manifest files
    manifest_parsers = {
        'requirements.txt': parse_requirements_txt,
        'pyproject.toml': parse_pyproject_toml,
        'package.json': parse_package_json,
        'pubspec.yaml': parse_pubspec_yaml,
        'CMakeLists.txt': parse_cmake_lists,
    }

    ignores = list(ignore_patterns or DEFAULT_IGNORE_PATTERNS)

    # Walk with pruning
    for path in fs.walk_files(root_path, ignore_patterns=ignores):
        # 1. Check Manifests (Exact Name or Extension)
        if path.name in manifest_parsers:
            parser = manifest_parsers[path.name]
            try:
                deps = parser(path)
                if deps:
                    rel_path = fs.get_relative_path(path, root_path)
                    results[rel_path] = deps
            except Exception:
                pass
        elif path.suffix.lower() == '.csproj':
             try:
                deps = parse_csproj(path)
                if deps:
                    rel_path = fs.get_relative_path(path, root_path)
                    results[rel_path] = deps
             except Exception:
                pass

        # 2. Check Source Code (Extension)
        if path.suffix.lower() in SOURCE_PARSERS:
            parser = SOURCE_PARSERS[path.suffix.lower()]
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                deps = parser(content)
                if deps:
                    rel_path = fs.get_relative_path(path, root_path)
                    # Merge if both exist (rare but possible if a file matches both)
                    if rel_path in results:
                        results[rel_path].extend(deps)
                    else:
                        results[rel_path] = deps
            except Exception:
                pass
                    
    return results