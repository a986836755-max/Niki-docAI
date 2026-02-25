# Context: core
> @CONTEXT: Local | core | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:49

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """ @DEP: fs, capabilities, io, text_utils
*   **[capabilities.py](capabilities.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: typing, sys, subprocess, tree_sitter, importlib
    *   `@API`
        *   `PUB:` CLS **CapabilityManager** [🔗50]
            *   `VAL->` VAR **LANGUAGE_PACKAGES**` = {
        "python": "tree-sitter-python",
        "javascrip...` [🔗5]
            *   `VAL->` VAR **OPTIONAL_PACKAGES**` = {
        "chromadb": "chromadb",
    }` [🔗2]
            *   `VAL->` VAR _CACHE`: Dict[str, Optional[Language]] = {}` [🔗18]
            *   `PUB:` CLM **ensure_package**`(cls, package_name: str, auto_install: bool = True) -> bool` [🔗3]
            *   `PUB:` CLM **ensure_languages**`(cls, lang_names: set[str], auto_install: bool = True)` [🔗8]
            *   `PUB:` CLM **get_language**`(cls, lang_name: str, auto_install: bool = False) -> Optional[Language]` [🔗28]
            *   `PRV:` STA _try_import`(lang_name: str) -> Optional[Language]` [🔗8]
*   **[fs.py](fs.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, typing, os, pathspec, pathlib, dataclasses
    *   `@API`
        *   `PUB:` CLS **FileFilter** [🔗14]
            *   `VAL->` VAR **ignore_patterns**`: Set[str] = field(default_factory=set)` [🔗97]
            *   `VAL->` VAR **allow_extensions**`: Set[str] = field(default_factory=set)` [🔗8]
            *   `VAL->` VAR **spec**`: Optional[pathspec.PathSpec] = None` [🔗875]
            *   `GET->` PRP **has_extension_filter**`(self) -> bool` [🔗4]
        *   `PUB:` FUN **load_gitignore**`(root: Path) -> Optional[pathspec.PathSpec]` [🔗4]
        *   `PUB:` FUN **should_ignore**`(path: Path, filter_config: FileFilter, root: Path = None) -> bool` [🔗7]
        *   `PUB:` FUN **list_dir**`(path: Path, filter_config: FileFilter, root: Path = None) -> List[Path]` [🔗4]
        *   `PUB:` FUN **walk_files**`(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]` [🔗34]
        *   `PUB:` FUN **get_relative_path**`(path: Path, root: Path) -> str` [🔗6]
*   **[io.py](io.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, typing, os, pathlib, difflib, datetime
    *   `@API`
        *   `VAL->` VAR _DRY_RUN_MODE` = False` [🔗7]
        *   `PUB:` FUN **set_dry_run**`(enabled: bool) -> None` [🔗3]
        *   `PUB:` FUN **safe_io**`(operation: Callable[..., Any], error_msg: str, *args: Any, **kwargs: Any) -> Any` [🔗8]
        *   `PUB:` FUN **read_text**`(path: Path) -> Optional[str]` [🔗53]
        *   `PRV:` FUN _read`()` [🔗62]
        *   `PUB:` FUN **read_head**`(path: Path, n_bytes: int = 2048) -> Optional[str]` [🔗5]
        *   `PRV:` FUN _read`()` [🔗62]
        *   `PUB:` FUN **write_text**`(path: Path, content: str) -> bool` [🔗32]
        *   `PRV:` FUN _write`()` [🔗37]
        *   `PUB:` FUN **read_lines**`(path: Path) -> List[str]` [🔗2]
        *   `PUB:` FUN **append_text**`(path: Path, content: str) -> bool` [🔗3]
        *   `PRV:` FUN _append`()` [🔗3]
        *   `PUB:` FUN **update_section**`(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool` [🔗10]
        *   `PUB:` FUN **update_header_timestamp**`(path: Path) -> bool` [🔗8]
        *   `PUB:` FUN **delete_file**`(path: Path) -> bool` [🔗4]
        *   `PRV:` FUN _delete`()` [🔗3]
*   **[text_utils.py](text_utils.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, typing, models.context
    *   `@API`
        *   `VAL->` VAR **TAG_REGEX**` = re.compile(
    r"(?m)^\s*(?:#+|//|<!--|>|\*)\s*([@!][a-zA-Z...` [🔗9]
        *   `PUB:` FUN **clean_docstring**`(raw: str) -> str` [🔗10]
        *   `PUB:` FUN **extract_attributes**`(attr_str: str) -> dict` [🔗3]
        *   `PUB:` FUN **extract_tags_from_text**`(text: str, line_offset: int = 0) -> List[Tag]` [🔗7]
<!-- NIKI_AUTO_Context_END -->
