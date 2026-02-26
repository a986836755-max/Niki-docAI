# Context: ast
> @CONTEXT: Local | ast | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 20:35:04

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Atoms: AST Parsing (Tree-sitter Wrapper). @DEP: .base, .discovery, .symbols, .utils
    *   `@API`
        *   `VAL->` VAR __all__` = [
    'get_language', 'get_parser', 'parse_code', 'query_tre...`
*   **[base.py](base.py#L1)**: Atoms: AST Parsing Base. @DEP: .., ...core.capabilities, dataclasses, pathlib, tree_sitter, ...
    *   `@API`
        *   `VAL->` VAR _LANGUAGES` = {}`
        *   `PUB:` FUN **get_language**`(lang_key: str) -> Optional[Language]`
        *   `PUB:` CLS **AstNode**
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **text**`: str`
            *   `VAL->` VAR **start_point**`: tuple[int, int]`
            *   `VAL->` VAR **end_point**`: tuple[int, int]`
            *   `VAL->` VAR **children**`: list['AstNode'] = field(default_factory=list)`
            *   `GET->` PRP **start_line**`(self) -> int`
            *   `GET->` PRP **end_line**`(self) -> int`
        *   `PUB:` FUN **get_parser**`(lang_key: str = 'python') -> Optional[Parser]`
        *   `PUB:` FUN **parse_code**`(content: str, file_path: Optional[Path] = None) -> Optional[Tree]`
        *   `PUB:` FUN **get_lang_key**`(file_path: Path) -> Optional[str]`
        *   `PUB:` FUN **query_tree**`(tree: Tree, query_scm: str, lang_key: str = 'python') -> list[dict]`
*   **[discovery.py](discovery.py#L1)**: Atoms: AST Symbol Discovery. @DEP: .., .base, tree_sitter, typing
    *   `@API`
        *   `PUB:` FUN **find_calls**`(tree: Tree, lang_key: str = 'python') -> List[str]`
        *   `PUB:` FUN **find_calls_with_loc**`(tree: Tree, lang_key: str = 'python') -> List[dict]`
        *   `PUB:` FUN **find_imports**`(tree: Tree, lang_key: str = 'python') -> List[str]`
*   **[skeleton.py](skeleton.py#L1)**: Atoms: Semantic Skeleton Generator. @DEP: .., .base, ndoc.core.capabilities, pathlib, tree_sitter, ...
    *   `@API`
        *   `PUB:` FUN **generate_skeleton**`(content: str, file_path: Optional[str] = None) -> str`
        *   `PRV:` FUN _reconstruct_skeleton`(node: Node, content_bytes: bytes, lang_key: str) -> str`
        *   `PUB:` FUN **visit**`(n: Node)`
        *   `PRV:` FUN _is_body_node`(node: Node, lang_key: str) -> bool`
*   **[symbols.py](symbols.py#L1)**: Atoms: AST Symbol Extraction. @DEP: .., ...core.text_utils, ...models.symbol, .base, .utils, ...
    *   `@API`
        *   `PUB:` FUN **extract_symbols**`(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]`
*   **[utils.py](utils.py#L1)**: Atoms: AST Parsing Utilities. @DEP: .., .base, tree_sitter, typing
    *   `@API`
        *   `VAL->` VAR **MAX_VALUE_LENGTH**` = 60`
        *   `VAL->` VAR **MAX_CONTENT_LENGTH**` = 200`
        *   `PUB:` FUN **truncate**`(text: str, max_len: int = 100) -> str`
        *   `PUB:` FUN **node_to_data**`(node: Node, include_children: bool = False) -> AstNode`
        *   `PRV:` FUN _get_parent_name`(node: Node, lang_key: str = 'python') -> Optional[str]`
        *   `PRV:` FUN _is_inside_function`(node: Node) -> bool`
        *   `PRV:` FUN _extract_docstring_from_node`(node: Node, content_bytes: bytes, lang_key: str = 'python') -> Optional[str]`
        *   `PRV:` FUN _is_async_function`(node: Node, lang_key: str = 'python') -> bool`
<!-- NIKI_AUTO_Context_END -->
