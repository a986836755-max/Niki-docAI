# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-30 19:25:16

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Flows: Business Logic Pipelines.
*   **[clean_flow.py](clean_flow.py#L1)**: Flow: Clean / Reset. @DEP: ndoc.models.config, os, pathlib, typing
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None, force: bool = False) -> bool`
*   **[config_flow.py](config_flow.py#L1)**: Flow: Configuration Loading. @DEP: ndoc.atoms, ndoc.models.config, pathlib, re, typing
    *   `@API`
        *   `PUB:` FUN **load_project_config**`(root_path: Path) -> ProjectConfig`
        *   `PUB:` FUN **ensure_rules_file**`(root_path: Path, force: bool = False) -> bool`
        *   `PRV:` FUN _parse_rules`(file_path: Path, config: ProjectConfig) -> None`
*   **[context_flow.py](context_flow.py#L1)**: Flow: Recursive Context Generation. @DEP: atoms, dataclasses, datetime, models.config, models.context, pathlib, re, typing
    *   `@API`
        *   `PUB:` FUN **format_file_summary**`(ctx: FileContext, root: Optional[Path] = None) -> str`
        *   `PUB:` FUN **format_symbol_list**`(ctx: FileContext) -> str`
        *   `PRV:` FUN _format_single_symbol`(sym, level: int)`
        *   `PUB:` FUN **format_dependencies**`(ctx: FileContext) -> str`
        *   `PUB:` FUN **generate_dir_content**`(context: DirectoryContext) -> str`
        *   `PUB:` FUN **cleanup_legacy_map**`(file_path: Path) -> None`
        *   `PUB:` FUN **process_directory**`(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False) -> Optional[DirectoryContext]`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PUB:` FUN **update_directory**`(path: Path, config: ProjectConfig) -> bool`
*   **[deps_flow.py](deps_flow.py#L1)**: Flow: Dependency Graph Generation. @DEP: atoms, collections, datetime, models.config, pathlib, typing
    *   `@API`
        *   `PUB:` FUN **collect_imports**`(root: Path) -> Dict[str, List[str]]`
        *   `PUB:` FUN **build_dependency_graph**`(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]`
        *   `PUB:` FUN **generate_mermaid_graph**`(graph: Dict[str, Set[str]]) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[doctor_flow.py](doctor_flow.py#L1)**: Flow: System Diagnostics. @DEP: importlib, ndoc.models.config, pathlib, platform, shutil, sys, tree_sitter, tree_sitter_python, typing
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _pass`(msg: str)`
        *   `PRV:` FUN _fail`(msg: str)`
        *   `PRV:` FUN _warn`(msg: str)`
        *   `PRV:` FUN _check_import`(module_name: str) -> bool`
        *   `PRV:` FUN _check_tree_sitter_bindings`() -> bool`
        *   `PRV:` FUN _check_project_files`(config: ProjectConfig)`
*   **[init_flow.py](init_flow.py#L1)**: Flow: Initialization. @DEP: ndoc.flows, ndoc.models.config
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[map_flow.py](map_flow.py#L1)**: Flow: Map Generation. @DEP: atoms, dataclasses, datetime, models.config, pathlib, typing
    *   `@API`
        *   `PUB:` CLS **MapContext**
            *   `VAL->` VAR **root**`: Path`
            *   `VAL->` VAR **ignore_patterns**`: List[str]`
        *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str`
        *   `PUB:` FUN **format_file_entry**`(path: Path, root: Path, level: int) -> str`
        *   `PUB:` FUN **build_tree_lines**`(current_path: Path, context: MapContext, level: int = 0) -> List[str]`
        *   `PUB:` FUN **generate_tree_content**`(config: ProjectConfig) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[stats_flow.py](stats_flow.py#L1)**: Flow: Statistics. @DEP: datetime, ndoc.atoms, ndoc.models.config, os, pathlib, re, time
    *   `@API`
        *   `PUB:` FUN **check_should_update**`(root_path: Path, force: bool) -> bool`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[syntax_flow.py](syntax_flow.py#L1)**: Flow: Syntax Manual Sync. @DEP: ndoc.atoms, ndoc.models.config, pathlib
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[tech_flow.py](tech_flow.py#L1)**: Flow: Tech Stack Snapshot Generation. @DEP: datetime, ndoc.atoms, ndoc.models.config, pathlib
    *   `@API`
        *   `PUB:` FUN **generate_tech_content**`(config: ProjectConfig) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[todo_flow.py](todo_flow.py#L1)**: Flow: Todo Aggregation. @DEP: atoms, dataclasses, datetime, models.config, pathlib, typing
    *   `@API`
        *   `PUB:` CLS **TodoItem**
            *   `VAL->` VAR **file_path**`: Path`
            *   `VAL->` VAR **line**`: int`
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **content**`: str`
            *   `GET->` PRP **priority_icon**`(self) -> str`
        *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]`
        *   `PUB:` FUN **format_todo_lines**`(todos: List[TodoItem], root: Path) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[update_flow.py](update_flow.py#L1)**: Flow: Self-Update Flow. @DEP: pathlib, subprocess, sys, typing
    *   `@API`
        *   `PRV:` FUN _is_git_repo`(path: Path) -> bool`
        *   `PUB:` FUN **run**`() -> bool`
*   **[verify_flow.py](verify_flow.py#L1)**: Flow: Verification. @DEP: ndoc.models.config, sys
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
<!-- NIKI_AUTO_Context_END -->
