# Context: flows
> @CONTEXT: Recursive Context | flows | @TAGS: @AI
> 最后更新 (Last Updated): 2026-02-27 18:00:27

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->



## @FILES
<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[_AI.md](_AI.md#L1)**: Context: flows
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: .
*   **[adr_flow.py](adr_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[arch_flow.py](arch_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, editors/vscode/editors/vscode/server/ndoc/flows/__init__.py, ...
    *   `@API`
        *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str`
        *   `PUB:` FUN **format_file_entry**`(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str`
        *   `PUB:` FUN **extract_file_summary**`(path: Path) -> str`
        *   `PUB:` FUN **build_tree_lines**`(current_path: Path, root: Path, ignore_patterns: List[str], level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]`
        *   `PUB:` FUN **generate_bom_section**`(root: Path, ignore_patterns: List[str]) -> str`
        *   `PUB:` FUN **generate_tech_section**`(root: Path, ignore_patterns: List[str]) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[archive_flow.py](archive_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/brain/vectordb.py, editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[capability_flow.py](capability_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, auto_install: bool = True) -> bool`
        *   `PUB:` FUN **check_single_file**`(file_path: Path, auto_install: bool = True)`
*   **[check_flow.py](check_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/brain/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/models/context.py, ...
    *   `@API`
        *   `PRV:` FUN _to_context`(scan_result: scanner.ScanResult, path: Path, root: Path) -> FileContext`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: Optional[str] = None) -> bool`
*   **[clean_flow.py](clean_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: src/ndoc/core/cli.py, src/ndoc/models/config.py
    *   `@API`
        *   `VAL->` VAR **GENERATED_FILES**` = [
    "_AI.md",
    "_MAP.md",
    "_DEPS.md",
    "_NEXT.md...`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None, force: bool = False) -> bool`
*   **[config_flow.py](config_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, editors/vscode/editors/vscode/server/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **load_project_config**`(root_path: Path) -> ProjectConfig`
        *   `PUB:` FUN **ensure_rules_file**`(root_path: Path, force: bool = False) -> bool`
        *   `PUB:` FUN **ensure_guide_file**`(root_path: Path, force: bool = False) -> bool`
        *   `PRV:` FUN _parse_rules`(file_path: Path, config: ProjectConfig) -> None`
        *   `PRV:` FUN _parse_command_list`(raw: str) -> List[str]`
*   **[context_flow.py](context_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/brain/__init__.py, editors/vscode/editors/vscode/server/ndoc/brain/vectordb.py, editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, ...
    *   `@API`
        *   `PUB:` FUN **cleanup_legacy_map**`(file_path: Path) -> None`
        *   `PUB:` FUN **process_directory**`(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False, test_mapper: Optional[TestUsageMapper] = None, vectordb: Optional[VectorDB] = None) -> Optional[DirectoryContext]`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PUB:` FUN **update_directory**`(path: Path, config: ProjectConfig) -> bool`
*   **[data_flow.py](data_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/models/context.py, ...
    *   `@API`
        *   `PUB:` CLS **DataDefinition**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **path**`: str`
            *   `VAL->` VAR **docstring**`: str`
            *   `VAL->` VAR **fields**`: List[str]`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PUB:` FUN **get_plural**`(name: str) -> str`
*   **[deps_flow.py](deps_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None) -> bool`
*   **[doctor_flow.py](doctor_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/capabilities.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _pass`(msg: str)`
        *   `PRV:` FUN _fail`(msg: str)`
        *   `PRV:` FUN _warn`(msg: str)`
        *   `PRV:` FUN _check_import`(module_name: str) -> bool`
        *   `PRV:` FUN _check_tree_sitter_bindings`(required_langs: set = None) -> bool`
        *   `PRV:` FUN _check_project_files`(config: ProjectConfig)`
*   **[impact_flow.py](impact_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py, ...
    *   `@API`
        *   `PUB:` FUN **get_changed_files**`(root: Path) -> List[str]`
        *   `PUB:` FUN **build_reverse_graph**`(graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]`
        *   `PUB:` FUN **find_impacted_nodes**`(changed_modules: List[str], rev_graph: Dict[str, Set[str]]) -> Set[str]`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[init_flow.py](init_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/cli.py, src/ndoc/flows/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[inject_flow.py](inject_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py, ...
    *   `@API`
        *   `PUB:` FUN **process_file**`(file_path: Path, root: Path) -> bool`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None)`
*   **[lesson_flow.py](lesson_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py
    *   `@API`
        *   `PUB:` FUN **run_check**`(config: ProjectConfig, target_files: List[str] = None) -> bool`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[map_flow.py](map_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, editors/vscode/editors/vscode/server/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[mind_flow.py](mind_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[prompt_flow.py](prompt_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/brain/vectordb.py, editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, ...
    *   `@API`
        *   `PUB:` FUN **get_context_prompt**`(file_path: str, config: ProjectConfig, focus: bool = False, use_skeleton: bool = False) -> str`
        *   `PUB:` FUN **run**`(file_path: str, config: ProjectConfig, focus: bool = False) -> bool`
*   **[quality_flow.py](quality_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, src/ndoc/models/config.py
    *   `@API`
        *   `PRV:` FUN _run_commands`(label: str, commands: List[str], root_path: Path) -> bool`
        *   `PUB:` FUN **run_lint**`(config: ProjectConfig) -> bool`
        *   `PUB:` FUN **run_typecheck**`(config: ProjectConfig) -> bool`
*   **[search_flow.py](search_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/brain/vectordb.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, editors/vscode/editors/vscode/server/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, query: str, limit: int = 5) -> bool`
*   **[status_flow.py](status_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, editors/vscode/editors/vscode/server/ndoc/models/config.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[syntax_flow.py](syntax_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/templates.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[update_flow.py](update_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py
    *   `@API`
        *   `PRV:` FUN _is_git_repo`(path: Path) -> bool`
        *   `PUB:` FUN **run**`() -> bool`
*   **[verify_flow.py](verify_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: editors/vscode/editors/vscode/server/ndoc/core/__init__.py, editors/vscode/editors/vscode/server/ndoc/core/cli.py, editors/vscode/editors/vscode/server/ndoc/core/logger.py, editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, fs_module=fs, io_module=io, scanner_module=scanner, logger_instance=logger) -> bool`
        *   `PRV:` FUN _verify_rules_content`(config: ProjectConfig, io_module, logger_instance) -> bool`
        *   `PRV:` FUN _check_architecture`(config: ProjectConfig, fs_module, io_module, scanner_module, logger_instance) -> bool`
<!-- NIKI_AUTO_Context_END -->

---
*Generated by Niki-docAI*
