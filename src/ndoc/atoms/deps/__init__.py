"""
Atom: Dependency Parser.
原子能力：依赖文件解析与语言统计。
"""
from .stats import (
    detect_languages, LANGUAGE_EXTENSIONS, DEFAULT_IGNORE_PATTERNS
)
from .parsers import (
    extract_imports, extract_cpp_includes, extract_dart_imports, extract_csharp_usings
)
from .manifests import (
    parse_requirements_txt, parse_pyproject_toml, parse_package_json,
    parse_pubspec_yaml, parse_cmake_lists, parse_csproj
)
from .core import (
    extract_dependencies, get_project_dependencies, SOURCE_PARSERS
)

__all__ = [
    'detect_languages', 'LANGUAGE_EXTENSIONS', 'DEFAULT_IGNORE_PATTERNS',
    'extract_imports', 'extract_cpp_includes', 'extract_dart_imports', 'extract_csharp_usings',
    'parse_requirements_txt', 'parse_pyproject_toml', 'parse_package_json',
    'parse_pubspec_yaml', 'parse_cmake_lists', 'parse_csproj',
    'extract_dependencies', 'get_project_dependencies', 'SOURCE_PARSERS'
]
