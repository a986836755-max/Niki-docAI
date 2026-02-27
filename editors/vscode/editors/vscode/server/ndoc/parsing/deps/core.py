"""
Core parsing logic for dependency manifests.
"""
from typing import List
import re
from pathlib import Path
from ...core import io
import json

def parse_requirements_txt(file_path: Path) -> List[str]:
    """Parse requirements.txt."""
    content = io.read_text(file_path)
    if not content:
        return []
    
    deps = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # Remove comments
        line = line.split('#')[0].strip()
        # Extract package name (simple regex)
        # Matches: package==1.0, package>=1.0, package
        match = re.match(r'^([a-zA-Z0-9_\-]+)', line)
        if match:
            deps.append(match.group(1))
    return deps

def parse_pyproject_toml(file_path: Path) -> List[str]:
    """Parse pyproject.toml dependencies (simplified)."""
    content = io.read_text(file_path)
    if not content:
        return []
    
    deps = []
    in_dep_section = False
    
    # Very basic TOML parsing
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('[project.dependencies]') or line.startswith('[tool.poetry.dependencies]'):
            in_dep_section = True
            continue
        elif line.startswith('[') and in_dep_section:
            in_dep_section = False
            continue
            
        if in_dep_section and '=' in line:
            key = line.split('=')[0].strip()
            # Ignore python version constraint
            if key and key != 'python':
                deps.append(key)
                
    return deps

def parse_package_json(file_path: Path) -> List[str]:
    """Parse package.json dependencies."""
    content = io.read_text(file_path)
    if not content:
        return []
        
    try:
        data = json.loads(content)
        deps = []
        if 'dependencies' in data:
            deps.extend(data['dependencies'].keys())
        if 'devDependencies' in data:
            deps.extend(data['devDependencies'].keys())
        return deps
    except:
        return []

def parse_pubspec_yaml(file_path: Path) -> List[str]:
    """Parse pubspec.yaml dependencies."""
    content = io.read_text(file_path)
    if not content:
        return []
        
    deps = []
    in_dep_section = False
    
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('dependencies:') or line.startswith('dev_dependencies:'):
            in_dep_section = True
            continue
        # Check if we are in a section and indentation matches list item
        # Simplified: look for "  package:"
        elif in_dep_section and ':' in line and not line.startswith('#'):
            parts = line.split(':')
            key = parts[0].strip()
            # Avoid detecting subsequent sections
            if not line.startswith(' '): # If unindented, likely a new section
                in_dep_section = False
                continue
            if key:
                deps.append(key)
        elif not line:
            continue
            
    return deps

def parse_csproj(file_path: Path) -> List[str]:
    """Parse .csproj dependencies (PackageReference)."""
    content = io.read_text(file_path)
    if not content:
        return []
        
    deps = []
    # <PackageReference Include="Microsoft.AspNetCore.App" />
    for match in re.finditer(r'<PackageReference\s+Include="([^"]+)"', content):
        deps.append(match.group(1))
        
    return deps

def parse_go_mod(file_path: Path) -> List[str]:
    """Parse go.mod dependencies."""
    content = io.read_text(file_path)
    if not content:
        return []
        
    deps = []
    in_require = False
    
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('require ('):
            in_require = True
            continue
        elif line == ')':
            in_require = False
            continue
        elif line.startswith('require '):
            # require github.com/foo/bar v1.0.0
            parts = line.split()
            if len(parts) >= 2:
                deps.append(parts[1])
        elif in_require:
            # github.com/foo/bar v1.0.0
            parts = line.split()
            if len(parts) >= 1:
                deps.append(parts[0])
                
    return deps

def parse_cargo_toml(file_path: Path) -> List[str]:
    """Parse Cargo.toml dependencies."""
    content = io.read_text(file_path)
    if not content:
        return []
        
    deps = []
    in_dep_section = False
    
    # Very basic TOML parsing for [dependencies] and [dev-dependencies]
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('[dependencies]') or line.startswith('[dev-dependencies]'):
            in_dep_section = True
            continue
        elif line.startswith('[') and in_dep_section:
            in_dep_section = False
            continue
            
        if in_dep_section and '=' in line:
            key = line.split('=')[0].strip()
            if key:
                deps.append(key)
                
    return deps
