
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
}

def detect_languages(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]:
    """
    扫描项目文件扩展名，统计语言占比 (Scan project for language statistics).
    Returns:
        Dict[Language, Percentage]
    """
    from . import fs # Avoid circular import if any
    
    # Use existing fs lister but we need recursive all files
    # Simple walk for now as we need stats
    stats = Counter()
    total_files = 0
    
    ignore = ignore_patterns or {'.git', '.vscode', '__pycache__', 'node_modules', 'venv', 'env', 'dist', 'build'}
    
    for path in root_path.rglob('*'):
        if path.is_dir():
            if path.name in ignore:
                continue
            # Skip if parent is ignored (rough check)
            if any(p in ignore for p in path.parts):
                continue
        elif path.is_file():
            if any(p in ignore for p in path.parts):
                continue
                
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
    except Exception:
        pass
    return sorted(list(imports))

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
    Extract import statements from Dart code.
    Returns list of package names or file paths.
    """
    imports = set()
    try:
        # Match import 'package:name/...' or import 'file.dart'
        matches = re.findall(r"import\s+['\"]([^'\"]+)['\"]", content)
        for imp in matches:
            # Filter standard dart: imports if desired, but user asked for imports
            imports.add(imp)
    except Exception:
        pass
    return sorted(list(imports))

def get_project_dependencies(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]:
    """
    Detect and parse dependency files recursively.
    Returns: Dict[RelativeFilePath, List[Dependency]]
    """
    results = {}
    
    target_files = {
        'requirements.txt': parse_requirements_txt,
        'pyproject.toml': parse_pyproject_toml,
        'package.json': parse_package_json,
        'pubspec.yaml': parse_pubspec_yaml,
        'CMakeLists.txt': parse_cmake_lists,
    }
    
    ignore = ignore_patterns or {'.git', '.vscode', '__pycache__', 'node_modules', 'venv', 'env', 'dist', 'build', '.dart_tool'}

    # Walk the directory tree
    for path in root_path.rglob('*'):
        if path.is_dir():
            if path.name in ignore:
                continue
            # Check if any parent is ignored (optimization: rglob descends, so we might process children of ignored dirs if not careful)
            # Actually rglob returns all files. We need to manually filter paths inside ignored dirs.
            if any(p in ignore for p in path.parts):
                continue
        elif path.is_file():
            if any(p in ignore for p in path.parts):
                continue
            
            if path.name in target_files:
                parser = target_files[path.name]
                try:
                    deps = parser(path)
                    if deps:
                        # Use relative path for readability
                        rel_path = path.relative_to(root_path).as_posix()
                        results[rel_path] = deps
                except Exception:
                    pass
                    
    return results