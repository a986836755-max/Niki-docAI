# Context: core
> @CONTEXT: Recursive Context | core | @TAGS: @AI
> 最后更新 (Last Updated): 2026-02-27 18:00:27

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->



## @FILES
<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[_AI.md](_AI.md#L1)**: Context: core
*   **[__init__.py](__init__.py#L1)**: Core: Infrastructure Utilities.
*   **[bootstrap.py](bootstrap.py#L1)** @DEP: src/ndoc/core/capabilities.py, src/ndoc/core/logger.py
    *   `@API`
        *   `PUB:` FUN **ensure_cli_environment**`() -> None`
        *   `PRV:` FUN _ensure_cli_shim`() -> None`
        *   `PRV:` FUN _get_user_bin_dir`() -> Path`
        *   `PRV:` FUN _ensure_path`(bin_dir: Path) -> None`
        *   `PRV:` FUN _persist_path`(bin_dir: Path) -> None`
        *   `PRV:` FUN _persist_path_windows`(bin_dir: Path) -> None`
        *   `PRV:` FUN _persist_path_unix`(bin_dir: Path) -> None`
        *   `PRV:` FUN _write_if_changed`(path: Path, content: str) -> None`
        *   `PRV:` FUN _is_stdio_mode`() -> bool`
*   **[cache.py](cache.py#L1)**: Atoms: Cache Management. @DEP: hashlib, json, pathlib, sqlite3, typing
    *   `@API`
        *   `PUB:` CLS **FileCache**
            *   `PRV:` MET __init__`(self, cache_dir: Path, db_name: str = "ndoc_cache.db")`
            *   `PRV:` MET _connect`(self)`
            *   `PRV:` MET _init_db`(self)`
            *   `PUB:` MET **load**`(self)`
            *   `PUB:` MET **save**`(self)`
            *   `PUB:` MET **close**`(self)`
            *   `PUB:` MET **get_file_hash**`(self, file_path: Path) -> str`
            *   `PUB:` MET **is_changed**`(self, file_path: Path) -> bool`
            *   `PUB:` MET **update**`(self, file_path: Path, result: Any)`
            *   `PUB:` MET **get**`(self, file_path: Path) -> Optional[Any]`
*   **[capabilities.py](capabilities.py#L1)**: Atoms: Capability Manager. @DEP: src/ndoc/__init__.py, src/ndoc/core/logger.py
    *   `@API`
        *   `PUB:` CLS **CapabilityManager**
            *   `VAL->` VAR **LANGUAGE_PACKAGES**`: Dict[str, str] = {
        "python": "tree-sitter-python",
        "javascrip...`
            *   `VAL->` VAR **OPTIONAL_PACKAGES**`: Dict[str, str] = {
        "chromadb": "chromadb",
    }`
            *   `VAL->` VAR _CACHE`: Dict[str, Optional[Language]] = {}`
            *   `VAL->` VAR _FAILED_INSTALLS`: Set[str] = set()`
            *   `VAL->` VAR _LOCAL_LIB_DIR`: Optional[Path] = None`
            *   `VAL->` VAR _TREE_SITTER_BOOTSTRAPPED`: bool = False`
            *   `PRV:` CLM _get_lib_dir`(cls) -> Path`
            *   `PRV:` CLM _init_local_lib`(cls) -> None`
            *   `VAL->` VAR _LOCK_FILE_DIR`: Path = Path(tempfile.gettempdir()) / "ndoc_locks"`
            *   `VAL->` VAR _LOCK_TTL_SECONDS`: int = 3600`
            *   `PRV:` CLM _is_locked`(cls, package_name: str) -> bool`
            *   `PRV:` CLM _set_lock`(cls, package_name: str) -> None`
            *   `PUB:` CLM **ensure_package**`(cls, package_name: str, auto_install: bool = True) -> bool`
            *   `PUB:` CLM **ensure_languages**`(cls, lang_names: Set[str], auto_install: bool = True) -> None`
            *   `PUB:` CLM **get_language**`(cls, lang_name: str, auto_install: bool = False, check_only: bool = False) -> Optional[Language]`
            *   `PRV:` STA _try_import`(lang_name: str) -> Optional[Language]`
            *   `PUB:` MET **make_language**`(ptr)`
            *   `PRV:` STA _has_dart_dll`() -> bool`
*   **[cli.py](cli.py#L1)**: Core: CLI Command Registry. @DEP: dataclasses, inspect, typing
    *   `@API`
        *   `PUB:` CLS **CommandInfo**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **help**`: str`
            *   `VAL->` VAR **handler**`: Callable`
            *   `VAL->` VAR **group**`: str = "General"`
        *   `PUB:` CLS **CommandRegistry**
            *   `VAL->` VAR _commands`: Dict[str, CommandInfo] = {}`
            *   `PUB:` CLM **register**`(cls, name: str, help: str, group: str = "General")`
            *   `PUB:` MET **decorator**`(func: Callable)`
            *   `PUB:` CLM **get_commands**`(cls) -> List[CommandInfo]`
            *   `PUB:` CLM **get_handler**`(cls, name: str) -> Optional[Callable]`
        *   `VAL->` VAR **ndoc_command**` = CommandRegistry.register`
*   **[errors.py](errors.py#L1)**: Custom exceptions for ndoc.
    *   `@API`
        *   `PUB:` CLS **NdocError**
        *   `PUB:` CLS **ConfigurationError**
        *   `PUB:` CLS **FileSystemError**
        *   `PUB:` CLS **ParsingError**
        *   `PUB:` CLS **DependencyError**
*   **[fs.py](fs.py#L1)**: Atoms: File System Traversal. @DEP: dataclasses, os, pathlib, pathspec, re, ...
    *   `@API`
        *   `PUB:` FUN **scan_project_files**`(root: Path, ignore_patterns: List[str], allow_extensions: Optional[Set[str]] = None) -> Iterator[Tuple[Path, str]]`
        *   `PRV:` FUN _infer_language`(path: Path) -> str`
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
*   **[graph.py](graph.py#L1)**: Core: Graph Algorithms. @DEP: collections, pathlib, typing
    *   `@API`
        *   `PUB:` FUN **calculate_metrics**`(graph: Dict[str, Set[str]]) -> Dict[str, Dict[str, float]]`
        *   `PUB:` FUN **find_circular_dependencies**`(graph: Dict[str, Set[str]]) -> List[List[str]]`
        *   `PUB:` FUN **strongconnect**`(v)`
*   **[io.py](io.py#L1)**: Atoms: Input/Output Operations. @DEP: datetime, difflib, os, pathlib, re, ...
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
*   **[logger.py](logger.py#L1)**: Standardized logging for ndoc. @DEP: logging, sys, typing
    *   `@API`
        *   `VAL->` VAR **LOG_FORMAT**` = "%(levelname)s: %(message)s"`
        *   `VAL->` VAR **DEBUG_LOG_FORMAT**` = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"`
        *   `PUB:` FUN **setup_logger**`(name: str = "ndoc", level: int = logging.INFO) -> logging.Logger`
        *   `VAL->` VAR **logger**` = setup_logger()`
        *   `PUB:` FUN **set_log_level**`(level: int)`
*   **[native_builder.py](native_builder.py#L1)**: Native Builder: Handles local compilation of language bindings on Windows. @DEP: src/ndoc/core/logger.py
    *   `@API`
        *   `PUB:` FUN **find_vcvars64**`() -> Optional[str]`
        *   `PUB:` FUN **ensure_dart_source**`(work_dir: Path) -> bool`
        *   `PUB:` FUN **build_dart_dll**`(output_path: Path) -> bool`
*   **[stats.py](stats.py#L1)**: Core: Project Statistics. @DEP: src/ndoc/core/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **should_update_stats**`(root_path: Path, force: bool) -> bool`
        *   `PUB:` FUN **collect_full_stats**`(config: ProjectConfig) -> Dict`
*   **[task_manager.py](task_manager.py#L1)**: Core: Task Management. @DEP: src/ndoc/core/__init__.py, src/ndoc/core/logger.py, src/ndoc/models/status.py, src/ndoc/parsing/__init__.py
    *   `@API`
        *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]`
        *   `PUB:` FUN **sync_task_checkboxes**`(target_file: Path, todos: List[TodoItem], log_prefix: Optional[str] = None) -> bool`
        *   `PUB:` FUN **remove_stats_section**`(status_file: Path) -> bool`
*   **[templates.py](templates.py#L1)** @DEP: src/ndoc/core/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `VAL->` VAR _CONFIG`: Optional[TemplateConfig] = None`
        *   `VAL->` VAR _ENV`: Optional[Environment] = None`
        *   `PUB:` FUN **configure**`(config: TemplateConfig) -> None`
        *   `PUB:` FUN **get_template**`(name: str) -> str`
        *   `PUB:` FUN **render_document**`(body_template_name: str, title: str, context: str, tags: str, timestamp: str, **body_kwargs) -> str`
*   **[text_utils.py](text_utils.py#L1)**: Atoms: Text Processing Utilities. @DEP: src/ndoc/models/context.py
    *   `@API`
        *   `VAL->` VAR **TAG_REGEX**` = re.compile(
    r"(?m)^\s*(?:#+|//|<!--|>|\*)\s*([@!][a-zA-Z...`
        *   `PUB:` FUN **clean_docstring**`(raw: str) -> str`
        *   `PUB:` FUN **extract_attributes**`(attr_str: str) -> dict`
        *   `PUB:` FUN **extract_tags_from_text**`(text: str, line_offset: int = 0) -> List[Tag]`
*   **[transforms.py](transforms.py#L1)**: Core: Data Transforms. @DEP: src/ndoc/core/__init__.py, src/ndoc/models/config.py, src/ndoc/models/context.py, src/ndoc/parsing/deps/test_mapper.py
    *   `@API`
        *   `PUB:` FUN **inject_test_usages**`(f_ctx: FileContext, test_mapper: TestUsageMapper, config: ProjectConfig)`
        *   `PUB:` FUN **inject_header_to_file**`(file_path: Path, header_content: str) -> bool`
<!-- NIKI_AUTO_Context_END -->

---
*Generated by Niki-docAI*
