import ast
import re
from pathlib import Path
from ndoc.base import io

def extract_docstring(file_path):
    """
    Extracts the top-level docstring or first comment from a code file.
    Supports Python (via AST) and C++/Dart/JS (via Regex).
    """
    try:
        content = io.read_text_safe(file_path)
        if not content:
            return None
        suffix = file_path.suffix.lower()

        # 1. Python: Use AST + Comment Fallback
        if suffix == '.py':
            try:
                tree = ast.parse(content)
                docstring = ast.get_docstring(tree)
                if docstring:
                    # Return first line of docstring
                    return docstring.strip().split('\n')[0]
            except:
                pass
                
            # Fallback: Check first few lines for # comments
            for line in content.splitlines()[:10]:
                line = line.strip()
                if not line: continue
                if line.startswith('#'):
                    # Skip shebang/encoding
                    if line.startswith('#!') or line.startswith('# -*-'):
                        continue
                    return line.lstrip('#').strip()
                else:
                    # Found code or other stuff (imports, defs), stop searching
                    break

        # 2. C-style (C++, C, Dart, JS, TS, Java, Swift)
        if suffix in {'.cpp', '.h', '.hpp', '.c', '.cc', '.dart', '.js', '.ts', '.java', '.kt', '.swift'}:
            # Match /** ... */ or // ... at start of file
            # Limit search to first 1000 chars to save time
            header = content[:1000]
            
            # Pattern 1: Doxygen/Javadoc style /** ... */
            match = re.search(r'/\*\*(.*?)\*/', header, re.DOTALL)
            if match:
                raw = match.group(1).strip()
                # Remove leading *
                clean = re.sub(r'^\s*\*\s?', '', raw, flags=re.MULTILINE).strip()
                return clean.split('\n')[0]

            # Pattern 2: Simple block comment /* ... */
            match = re.search(r'/\*(.*?)\*/', header, re.DOTALL)
            if match:
                raw = match.group(1).strip()
                # Remove leading *
                clean = re.sub(r'^\s*\*\s?', '', raw, flags=re.MULTILINE).strip()
                return clean.split('\n')[0]
                
            # Pattern 3: Top-level line comments // ...
            # Must be at the very beginning or after whitespace
            match = re.search(r'^\s*//\s*(.*)', header, re.MULTILINE)
            if match:
                return match.group(1).strip()

    except Exception:
        pass
        
    return None

# --- Dependency Parsers ---

def parse_cmake_deps(file_path: Path):
    """Scans CMakeLists.txt for FetchContent_Declare versions."""
    deps = []
    content = io.read_text_safe(file_path)
    if not content:
        return deps
    
    # Regex to capture library name and GIT_TAG
    pattern = re.compile(r'FetchContent_Declare\s*\(\s*([a-zA-Z0-9_]+).*?GIT_TAG\s+([^\s\)]+)', re.DOTALL | re.IGNORECASE)
    
    matches = pattern.findall(content)
    for name, tag in matches:
        deps.append({
            'name': name.lower(),
            'version': tag.strip(),
            'source': 'CMake'
        })
    return deps

def parse_pubspec_deps(file_path: Path):
    """Scans pubspec.yaml for dependency versions."""
    deps = []
    data = io.read_yaml_safe(file_path)
    if not data:
        return deps
            
    if 'environment' in data and 'sdk' in data['environment']:
        deps.append({
            'name': 'dart_sdk', 
            'version': data['environment']['sdk'],
            'source': 'Pubspec'
        })
        
    if 'dependencies' in data:
        for name, ver in data['dependencies'].items():
            version_str = "Unknown"
            if isinstance(ver, str):
                version_str = ver
            elif isinstance(ver, dict):
                if 'sdk' in ver:
                    version_str = f"sdk: {ver['sdk']}"
                elif 'version' in ver:
                    version_str = ver['version']
                elif 'path' in ver:
                    version_str = "local"
            
            deps.append({
                'name': name,
                'version': version_str,
                'source': 'Pubspec'
            })
    return deps

def parse_pyproject_deps(file_path: Path):
    """Scans pyproject.toml for dependencies."""
    deps = []
    content = io.read_text_safe(file_path)
    if not content:
        return deps

    # Simple regex for lines inside dependencies = [...]
    in_deps = False
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('dependencies = ['):
            in_deps = True
            continue
        if in_deps:
            if line.startswith(']'):
                in_deps = False
                break
            # Extract "package>=version"
            m = re.match(r'"(.*?)"', line)
            if m:
                dep_str = m.group(1)
                # Split name and version
                if '>=' in dep_str:
                    name, ver = dep_str.split('>=', 1)
                    ver = '>=' + ver
                elif '==' in dep_str:
                    name, ver = dep_str.split('==', 1)
                    ver = '==' + ver
                else:
                    name = dep_str
                    ver = "latest"
                
                deps.append({
                    'name': name,
                    'version': ver,
                    'source': 'pyproject.toml'
                })
    return deps

def parse_requirements_deps(file_path: Path):
    """Scans requirements.txt for dependencies."""
    deps = []
    content = io.read_text_safe(file_path)
    if not content:
        return deps
        
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Simple parse: name[==|>=|<=]version
        # Handle comments at end of line
        line = line.split('#')[0].strip()
        
        ver = "latest"
        name = line
        
        for op in ['==', '>=', '<=', '~=', '>']:
            if op in line:
                parts = line.split(op, 1)
                name = parts[0].strip()
                ver = op + parts[1].strip()
                break
                
        deps.append({
            'name': name,
            'version': ver,
            'source': 'requirements.txt'
        })
    return deps

def parse_imports(file_path: Path):
    """
    Scans a file for imports/includes.
    Returns a set of imported module names (or paths).
    """
    imports = set()
    suffix = file_path.suffix.lower()
    content = io.read_text_safe(file_path)
    if not content:
        return imports

    # C++ Pattern: #include "path/to/module/..." or <module/...>
    include_pattern = re.compile(r'#include\s+["<]([^">]+)[">]')
    
    # Dart Pattern: import 'package:module/...' or relative
    dart_import_pattern = re.compile(r"import\s+['\"]([^'\"]+)['\"]")

    try:
        # C/C++
        if suffix in {'.h', '.hpp', '.cpp', '.c', '.cc'}:
            matches = include_pattern.findall(content)
            for match in matches:
                imports.add(match)
                    
        # Python
        elif suffix == '.py':
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.add(node.module)
            except SyntaxError:
                pass
                    
        # Dart
        elif suffix == '.dart':
            matches = dart_import_pattern.findall(content)
            for match in matches:
                if match.startswith('package:'):
                    # package:module_name/...
                    pkg_name = match.split(':')[1].split('/')[0]
                    imports.add(pkg_name)
    except: 
        pass
        
    return imports
