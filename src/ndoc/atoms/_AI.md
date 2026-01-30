# Context: atoms
> @CONTEXT: Local | atoms | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-30 19:25:16

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Atoms: File System Operations.
*   **[ast.py](ast.py#L1)**: Atoms: AST Parsing (Tree-sitter Wrapper). @DEP: dataclasses, models.context, pathlib, tree_sitter, tree_sitter_c_sharp, tree_sitter_cpp, tree_sitter_dart, tree_sitter_go, tree_sitter_java, tree_sitter_javascript, tree_sitter_python, tree_sitter_rust, tree_sitter_typescript, typing
    *   `@API`
        *   `PUB:` FUN **get_language**`(lang_key: str) -> Optional[Language]`
        *   `PUB:` CLS **AstNode**
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **text**`: str`
            *   `VAL->` VAR **start_point**`: tuple[int, int]`
            *   `VAL->` VAR **end_point**`: tuple[int, int]`
            *   `VAL->` VAR **children**`: List['AstNode'] = field(default_factory=list)`
            *   `GET->` PRP **start_line**`(self) -> int`
            *   `GET->` PRP **end_line**`(self) -> int`
        *   `PUB:` FUN **get_parser**`(lang_key: str = 'python') -> Optional[Parser]`
        *   `PUB:` FUN **parse_code**`(content: str, file_path: Optional[Path] = None) -> Optional[Tree]`
        *   `PUB:` FUN **query_tree**`(tree: Tree, query_scm: str, lang_key: str = 'python') -> List[Dict[str, Node]]`
        *   `PUB:` FUN **node_to_data**`(node: Node, include_children: bool = False) -> AstNode`
        *   `PRV:` FUN _get_parent_name`(node: Node, lang_key: str = 'python') -> Optional[str]`
        *   `PRV:` FUN _extract_docstring_from_node`(node: Node, content_bytes: bytes, lang_key: str = 'python') -> Optional[str]`
        *   `PRV:` FUN _is_async_function`(node: Node, lang_key: str = 'python') -> bool`
        *   `PUB:` FUN **extract_symbols**`(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]`
*   **[deps.py](deps.py#L1)**: Atom: Dependency Parser. @DEP: ast, configparser, json, pathlib, re, typing
    *   `@API`
        *   `PUB:` FUN **detect_languages**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]`
        *   `PUB:` FUN **extract_imports**`(content: str) -> List[str]`
        *   `PUB:` FUN **parse_requirements_txt**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_pyproject_toml**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_package_json**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_pubspec_yaml**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_cmake_lists**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **extract_cpp_includes**`(content: str) -> List[str]`
        *   `PUB:` FUN **extract_dart_imports**`(content: str) -> List[str]`
        *   `PUB:` FUN **extract_csharp_usings**`(content: str) -> List[str]`
        *   `PUB:` FUN **parse_csproj**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **extract_dependencies**`(content: str, file_path: Path) -> List[str]`
        *   `PUB:` FUN **get_project_dependencies**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]`
*   **[fs.py](fs.py#L1)**: Atoms: File System Traversal. @DEP: dataclasses, os, pathlib, re, typing
    *   `@API`
        *   `PUB:` CLS **FileFilter**
            *   `VAL->` VAR **ignore_patterns**`: Set[str] = field(default_factory=set)`
            *   `VAL->` VAR **allow_extensions**`: Set[str] = field(default_factory=set)`
            *   `GET->` PRP **has_extension_filter**`(self) -> bool`
        *   `PUB:` FUN **should_ignore**`(name: str, filter_config: FileFilter) -> bool`
        *   `PUB:` FUN **list_dir**`(path: Path, filter_config: FileFilter) -> List[Path]`
        *   `PUB:` FUN **walk_files**`(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]`
        *   `PUB:` FUN **get_relative_path**`(path: Path, root: Path) -> str`
*   **[io.py](io.py#L1)**: Atoms: Input/Output Operations. @DEP: datetime, difflib, os, pathlib, re, typing
    *   `@API`
        *   `PUB:` FUN **set_dry_run**`(enabled: bool)`
        *   `PUB:` FUN **safe_io**`(operation: Callable[..., Any], error_msg: str, *args, **kwargs) -> Any`
        *   `PUB:` FUN **read_text**`(path: Path) -> Optional[str]`
        *   `PRV:` FUN _read`()`
        *   `PUB:` FUN **write_text**`(path: Path, content: str) -> bool`
        *   `PRV:` FUN _write`()`
        *   `PUB:` FUN **read_lines**`(path: Path) -> List[str]`
        *   `PUB:` FUN **append_text**`(path: Path, content: str) -> bool`
        *   `PRV:` FUN _append`()`
        *   `PUB:` FUN **update_section**`(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool`
        *   `PUB:` FUN **update_header_timestamp**`(path: Path) -> bool`
        *   `PUB:` FUN **delete_file**`(path: Path) -> bool`
        *   `PRV:` FUN _delete`()`
*   **[queries.py](queries.py#L1)**
*   **[scanner.py](scanner.py#L1)**: Atoms: Content Scanner. @DEP: atoms.ast, dataclasses, models.context, pathlib, re, typing
    *   `@API`
        *   `PUB:` CLS **TokenRule**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **pattern**`: Pattern`
            *   `VAL->` VAR **group_map**`: Dict[str, int]`
        *   `PUB:` CLS **ScanResult**
            *   `VAL->` VAR **tags**`: List[Tag] = field(default_factory=list)`
            *   `VAL->` VAR **sections**`: Dict[str, Section] = field(default_factory=dict)`
            *   `VAL->` VAR **symbols**`: List[Symbol] = field(default_factory=list)`
            *   `VAL->` VAR **docstring**`: str = ""`
            *   `VAL->` VAR **summary**`: str = ""`
            *   `VAL->` VAR **todos**`: List[dict] = field(default_factory=list)`
            *   `VAL->` VAR **is_core**`: bool = False`
        *   `PUB:` FUN **extract_todos**`(content: str) -> List[dict]`
        *   `PUB:` FUN **extract_docstring**`(content: str) -> str`
        *   `PUB:` FUN **parse_tags**`(content: str) -> List[Tag]`
        *   `PRV:` FUN _extract_args`(args_str: Optional[str]) -> List[str]`
        *   `PUB:` FUN **parse_sections**`(content: str) -> Dict[str, Section]`
        *   `PUB:` FUN **extract_summary**`(content: str, docstring: str) -> str`
        *   `PUB:` FUN **regex_scan**`(content: str, ext: str) -> List[Symbol]`
        *   `PUB:` FUN **scan_file_content**`(content: str, file_path: Optional[Path] = None) -> ScanResult`
<!-- NIKI_AUTO_Context_END -->
