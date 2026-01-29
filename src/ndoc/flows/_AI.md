# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-29 20:01:46

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py)**: Flows: Business Logic Pipelines.
*   **[clean_flow.py](clean_flow.py)**: Flow: Clean / Reset.
    *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None, force: bool = False) -> bool`
*   **[config_flow.py](config_flow.py)**: Flow: Configuration Loading.
    *   `PUB:` FUN **ensure_rules_file**`(root_path: Path, force: bool = False) -> bool`
    *   `PUB:` FUN **load_project_config**`(root_path: Path) -> ProjectConfig`
    *   `PRV:` FUN _parse_rules`(file_path: Path, config: ProjectConfig) -> None`
*   **[context_flow.py](context_flow.py)**: Flow: Recursive Context Generation.
    *   `PUB:` FUN **cleanup_legacy_map**`(file_path: Path) -> None`
    *   `PUB:` FUN **format_dependencies**`(ctx: FileContext) -> str`
    *   `PUB:` FUN **format_file_summary**`(ctx: FileContext) -> str`
    *   `PUB:` FUN **format_symbol_list**`(ctx: FileContext) -> str`
    *   `PUB:` FUN **generate_dir_content**`(context: DirectoryContext) -> str`
    *   `PUB:` FUN **process_directory**`(path: Path, config: ProjectConfig, recursive: bool = True) -> None`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
    *   `PUB:` FUN **update_directory**`(path: Path, config: ProjectConfig) -> bool`
    *   `PRV:` FUN _format_single_symbol`(sym, level: int)`
*   **[deps_flow.py](deps_flow.py)**: Flow: Dependency Graph Generation.
    *   `PUB:` FUN **build_dependency_graph**`(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]`
    *   `PUB:` FUN **collect_imports**`(root: Path) -> Dict[str, List[str]]`
    *   `PUB:` FUN **generate_mermaid_graph**`(graph: Dict[str, Set[str]]) -> str`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[doctor_flow.py](doctor_flow.py)**: Flow: System Diagnostics.
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
    *   `PRV:` FUN _check_import`(module_name: str) -> bool`
    *   `PRV:` FUN _check_project_files`(config: ProjectConfig)`
    *   `PRV:` FUN _check_tree_sitter_bindings`() -> bool`
    *   `PRV:` FUN _fail`(msg: str)`
    *   `PRV:` FUN _pass`(msg: str)`
    *   `PRV:` FUN _warn`(msg: str)`
*   **[init_flow.py](init_flow.py)**: Flow: Initialization.
    *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[map_flow.py](map_flow.py)**: Flow: Map Generation.
    *   `PUB:` CLS **MapContext**
    *   `PUB:` FUN **build_tree_lines**`(current_path: Path, context: MapContext, level: int = 0) -> List[str]`
    *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str`
    *   `PUB:` FUN **format_file_entry**`(path: Path, root: Path, level: int) -> str`
    *   `PUB:` FUN **generate_tree_content**`(config: ProjectConfig) -> str`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[stats_flow.py](stats_flow.py)**: Flow: Statistics.
    *   `PUB:` FUN **check_should_update**`(root_path: Path, force: bool) -> bool`
    *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[syntax_flow.py](syntax_flow.py)**: Flow: Syntax Manual Sync.
    *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[tech_flow.py](tech_flow.py)**: Flow: Tech Stack Snapshot Generation.
    *   `PUB:` FUN **generate_tech_content**`(config: ProjectConfig) -> str`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[todo_flow.py](todo_flow.py)**: Flow: Todo Aggregation.
    *   `PUB:` CLS **TodoItem**
    *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]`
    *   `PUB:` FUN **format_todo_lines**`(todos: List[TodoItem], root: Path) -> str`
    *   `GET->` VAR **priority_icon**`(self) -> str`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[update_flow.py](update_flow.py)**: Flow: Self-Update Flow.
    *   `PUB:` FUN **run**`() -> bool`
    *   `PRV:` FUN _is_git_repo`(path: Path) -> bool`
*   **[verify_flow.py](verify_flow.py)**: Flow: Verification.
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
<!-- NIKI_AUTO_Context_END -->
