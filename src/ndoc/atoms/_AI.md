# Context: atoms
> @CONTEXT: Local | atoms | @TAGS: @LOCAL

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py)**: Atoms: File System Operations.
*   **[ast.py](ast.py)**: Atoms: AST Parsing (Tree-sitter Wrapper).
    *   `PUB:` CLS **AstNode**
    *   `GET->` VAR **end_line**`(self) -> int`
    *   `PUB:` FUN **extract_symbols**`(tree: Tree, content_bytes: bytes) -> List[Symbol]`
    *   `PUB:` FUN **get_parser**`() -> Parser`
    *   `PUB:` FUN **node_to_data**`(node: Node, include_children: bool = False) -> AstNode`
    *   `PUB:` FUN **parse_code**`(content: str) -> Tree`
    *   `PUB:` FUN **query_tree**`(tree: Tree, query_scm: str) -> List[Dict[str, Node]]`
    *   `GET->` VAR **start_line**`(self) -> int`
    *   `PRV:` FUN _extract_docstring_from_node`(node: Node, content_bytes: bytes) -> Optional[str]`
    *   `@DEP` dataclasses, models.context, tree_sitter, tree_sitter_python, typing
*   **[deps.py](deps.py)**: Atom: Dependency Parser.
    *   `PUB:` FUN **detect_languages**`(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]`
    *   `PUB:` FUN **extract_imports**`(content: str) -> List[str]`
    *   `PUB:` FUN **get_project_dependencies**`(root_path: Path) -> Dict[str, List[str]]`
    *   `PUB:` FUN **parse_package_json**`(file_path: Path) -> List[str]`
    *   `PUB:` FUN **parse_pyproject_toml**`(file_path: Path) -> List[str]`
    *   `PUB:` FUN **parse_requirements_txt**`(file_path: Path) -> List[str]`
    *   `@DEP` ast, configparser, json, pathlib, re, typing
*   **[fs.py](fs.py)**: Atoms: File System Traversal.
    *   `PUB:` CLS **FileFilter**
    *   `PUB:` FUN **get_relative_path**`(path: Path, root: Path) -> str`
    *   `GET->` VAR **has_extension_filter**`(self) -> bool`
    *   `PUB:` FUN **list_dir**`(path: Path, filter_config: FileFilter) -> List[Path]`
    *   `PUB:` FUN **should_ignore**`(name: str, filter_config: FileFilter) -> bool`
    *   `PUB:` FUN **walk_files**`(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]`
    *   `@DEP` dataclasses, os, pathlib, re, typing
*   **[io.py](io.py)**: Atoms: Input/Output Operations.
    *   `PUB:` FUN **append_text**`(path: Path, content: str) -> bool`
    *   `PUB:` FUN **read_lines**`(path: Path) -> List[str]`
    *   `PUB:` FUN **read_text**`(path: Path) -> Optional[str]`
    *   `PUB:` FUN **safe_io**`(operation: Callable[..., Any], error_msg: str, *args, **kwargs) -> Any`
    *   `PUB:` FUN **update_section**`(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool`
    *   `PUB:` FUN **write_text**`(path: Path, content: str) -> bool`
    *   `PRV:` FUN _append`()`
    *   `PRV:` FUN _read`()`
    *   `PRV:` FUN _write`()`
    *   `@DEP` os, pathlib, re, typing
*   **[scanner.py](scanner.py)**: Atoms: Content Scanner.
    *   `PUB:` CLS **ScanResult**
    *   `PUB:` CLS **TokenRule**
    *   `PUB:` FUN **extract_docstring**`(content: str) -> str`
    *   `PUB:` FUN **extract_summary**`(content: str, docstring: str) -> str`
    *   `PUB:` FUN **extract_todos**`(content: str) -> List[dict]`
    *   `PUB:` FUN **parse_sections**`(content: str) -> Dict[str, Section]`
    *   `PUB:` FUN **parse_tags**`(content: str) -> List[Tag]`
    *   `PUB:` FUN **scan_file_content**`(content: str, file_path: Optional[Path] = None) -> ScanResult`
    *   `PRV:` FUN _extract_args`(args_str: Optional[str]) -> List[str]`
    *   `@DEP` atoms.ast, dataclasses, models.context, pathlib, re, typing
<!-- NIKI_AUTO_Context_END -->
