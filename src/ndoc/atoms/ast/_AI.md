# Context: ast
> @CONTEXT: Local | ast | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 16:49:06

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Atoms: AST Parsing (Tree-sitter Wrapper). @DEP: base, base.get_parser, utils.MAX_VALUE_LENGTH, base.query_tree, discovery.find_calls, base.AstNode, utils.MAX_CONTENT_LENGTH, utils.truncate, base.get_language, symbols, base.parse_code, utils, symbols.extract_symbols, discovery.find_imports, base.get_lang_key, discovery, utils.node_to_data
    *   `@API`
        *   `VAL->` VAR __all__` = [
    'get_language', 'get_parser', 'parse_code', 'query_tree', 'AstNode', 'get_lang_key',
    'node_to_data', 'truncate', 'MAX_VALUE_LENGTH', 'MAX_CONTENT_LENGTH',
    'find_calls', 'find_imports', 'extract_symbols'
]`
*   **[base.py](base.py#L1)**: Atoms: AST Parsing Base. @DEP: tree_sitter_c_sharp, typing.Dict, tree_sitter_typescript, tree_sitter.Language, tree_sitter_cpp, tree_sitter_go, pathlib.Path, dataclasses, tree_sitter.Tree, dataclasses.dataclass, tree_sitter_python, tree_sitter_dart, tree_sitter_javascript, pathlib, typing, tree_sitter.Parser, dataclasses.field, typing.Optional, tree_sitter_java, tree_sitter, tree_sitter_rust
    *   `@API`
        *   `VAL->` VAR _LANGUAGES` = {}`
        *   `VAL->` VAR **tspython**` = None`
        *   `VAL->` VAR **tscpp**` = None`
        *   `VAL->` VAR **tsjs**` = None`
        *   `VAL->` VAR **tsts**` = None`
        *   `VAL->` VAR **tsgo**` = None`
        *   `VAL->` VAR **tsrust**` = None`
        *   `VAL->` VAR **tsdart**` = None`
        *   `VAL->` VAR **tscsharp**` = None`
        *   `VAL->` VAR **tsjava**` = None`
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
*   **[discovery.py](discovery.py#L1)**: Atoms: AST Symbol Discovery. @DEP: typing.List, base, typing, base.query_tree, tree_sitter.Tree, base.get_language, tree_sitter
    *   `@API`
        *   `PUB:` FUN **find_calls**`(tree: Tree, lang_key: str = 'python') -> List[str]`
        *   `PUB:` FUN **find_imports**`(tree: Tree, lang_key: str = 'python') -> List[str]`
*   **[symbols.py](symbols.py#L1)**: Atoms: AST Symbol Extraction. @DEP: utils._is_inside_function, utils.MAX_VALUE_LENGTH, utils.truncate, pathlib.Path, tree_sitter.Tree, utils, models.context, pathlib, utils._get_parent_name, typing.List, text_utils, utils._extract_docstring_from_node, base.get_language, base, typing, utils.MAX_CONTENT_LENGTH, typing.Optional, models.context.Symbol, tree_sitter, utils._is_async_function, text_utils.extract_tags_from_text
    *   `@API`
        *   `PUB:` FUN **extract_symbols**`(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]`
*   **[utils.py](utils.py#L1)**: Atoms: AST Parsing Utilities. @DEP: base, typing, base.query_tree, base.AstNode, tree_sitter.Node, typing.Optional, tree_sitter
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
