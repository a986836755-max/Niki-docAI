# Context: deps
> @CONTEXT: Local | deps | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 16:47:54

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Atom: Dependency Parser. @DEP: stats, core, manifests, parsers
    *   `@API`
        *   `VAL->` VAR __all__` = [
    'detect_languages', 'LANGUAGE_EXTENSIONS', 'DEFAULT_IGNORE_PATTERNS',
    'extract_imports', 'extract_cpp_includes', 'extract_dart_imports', 'extract_csharp_usings',
    'parse_requirements_txt', 'parse_pyproject_toml', 'parse_package_json',
    'parse_pubspec_yaml', 'parse_cmake_lists', 'parse_csproj',
    'extract_dependencies', 'get_project_dependencies', 'SOURCE_PARSERS'
]`
*   **[core.py](core.py#L1)**: Atoms: Dependency Core Logic. @DEP: stats, manifests, pathlib, typing, parsers
    *   `@API`
        *   `VAL->` VAR **SOURCE_PARSERS**` = {
    '.py': extract_imports,
    '.dart': extract_dart_imports,
    '.cpp': extract_cpp_includes,
    '.h': extract_cpp_includes,
    '.hpp': extract_cpp_includes,
    '.c': extract_cpp_includes,
    '.cc': extract_cpp_includes,
    '.cs': extract_csharp_usings,
}`
        *   `PUB:` FUN **extract_dependencies**`(content: str, file_path: Path) -> List[str]`
        *   `PUB:` FUN **get_project_dependencies**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]`
*   **[manifests.py](manifests.py#L1)**: Atoms: Dependency Manifest Parsers. @DEP: typing, re, json, pathlib
    *   `@API`
        *   `PUB:` FUN **parse_requirements_txt**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_pyproject_toml**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_package_json**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_pubspec_yaml**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_cmake_lists**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_csproj**`(file_path: Path) -> List[str]`
*   **[parsers.py](parsers.py#L1)**: Atoms: Source Code Dependency Parsers. @DEP: ast, typing, re
    *   `@API`
        *   `PUB:` FUN **extract_imports**`(content: str) -> List[str]`
        *   `PUB:` FUN **extract_cpp_includes**`(content: str) -> List[str]`
        *   `PUB:` FUN **extract_dart_imports**`(content: str) -> List[str]`
        *   `PUB:` FUN **extract_csharp_usings**`(content: str) -> List[str]`
*   **[stats.py](stats.py#L1)**: Atoms: Language Statistics. @DEP: typing, pathlib
    *   `@API`
        *   `VAL->` VAR **DEFAULT_IGNORE_PATTERNS**` = {
    '.git', '.vscode', '.idea', '__pycache__', 
    'node_modules', 'venv', 'env', '.env', 
    'dist', 'build', 'target', 'out', 
    '.dart_tool', '.pub-cache', 
    'coverage', 'tmp', 'temp'
}`
        *   `VAL->` VAR **LANGUAGE_EXTENSIONS**` = {
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
}`
        *   `PUB:` FUN **detect_languages**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]`
<!-- NIKI_AUTO_Context_END -->
