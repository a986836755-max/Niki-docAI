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

def get_project_dependencies(root_path: Path) -> Dict[str, List[str]]:
    """
    Detect and parse dependency files.
    Returns: Dict[SourceFile, List[Dependency]]
    """
    results = {}
    
    # Python
    req_txt = root_path / "requirements.txt"
    if req_txt.exists():
        results["requirements.txt"] = parse_requirements_txt(req_txt)
        
    pyproj = root_path / "pyproject.toml"
    if pyproj.exists():
        results["pyproject.toml"] = parse_pyproject_toml(pyproj)
        
    # JS/TS
    pkg_json = root_path / "package.json"
    if pkg_json.exists():
        results["package.json"] = parse_package_json(pkg_json)
        
    return results
