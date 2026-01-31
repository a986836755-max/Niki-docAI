"""
Atoms: Dependency Manifest Parsers.
解析包管理器配置文件。
"""
import re
import json
from pathlib import Path
from typing import List

def parse_requirements_txt(file_path: Path) -> List[str]:
    deps = []
    if not file_path.exists():
        return deps
    try:
        content = file_path.read_text(encoding='utf-8')
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith(('git+', 'http', 'svn+')):
                deps.append(line)
                continue
            match = re.match(r'^([a-zA-Z0-9_\-\.]+)', line)
            if match:
                deps.append(line)
    except Exception:
        pass
    return deps

def parse_pyproject_toml(file_path: Path) -> List[str]:
    deps = []
    if not file_path.exists():
        return deps
    try:
        content = file_path.read_text(encoding='utf-8')
        in_dep_section = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                in_dep_section = section in ['tool.poetry.dependencies', 'project.dependencies']
                continue
            if in_dep_section and '=' in line:
                key = line.split('=')[0].strip()
                if key and key != 'python':
                    deps.append(key)
    except Exception:
        pass
    return deps

def parse_package_json(file_path: Path) -> List[str]:
    deps = []
    if not file_path.exists():
        return deps
    try:
        data = json.loads(file_path.read_text(encoding='utf-8'))
        dependencies = data.get('dependencies', {})
        dev_dependencies = data.get('devDependencies', {})
        for name, ver in dependencies.items():
            deps.append(f"{name} ({ver})")
        for name, ver in dev_dependencies.items():
            deps.append(f"{name} (dev: {ver})")
    except Exception:
        pass
    return deps

def parse_pubspec_yaml(file_path: Path) -> List[str]:
    deps = []
    if not file_path.exists():
        return deps
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()
        current_section = None
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            indent = len(line) - len(line.lstrip())
            if stripped == 'dependencies:':
                current_section = 'deps'
            elif stripped == 'dev_dependencies:':
                current_section = 'dev_deps'
            elif stripped.endswith(':') and indent == 0:
                current_section = None
            elif current_section and indent > 0:
                if ':' in stripped:
                    name = stripped.split(':')[0].strip()
                    deps.append(name if current_section == 'deps' else f"{name} (dev)")
    except Exception:
        pass
    return deps

def parse_cmake_lists(file_path: Path) -> List[str]:
    deps = []
    if not file_path.exists():
        return deps
    try:
        content = file_path.read_text(encoding='utf-8')
        find_pkg_matches = re.findall(r'find_package\s*\(\s*([A-Za-z0-9_]+)', content, re.IGNORECASE)
        for name in find_pkg_matches:
            deps.append(f"find_package: {name}")
        fetch_matches = re.findall(r'FetchContent_Declare\s*\(\s*([A-Za-z0-9_]+)', content, re.IGNORECASE)
        for name in fetch_matches:
            deps.append(f"FetchContent: {name}")
    except Exception:
        pass
    return deps

def parse_csproj(file_path: Path) -> List[str]:
    deps = set()
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        pattern = re.compile(r'<PackageReference\s+Include="([^"]+)"', re.MULTILINE)
        for match in pattern.finditer(content):
            deps.add(match.group(1))
    except Exception:
        pass
    return list(deps)
