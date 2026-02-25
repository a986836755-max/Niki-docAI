# Context: parsing
> @CONTEXT: Local | parsing | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:53

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[ast/](ast/_AI.md#L1)**
*   **[deps/](deps/_AI.md#L1)**
*   **[langs/](langs/_AI.md#L1)**
*   **[_LANGS.json](_LANGS.json#L1)**
*   **[__init__.py](__init__.py#L1)**: """ @DEP: langs, ast, scanner, deps
*   **[scanner.py](scanner.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, atoms, models.symbol, typing, os, core.text_utils, models.context, pathlib ...
    *   `@API`
        *   `PUB:` CLS **TokenRule** [🔗3]
            *   `VAL->` VAR **name**`: str` [🔗25070]
            *   `VAL->` VAR **pattern**`: Pattern` [🔗2095]
            *   `VAL->` VAR **group_map**`: Dict[str, int]` [🔗7]
        *   `PUB:` CLS **ScanResult** [🔗19]
            *   `VAL->` VAR **tags**`: List[Tag] = field(default_factory=list)` [🔗855]
            *   `VAL->` VAR **sections**`: Dict[str, Section] = field(default_factory=dict)` [🔗107]
            *   `VAL->` VAR **symbols**`: List[Symbol] = field(default_factory=list)` [🔗702]
            *   `VAL->` VAR **docstring**`: str = ""` [🔗71]
            *   `VAL->` VAR **summary**`: str = ""` [🔗312]
            *   `VAL->` VAR **todos**`: List[dict] = field(default_factory=list)` [🔗172]
            *   `VAL->` VAR **memories**`: List[dict] = field(default_factory=list)` [🔗32]
            *   `VAL->` VAR **decisions**`: List[dict] = field(default_factory=list)` [🔗47]
            *   `VAL->` VAR **intents**`: List[str] = field(default_factory=list)` [🔗26]
            *   `VAL->` VAR **lessons**`: List[dict] = field(default_factory=list)` [🔗31]
            *   `VAL->` VAR **calls**`: List[str] = field(default_factory=list)` [🔗855]
            *   `VAL->` VAR **imports**`: List[str] = field(default_factory=list)` [🔗458]
            *   `VAL->` VAR **tokens**`: Dict[str, int] = field(default_factory=dict)` [🔗1548]
            *   `VAL->` VAR **is_core**`: bool = False` [🔗18]
        *   `VAL->` VAR _CACHE`: Optional[cache.FileCache] = None` [🔗18]
        *   `PUB:` FUN **get_cache**`(root: Path) -> cache.FileCache` [🔗4]
        *   `PRV:` FUN _reconstruct_result`(cached_data: dict, file_path: Path) -> ScanResult` [🔗5]
        *   `PRV:` FUN _scan_worker`(args: Tuple[Path, Path]) -> Tuple[Path, Optional[dict]]` [🔗3]
        *   `PUB:` FUN **scan_project**`(root: Path, ignore_patterns: List[str] = None) -> Dict[Path, ScanResult]` [🔗7]
        *   `PUB:` FUN **scan_file**`(file_path: Path, root: Path, force: bool = False) -> ScanResult` [🔗21]
        *   `PUB:` FUN **extract_todos**`(content: str) -> List[dict]` [🔗2]
        *   `PUB:` FUN **extract_memories**`(content: str) -> List[dict]` [🔗3]
        *   `PUB:` FUN **extract_docstring**`(content: str) -> str` [🔗12]
        *   `VAL->` VAR **SECTION_REGEX**` = re.compile(
    r"<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<...` [🔗3]
        *   `VAL->` VAR **DOCSTRING_PATTERNS**` = [
    re.compile(r'^\s*"""(.*?)"""', re.DOTALL),
    re.comp...` [🔗3]
        *   `PUB:` FUN **parse_tags**`(content: str) -> List[Tag]` [🔗6]
        *   `PUB:` FUN **parse_sections**`(content: str) -> Dict[str, Section]` [🔗3]
        *   `PUB:` FUN **extract_summary**`(content: str, docstring: str) -> str` [🔗5]
        *   `PUB:` FUN **extract_special_comments**`(content: str) -> Dict[str, List[Any]]` [🔗3]
        *   `PUB:` FUN **regex_scan**`(content: str, ext: str, file_path: Optional[Path] = None) -> List[Symbol]` [🔗3]
        *   `PUB:` FUN **scan_file_content**`(content: str, file_path: Optional[Path] = None) -> ScanResult` [🔗8]
*   **[universal.py](universal.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, typing, core.capabilities, pathlib, json, core, tree_sitter
    *   `@API`
        *   `VAL->` VAR _LANG_SPECS` = {}` [🔗4]
        *   `VAL->` VAR _EXT_MAP` = {}` [🔗3]
        *   `PRV:` FUN _load_specs`()` [🔗2]
        *   `PUB:` FUN **get_language_for_file**`(path: Path) -> Optional[str]` [🔗4]
        *   `PUB:` FUN **extract_imports**`(content: str, path: Path) -> Set[str]` [🔗9]
        *   `PUB:` FUN **visit**`(node)` [🔗174]
        *   `PUB:` FUN **extract_definitions**`(content: str, path: Path) -> List[str]` [🔗1]
        *   `PUB:` FUN **visit**`(node)` [🔗174]
<!-- NIKI_AUTO_Context_END -->
