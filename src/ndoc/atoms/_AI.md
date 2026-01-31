# Context: atoms
> @CONTEXT: Local | atoms | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 16:49:04

## !RULE
*   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
*   **Enhanced Symbol Context**: `scanner.py` 在重建缓存符号时必须确保 `path` 属性被正确填充，否则会导致下游 CLI 工具 (如 `lsp` 指令) 在解析相对路径时崩溃。
*   **LSP Service Hotness**: `lsp.py` 提供轻量级引用计数。该计数基于全局词频统计，虽然不是 100% 精确的定义引用，但在大规模 codebase 中能有效反映符号的“热度”和影响力。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[ast/](ast/_AI.md#L1)**
*   **[deps/](deps/_AI.md#L1)**
*   **[langs/](langs/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: Atoms: File System Operations.
*   **[cache.py](cache.py#L1)**: Atoms: Cache Management. @DEP: json, typing.Any, typing, pathlib.Path, typing.Dict, hashlib, typing.Optional, pathlib
    *   `@API`
        *   `PUB:` CLS **FileCache**
            *   `PRV:` MET __init__`(self, cache_dir: Path)`
            *   `PUB:` MET **load**`(self)`
            *   `PUB:` MET **save**`(self)`
            *   `PUB:` MET **get_file_hash**`(self, file_path: Path) -> str`
            *   `PUB:` MET **is_changed**`(self, file_path: Path) -> bool`
            *   `PUB:` MET **update**`(self, file_path: Path, result: Any)`
            *   `PUB:` MET **get**`(self, file_path: Path) -> Optional[Any]`
*   **[fs.py](fs.py#L1)**: Atoms: File System Traversal. @DEP: typing.List, typing.Set, typing, os, dataclasses, pathlib.Path, dataclasses.dataclass, dataclasses.field, typing.Iterator, pathspec, typing.Optional, re, typing.Pattern, typing.Callable, pathlib
    *   `@API`
        *   `PUB:` CLS **FileFilter**
            *   `VAL->` VAR **ignore_patterns**`: Set[str] = field(default_factory=set)`
            *   `VAL->` VAR **allow_extensions**`: Set[str] = field(default_factory=set)`
            *   `VAL->` VAR **spec**`: Optional[pathspec.PathSpec] = None`
            *   `GET->` PRP **has_extension_filter**`(self) -> bool`
        *   `PUB:` FUN **load_gitignore**`(root: Path) -> Optional[pathspec.PathSpec]`
        *   `PUB:` FUN **should_ignore**`(path: Path, filter_config: FileFilter, root: Path = None) -> bool`
        *   `PUB:` FUN **list_dir**`(path: Path, filter_config: FileFilter, root: Path = None) -> List[Path]`
        *   `PUB:` FUN **walk_files**`(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]`
        *   `PUB:` FUN **get_relative_path**`(path: Path, root: Path) -> str`
*   **[io.py](io.py#L1)**: Atoms: Input/Output Operations. @DEP: typing.List, typing.Any, typing, datetime, datetime.datetime, os, pathlib.Path, typing.Optional, typing.Union, re, typing.Callable, difflib, pathlib
    *   `@API`
        *   `VAL->` VAR _DRY_RUN_MODE` = False`
        *   `PUB:` FUN **set_dry_run**`(enabled: bool) -> None`
        *   `PUB:` FUN **safe_io**`(operation: Callable[..., Any], error_msg: str, *args: Any, **kwargs: Any) -> Any`
        *   `PUB:` FUN **read_text**`(path: Path) -> Optional[str]`
        *   `PRV:` FUN _read`()`
        *   `PUB:` FUN **read_head**`(path: Path, n_bytes: int = 2048) -> Optional[str]`
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
*   **[llm.py](llm.py#L1)**: Atoms: LLM Connector. @DEP: json, typing.Any, typing, os, typing.Dict, typing.Optional, urllib.request
    *   `@API`
        *   `PUB:` FUN **call_llm**`(prompt: str, system_prompt: str = "You are a helpful assistant.") -> Optional[str]`
        *   `PRV:` FUN _call_openai_compatible`(api_key: str, base_url: str, model: str, prompt: str, system_prompt: str) -> Optional[str]`
        *   `PRV:` FUN _call_gemini`(api_key: str, prompt: str, system_prompt: str) -> Optional[str]`
*   **[lsp.py](lsp.py#L1)**: Atoms: Lightweight LSP-like features. @DEP: typing.List, typing.Any, typing, pathlib.Path, typing.Dict, typing.Optional, re, models.context.Symbol, models.context, pathlib
    *   `@API`
        *   `PUB:` CLS **LSPService**
            *   `PRV:` MET __init__`(self, root: Path)`
            *   `PUB:` MET **index_project**`(self, files: List[Path])`
            *   `PUB:` MET **find_definitions**`(self, name: str) -> List[Symbol]`
            *   `PUB:` MET **get_reference_count**`(self, name: str) -> int`
            *   `PUB:` MET **find_references**`(self, name: str) -> List[Dict[str, Any]]`
        *   `VAL->` VAR _INSTANCE`: Optional[LSPService] = None`
        *   `PUB:` FUN **get_service**`(root: Path) -> LSPService`
*   **[scanner.py](scanner.py#L1)**: Atoms: Content Scanner. @DEP: atoms.ast.extract_symbols, typing.Dict, typing.Pattern, atoms.io, dataclasses.dataclass, dataclasses, pathlib.Path, ast.get_lang_key, atoms.ast.parse_code, models.context.Section, ast.find_calls, atoms.ast, models.context, pathlib, typing.List, typing.Any, text_utils, text_utils.TAG_REGEX, atoms.cache, text_utils.clean_docstring, models.context.Tag, atoms, typing, ast, ast.find_imports, dataclasses.field, typing.Iterator, typing.Optional, re, models.context.Symbol, text_utils.extract_tags_from_text
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
            *   `VAL->` VAR **calls**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **imports**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **is_core**`: bool = False`
        *   `VAL->` VAR _CACHE`: Optional[cache.FileCache] = None`
        *   `PUB:` FUN **get_cache**`(root: Path) -> cache.FileCache`
        *   `PUB:` FUN **scan_file**`(file_path: Path, root: Path, force: bool = False) -> ScanResult`
        *   `PUB:` FUN **extract_todos**`(content: str) -> List[dict]`
        *   `PUB:` FUN **extract_docstring**`(content: str) -> str`
        *   `VAL->` VAR **SECTION_REGEX**` = re.compile(
    r"<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<!--\s*NIKI_\1_END\s*-->", re.DOTALL
)`
        *   `VAL->` VAR **DOCSTRING_PATTERNS**` = [
    re.compile(r'^\s*"""(.*?)"""', re.DOTALL),
    re.compile(r"^\s*'''(.*?)'''", re.DOTALL),
]`
        *   `PUB:` FUN **parse_tags**`(content: str) -> List[Tag]`
        *   `PUB:` FUN **parse_sections**`(content: str) -> Dict[str, Section]`
        *   `PUB:` FUN **extract_summary**`(content: str, docstring: str) -> str`
        *   `PUB:` FUN **regex_scan**`(content: str, ext: str) -> List[Symbol]`
        *   `PUB:` FUN **scan_file_content**`(content: str, file_path: Optional[Path] = None) -> ScanResult`
*   **[text_utils.py](text_utils.py#L1)**: Atoms: Text Processing Utilities. @DEP: models.context.Tag, typing.List, typing, typing.Optional, re, models.context
    *   `@API`
        *   `VAL->` VAR **TAG_REGEX**` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s+(.*?))?(?:\s*(?:-->))?\s*$",
    re.MULTILINE,
)`
        *   `PUB:` FUN **clean_docstring**`(raw: str) -> str`
        *   `PUB:` FUN **extract_tags_from_text**`(text: str, line_offset: int = 0) -> List[Tag]`
<!-- NIKI_AUTO_Context_END -->
