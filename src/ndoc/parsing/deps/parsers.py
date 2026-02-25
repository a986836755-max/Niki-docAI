"""
Atoms: Source Code Dependency Parsers.
从源代码中提取导入/包含关系。
"""
import re
import ast
from typing import List

def extract_imports(content: str) -> List[str]:
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
    except SyntaxError:
        for match in re.finditer(r"^\s*import\s+([\w.,\s]+)", content, re.MULTILINE):
            for part in match.group(1).split(','):
                imports.add(part.strip())
        for match in re.finditer(r"^\s*from\s+([\w.]+)\s+import\s+", content, re.MULTILINE):
            imports.add(match.group(1))
    except Exception:
        pass
    return list(imports)

def extract_cpp_includes(content: str) -> List[str]:
    includes = set()
    try:
        matches = re.findall(r'#\s*include\s*[<"]([^>"]+)[>"]', content)
        for inc in matches:
            includes.add(inc)
    except Exception:
        pass
    return sorted(list(includes))

def extract_dart_imports(content: str) -> List[str]:
    imports = set()
    pattern = re.compile(r"^\s*import\s+['\"](.*?)['\"]", re.MULTILINE)
    for match in pattern.finditer(content):
        imports.add(match.group(1))
    return list(imports)

def extract_csharp_usings(content: str) -> List[str]:
    usings = set()
    pattern = re.compile(r"^\s*using\s+([\w\.]+)\s*;", re.MULTILINE)
    for match in pattern.finditer(content):
        usings.add(match.group(1))
    return list(usings)
