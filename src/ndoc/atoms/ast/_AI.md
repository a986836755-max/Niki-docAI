# Context: ast
> @CONTEXT: Local | ast | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 14:59:51

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Centralized Language Access**: All AST operations must obtain language instances via `base.get_language()` or `base.get_parser()`, which internally delegates to `CapabilityManager`. Do not bypass this layer.
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """ @DEP: base, utils, discovery, symbols
    *   `@API`
        *   `VAL->` VAR __all__` = [
    'get_language', 'get_parser', 'parse_code', 'query_tre...`
*   **[base.py](base.py#L1)**: """ @DEP: capabilities, pathlib, typing, dataclasses, tree_sitter
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
*   **[discovery.py](discovery.py#L1)**: """ @DEP: base, tree_sitter, typing
    *   `@API`
        *   `PUB:` FUN **find_calls**`(tree: Tree, lang_key: str = 'python') -> List[str]`
        *   `PUB:` FUN **find_imports**`(tree: Tree, lang_key: str = 'python') -> List[str]`
*   **[symbols.py](symbols.py#L1)**: """ @DEP: text_utils, pathlib, utils, models.context, base, typing, tree_sitter
    *   `@API`
        *   `PUB:` FUN **extract_symbols**`(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]`
*   **[utils.py](utils.py#L1)**: """ @DEP: base, tree_sitter, typing
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
