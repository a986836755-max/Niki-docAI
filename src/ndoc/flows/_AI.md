# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 15:34:10

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Dynamic Capability Loading**: New flows (like `capability_flow.py`) must be registered in `entry.py` to ensure they are executed during the relevant lifecycle phases (e.g., `init`, `map`, `all`).
*   **Auto-Provisioning**: `capability_flow` acts as the project's "immune system", proactively detecting and installing missing language capabilities based on file extensions. This logic should remain lightweight and idempotent.
*   **Doctor Integration**: `doctor_flow` should reuse the `CapabilityManager` logic to verify system health, rather than implementing redundant checks.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """
*   **[archive_flow.py](archive_flow.py#L1)**: """ @DEP: re, datetime, pathlib, models.config, atoms
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _extract_memory`(config: ProjectConfig, archived_content: list, memory_file: Path)`
*   **[capability_flow.py](capability_flow.py#L1)**: """ @DEP: pathlib, models.config, typing, atoms
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, auto_install: bool = True) -> bool`
        *   `PUB:` FUN **check_single_file**`(file_path: Path, auto_install: bool = True)`
*   **[clean_flow.py](clean_flow.py#L1)**: """ @DEP: pathlib, ndoc.models.config, os, typing
    *   `@API`
        *   `VAL->` VAR **GENERATED_FILES**` = [
    "_AI.md",
    "_MAP.md",
    "_TECH.md",
    "_DEPS.md...`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None, force: bool = False) -> bool`
*   **[config_flow.py](config_flow.py#L1)**: """ @DEP: re, pathlib, ndoc.models.config, ndoc.atoms, typing
    *   `@API`
        *   `VAL->` VAR **RULES_TEMPLATE**` = """# Project Rules
> @CONTEXT: Configuration | @TAGS: @CONFI...`
        *   `PUB:` FUN **load_project_config**`(root_path: Path) -> ProjectConfig`
        *   `PUB:` FUN **ensure_rules_file**`(root_path: Path, force: bool = False) -> bool`
        *   `PRV:` FUN _parse_rules`(file_path: Path, config: ProjectConfig) -> None`
*   **[context_flow.py](context_flow.py#L1)**: """ @DEP: re, datetime, pathlib, models.config, atoms, models.context, typing, dataclasses
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
*   **[data_flow.py](data_flow.py#L1)**: """ @DEP: datetime, pathlib, models.config, atoms, models.context, typing, dataclasses
    *   `@API`
        *   `PUB:` CLS **DataDefinition**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **path**`: str`
            *   `VAL->` VAR **docstring**`: str`
            *   `VAL->` VAR **fields**`: List[str]`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PUB:` FUN **get_plural**`(name: str) -> str`
*   **[deps_flow.py](deps_flow.py#L1)**: """ @DEP: datetime, pathlib, models.config, atoms, typing, collections
    *   `@API`
        *   `PUB:` FUN **collect_imports**`(root: Path) -> Dict[str, List[str]]`
        *   `PUB:` FUN **build_dependency_graph**`(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]`
        *   `PUB:` FUN **generate_mermaid_graph**`(graph: Dict[str, Set[str]]) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[doctor_flow.py](doctor_flow.py#L1)**: """ @DEP: sys, platform, pathlib, atoms.capabilities, ndoc.models.config, typing, importlib, tree_sitter ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _pass`(msg: str)`
        *   `PRV:` FUN _fail`(msg: str)`
        *   `PRV:` FUN _warn`(msg: str)`
        *   `PRV:` FUN _check_import`(module_name: str) -> bool`
        *   `PRV:` FUN _check_tree_sitter_bindings`() -> bool`
        *   `PRV:` FUN _check_project_files`(config: ProjectConfig)`
*   **[init_flow.py](init_flow.py#L1)**: """ @DEP: ndoc.models.config, ndoc.flows
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[map_flow.py](map_flow.py#L1)**: """ @DEP: datetime, pathlib, models.config, concurrent.futures, atoms, typing, dataclasses
    *   `@API`
        *   `PUB:` CLS **MapContext**
            *   `VAL->` VAR **root**`: Path`
            *   `VAL->` VAR **ignore_patterns**`: List[str]`
        *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str`
        *   `PUB:` FUN **format_file_entry**`(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str`
        *   `PUB:` FUN **extract_file_summary**`(path: Path) -> str`
        *   `PUB:` FUN **build_tree_lines**`(current_path: Path, context: MapContext, level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]`
        *   `PUB:` FUN **generate_tree_content**`(config: ProjectConfig) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[plan_flow.py](plan_flow.py#L1)**: """ @DEP: pathlib, models.config, datetime, atoms
    *   `@API`
        *   `VAL->` VAR **PLAN_SYSTEM_PROMPT**` = """
You are a senior software architect and project manager....`
        *   `PUB:` FUN **run**`(config: ProjectConfig, objective: str) -> bool`
*   **[prompt_flow.py](prompt_flow.py#L1)**: """ @DEP: re, pathlib, models.config, atoms, typing
    *   `@API`
        *   `VAL->` VAR **RULE_MARKER**` = "## !RULE"`
        *   `VAL->` VAR **CTX_START**` = "<!-- NIKI_CTX_START -->"`
        *   `PUB:` FUN **extract_rules_from_ai**`(ai_path: Path) -> str`
        *   `PUB:` FUN **get_context_prompt**`(file_path: Path, config: ProjectConfig) -> str`
        *   `PUB:` FUN **run**`(file_path: str, config: ProjectConfig) -> bool`
*   **[stats_flow.py](stats_flow.py#L1)**: """ @DEP: re, datetime, pathlib, time, os, ndoc.models.config, ndoc.atoms
    *   `@API`
        *   `PUB:` FUN **check_should_update**`(root_path: Path, force: bool) -> bool`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[symbols_flow.py](symbols_flow.py#L1)**: """ @DEP: datetime, pathlib, models.config, atoms, models.context, typing, collections
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _get_kind_icon`(kind: str) -> str`
*   **[syntax_flow.py](syntax_flow.py#L1)**: """ @DEP: pathlib, ndoc.models.config, ndoc.atoms
    *   `@API`
        *   `VAL->` VAR **SYNTAX_TEMPLATE**` = r"""# PROJECT SYNTAX
> @CONTEXT: DSL 定义 | @TAGS: @SYNTAX @OP...`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[tech_flow.py](tech_flow.py#L1)**: """ @DEP: pathlib, ndoc.models.config, ndoc.atoms, datetime
    *   `@API`
        *   `PUB:` FUN **generate_tech_content**`(config: ProjectConfig) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[todo_flow.py](todo_flow.py#L1)**: """ @DEP: re, datetime, pathlib, models.config, atoms, typing, dataclasses
    *   `@API`
        *   `PUB:` CLS **TodoItem**
            *   `VAL->` VAR **file_path**`: Path`
            *   `VAL->` VAR **line**`: int`
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **content**`: str`
            *   `VAL->` VAR **task_id**`: Optional[str] = None`
            *   `GET->` PRP **priority_icon**`(self) -> str`
        *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]`
        *   `PUB:` FUN **format_todo_lines**`(todos: List[TodoItem], root: Path) -> str`
        *   `PUB:` FUN **sync_tasks**`(config: ProjectConfig, todos: List[TodoItem]) -> bool`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[update_flow.py](update_flow.py#L1)**: """ @DEP: pathlib, sys, subprocess, typing
    *   `@API`
        *   `PRV:` FUN _is_git_repo`(path: Path) -> bool`
        *   `PUB:` FUN **run**`() -> bool`
*   **[verify_flow.py](verify_flow.py#L1)**: """ @DEP: sys, ndoc.models.config, atoms
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _verify_rules_content`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _check_architecture`(config: ProjectConfig) -> bool`
<!-- NIKI_AUTO_Context_END -->
