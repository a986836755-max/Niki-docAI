# Context: deps
> @CONTEXT: Local | deps | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 14:59:54

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """ @DEP: parsers, stats, manifests, core
    *   `@API`
        *   `VAL->` VAR __all__` = [
    'detect_languages', 'LANGUAGE_EXTENSIONS', 'DEFAULT_IG...`
*   **[core.py](core.py#L1)**: """ @DEP: stats, pathlib, typing, manifests, parsers
    *   `@API`
        *   `VAL->` VAR **SOURCE_PARSERS**` = {
    '.py': extract_imports,
    '.dart': extract_dart_impo...`
        *   `PUB:` FUN **extract_dependencies**`(content: str, file_path: Path) -> List[str]`
        *   `PUB:` FUN **get_project_dependencies**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]`
*   **[manifests.py](manifests.py#L1)**: """ @DEP: pathlib, json, re, typing
    *   `@API`
        *   `PUB:` FUN **parse_requirements_txt**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_pyproject_toml**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_package_json**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_pubspec_yaml**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_cmake_lists**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_csproj**`(file_path: Path) -> List[str]`
*   **[parsers.py](parsers.py#L1)**: """ @DEP: typing, re, ast
    *   `@API`
        *   `PUB:` FUN **extract_imports**`(content: str) -> List[str]`
        *   `PUB:` FUN **extract_cpp_includes**`(content: str) -> List[str]`
        *   `PUB:` FUN **extract_dart_imports**`(content: str) -> List[str]`
        *   `PUB:` FUN **extract_csharp_usings**`(content: str) -> List[str]`
*   **[stats.py](stats.py#L1)**: """ @DEP: pathlib, typing
    *   `@API`
        *   `VAL->` VAR **DEFAULT_IGNORE_PATTERNS**` = {
    '.git', '.vscode', '.idea', '__pycache__', 
    'node_...`
        *   `VAL->` VAR **LANGUAGE_EXTENSIONS**` = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': '...`
        *   `PUB:` FUN **detect_languages**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]`
<!-- NIKI_AUTO_Context_END -->
