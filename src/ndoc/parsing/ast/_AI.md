# Context: ast
> @CONTEXT: Local | ast | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:51

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Centralized Language Access**: All AST operations must obtain language instances via `base.get_language()` or `base.get_parser()`, which internally delegates to `CapabilityManager`. Do not bypass this layer.
<!-- Add local rules here -->
*   **Decoupled AST Logic**: Language-specific queries are isolated in `langs/`. `discovery.py` uses these queries for generic operations (find calls/imports).
*   **Location-Aware Discovery**: `find_calls_with_loc` provides line-level precision for symbol usages, enabling precise linking in `_AI.md`.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: symbols, discovery, base, utils
    *   `@API`
        *   `VAL->` VAR __all__` = [
    'get_language', 'get_parser', 'parse_code', 'query_tre...` [🔗4]
*   **[base.py](base.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: typing, core.capabilities, pathlib, dataclasses, tree_sitter
    *   `@API`
        *   `VAL->` VAR _LANGUAGES` = {}` [🔗5]
        *   `PUB:` FUN **get_language**`(lang_key: str) -> Optional[Language]` [🔗28]
        *   `PUB:` CLS **AstNode** [🔗11]
            *   `VAL->` VAR **type**`: str` [🔗33686]
            *   `VAL->` VAR **text**`: str` [🔗6961]
            *   `VAL->` VAR **start_point**`: tuple[int, int]` [🔗9]
            *   `VAL->` VAR **end_point**`: tuple[int, int]` [🔗6]
            *   `VAL->` VAR **children**`: list['AstNode'] = field(default_factory=list)` [🔗1568]
            *   `GET->` PRP **start_line**`(self) -> int` [🔗2]
            *   `GET->` PRP **end_line**`(self) -> int` [🔗2]
        *   `PUB:` FUN **get_parser**`(lang_key: str = 'python') -> Optional[Parser]` [🔗7]
        *   `PUB:` FUN **parse_code**`(content: str, file_path: Optional[Path] = None) -> Optional[Tree]` [🔗20]
        *   `PUB:` FUN **get_lang_key**`(file_path: Path) -> Optional[str]` [🔗9]
        *   `PUB:` FUN **query_tree**`(tree: Tree, query_scm: str, lang_key: str = 'python') -> list[dict]` [🔗9]
*   **[discovery.py](discovery.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: tree_sitter, typing, base
    *   `@API`
        *   `PUB:` FUN **find_calls**`(tree: Tree, lang_key: str = 'python') -> List[str]` [🔗6]
        *   `PUB:` FUN **find_calls_with_loc**`(tree: Tree, lang_key: str = 'python') -> List[dict]` [🔗5]
        *   `PUB:` FUN **find_imports**`(tree: Tree, lang_key: str = 'python') -> List[str]` [🔗6]
*   **[skeleton.py](skeleton.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: tree_sitter, typing, base, pathlib
    *   `@API`
        *   `PUB:` FUN **generate_skeleton**`(content: str, file_path: Optional[str] = None) -> str` [🔗3]
        *   `PRV:` FUN _reconstruct_skeleton`(node: Node, content_bytes: bytes, lang_key: str) -> str` [🔗2]
        *   `PUB:` FUN **visit**`(n: Node)` [🔗174]
        *   `PRV:` FUN _is_body_node`(node: Node, lang_key: str) -> bool` [🔗2]
*   **[symbols.py](symbols.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: models.symbol, typing, base, utils, core.text_utils, pathlib, tree_sitter
    *   `@API`
        *   `PUB:` FUN **extract_symbols**`(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]` [🔗17]
*   **[utils.py](utils.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: tree_sitter, typing, base
    *   `@API`
        *   `VAL->` VAR **MAX_VALUE_LENGTH**` = 60` [🔗9]
        *   `VAL->` VAR **MAX_CONTENT_LENGTH**` = 200` [🔗6]
        *   `PUB:` FUN **truncate**`(text: str, max_len: int = 100) -> str` [🔗152]
        *   `PUB:` FUN **node_to_data**`(node: Node, include_children: bool = False) -> AstNode` [🔗5]
        *   `PRV:` FUN _get_parent_name`(node: Node, lang_key: str = 'python') -> Optional[str]` [🔗10]
        *   `PRV:` FUN _is_inside_function`(node: Node) -> bool` [🔗4]
        *   `PRV:` FUN _extract_docstring_from_node`(node: Node, content_bytes: bytes, lang_key: str = 'python') -> Optional[str]` [🔗4]
        *   `PRV:` FUN _is_async_function`(node: Node, lang_key: str = 'python') -> bool` [🔗4]
<!-- NIKI_AUTO_Context_END -->
