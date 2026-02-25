# Context: deps
> @CONTEXT: Local | deps | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:52

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """ @DEP: stats, manifests, parsers, core
    *   `@API`
        *   `VAL->` VAR __all__` = [
    'detect_languages', 'LANGUAGE_EXTENSIONS', 'DEFAULT_IG...` [🔗4]
*   **[core.py](core.py#L1)**: """ @DEP: parsers, stats, typing, manifests, pathlib, core
    *   `@API`
        *   `VAL->` VAR **SOURCE_PARSERS**` = {
    '.py': extract_imports,
    '.dart': extract_dart_impo...` [🔗8]
        *   `PUB:` FUN **extract_dependencies**`(content: str, file_path: Path) -> List[str]` [🔗6]
        *   `PUB:` FUN **get_project_dependencies**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]` [🔗4]
*   **[manifests.py](manifests.py#L1)**: """ @DEP: re, pathlib, typing, json
    *   `@API`
        *   `PUB:` FUN **parse_requirements_txt**`(file_path: Path) -> List[str]` [🔗7]
        *   `PUB:` FUN **parse_pyproject_toml**`(file_path: Path) -> List[str]` [🔗7]
        *   `PUB:` FUN **parse_package_json**`(file_path: Path) -> List[str]` [🔗7]
        *   `PUB:` FUN **parse_pubspec_yaml**`(file_path: Path) -> List[str]` [🔗7]
        *   `PUB:` FUN **parse_cmake_lists**`(file_path: Path) -> List[str]` [🔗6]
        *   `PUB:` FUN **parse_csproj**`(file_path: Path) -> List[str]` [🔗7]
*   **[parsers.py](parsers.py#L1)**: """ @DEP: re, typing, ast
    *   `@API`
        *   `PUB:` FUN **extract_imports**`(content: str) -> List[str]` [🔗9]
        *   `PUB:` FUN **extract_cpp_includes**`(content: str) -> List[str]` [🔗10]
        *   `PUB:` FUN **extract_dart_imports**`(content: str) -> List[str]` [🔗6]
        *   `PUB:` FUN **extract_csharp_usings**`(content: str) -> List[str]` [🔗6]
*   **[stats.py](stats.py#L1)**: """ @DEP: pathlib, typing, core
    *   `@API`
        *   `VAL->` VAR **DEFAULT_IGNORE_PATTERNS**` = {
    '.git', '.vscode', '.idea', '__pycache__', 
    'node_...` [🔗17]
        *   `VAL->` VAR **LANGUAGE_EXTENSIONS**` = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': '...` [🔗8]
        *   `PUB:` FUN **detect_languages**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]` [🔗6]
<!-- NIKI_AUTO_Context_END -->
