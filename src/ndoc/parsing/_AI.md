# Context: parsing
> @CONTEXT: Local | parsing | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 20:35:08

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->
- DOD Architecture: `scanner.py` (Engine) MUST NOT contain business logic. It delegates to `extractors.py` (Pure Logic) and uses `ndoc.models.scan` (Data).
- Pure Extractors: Functions in `extractors.py` must be pure (no side effects, no I/O).

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[ast/](ast/_AI.md#L1)**
*   **[deps/](deps/_AI.md#L1)**
*   **[langs/](langs/_AI.md#L1)**
*   **[_LANGS.json](_LANGS.json#L1)**
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START>
*   **[extractors.py](extractors.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ., ..core.text_utils, ..models.context, ..models.scan, ..models.symbol, ...
    *   `@API`
        *   `VAL->` VAR **SECTION_REGEX**` = re.compile(
    r"<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<...`
        *   `VAL->` VAR **DOCSTRING_PATTERNS**` = [
    re.compile(r'^\s*"""(.*?)"""', re.DOTALL),
    re.comp...`
        *   `PUB:` FUN **extract_todos**`(content: str) -> List[dict]`
        *   `PUB:` FUN **extract_memories**`(content: str) -> List[dict]`
        *   `PUB:` FUN **extract_docstring**`(content: str) -> str`
        *   `PUB:` FUN **parse_tags**`(content: str) -> List[Tag]`
        *   `PUB:` FUN **parse_sections**`(content: str) -> Dict[str, Section]`
        *   `PUB:` FUN **extract_summary**`(content: str, docstring: str) -> str`
        *   `PUB:` FUN **extract_special_comments**`(content: str) -> Dict[str, List[Any]]`
        *   `PUB:` FUN **regex_scan**`(content: str, ext: str, file_path: Optional[Path] = None) -> List[Symbol]`
        *   `PUB:` FUN **scan_file_content**`(content: str, path: Path) -> ScanResult`
*   **[rules.py](rules.py#L1)**: Parsing: Rule Extraction. @DEP: ..core, pathlib, re, typing
    *   `@API`
        *   `PUB:` FUN **extract_summary_rules**`(ai_path: Path) -> List[str]`
        *   `PUB:` FUN **extract_syntax_summary**`(root: Path) -> str`
        *   `PUB:` FUN **extract_global_rules**`(root: Path) -> str`
        *   `PUB:` FUN **extract_domain_context**`(target_path: Path, root: Path) -> str`
*   **[scanner.py](scanner.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..core.capabilities, ..models.context, ..models.scan, ..models.symbol, ...
    *   `@API`
        *   `VAL->` VAR _CACHE`: Optional[cache.FileCache] = None`
        *   `PUB:` FUN **get_cache**`(root: Path, cache_dir: Path = None) -> cache.FileCache`
        *   `PRV:` FUN _reconstruct_result`(cached_data: dict, file_path: Path) -> ScanResult`
        *   `PRV:` FUN _scan_worker`(args: Tuple[Path, Path]) -> Tuple[Path, Optional[dict]]`
        *   `PUB:` FUN **scan_project**`(root: Path, ignore_patterns: List[str] = None) -> Dict[Path, ScanResult]`
        *   `PUB:` FUN **scan_file**`(file_path: Path, root: Path, force: bool = False) -> ScanResult`
*   **[universal.py](universal.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core.capabilities, .langs, pathlib, re, tree_sitter, ...
    *   `@API`
        *   `VAL->` VAR _LANG_SPECS` = {}`
        *   `VAL->` VAR _EXT_MAP` = {}`
        *   `PUB:` FUN **get_language_for_file**`(path: Path) -> Optional[str]`
        *   `VAL->` VAR **REGEX_PATTERNS**` = {
    'python': [
        r"^\s*import\s+([\w\s,]+)",       ...`
        *   `PRV:` FUN _extract_python_imports`(content: str) -> Set[str]`
        *   `PRV:` FUN _extract_go_imports`(content: str) -> Set[str]`
        *   `PUB:` FUN **extract_imports**`(content: str, path: Path) -> Set[str]`
        *   `PUB:` FUN **extract_definitions**`(content: str, path: Path) -> List[str]`
        *   `PUB:` FUN **visit**`(node)`
<!-- NIKI_AUTO_Context_END -->
