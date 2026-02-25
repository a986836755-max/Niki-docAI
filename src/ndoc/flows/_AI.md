# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:50

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->
### Auto-Detected Rules
*   **RULE**: @LAYER(core) CANNOT_IMPORT @LAYER(ui) --> [context_flow.py:465](context_flow.py#L465)
*   **RULE**: @FORBID(hardcoded_paths) --> [context_flow.py:466](context_flow.py#L466)
<!-- NIKI_AUTO_MEMORIES_END -->
*   **Dynamic Capability Loading**: New flows (like `capability_flow.py`) must be registered in `entry.py` to ensure they are executed during the relevant lifecycle phases (e.g., `init`, `map`, `all`).
*   **Auto-Provisioning**: `capability_flow` acts as the project's "immune system", proactively detecting and installing missing language capabilities based on file extensions. This logic should remain lightweight and idempotent.
*   **Modular Architecture**: The project now follows a layered architecture:
    *   `core/`: Infrastructure (FS, IO, Capabilities)
    *   `parsing/`: Code analysis (Scanner, AST, Deps, Langs)
    *   `brain/`: Intelligence (Index, Memory, Checker, LLM)
    *   `interfaces/`: Entry points (LSP, Daemon)
    *   `flows/`: Business logic (Context, Arch, Check, etc.)
*   **Architecture Split**: `arch_flow` now generates three separate files:
    *   `_ARCH.md`: High-level technology stack and Third-Party Dependencies (BOM).
    *   `_MAP.md`: Detailed file structure tree.
    *   `_DEPS.md`: Component Relationships with Instability Metrics (Ca/Ce/I) and Layered Topology.
*   **Universal AST Adapter**: `universal.py` uses `_LANGS.json` to drive multi-language dependency extraction (Python, JS, Java, C++, etc.), replacing the previous Python-only regex approach.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START>
*   **[adr_flow.py](adr_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: collections, typing, models.config, pathlib, parsing, core
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[arch_flow.py](arch_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: collections, typing, models.config, pathlib, parsing, concurrent.futures, core, datetime
    *   `@API`
        *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str` [🔗6]
        *   `PUB:` FUN **format_file_entry**`(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str` [🔗6]
        *   `PUB:` FUN **extract_file_summary**`(path: Path) -> str` [🔗6]
        *   `PUB:` FUN **build_tree_lines**`(current_path: Path, root: Path, ignore_patterns: List[str], level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]` [🔗8]
        *   `PUB:` FUN **analyze_dependencies**`(root: Path, ignore_patterns: List[str]) -> Dict[str, Set[str]]` [🔗2]
        *   `PUB:` FUN **calculate_metrics**`(graph: Dict[str, Set[str]]) -> Dict[str, Dict[str, float]]` [🔗2]
        *   `PUB:` FUN **generate_instability_table**`(metrics: Dict[str, Dict[str, float]]) -> str` [🔗2]
        *   `PUB:` FUN **generate_dependency_matrix**`(graph: Dict[str, Set[str]], modules: List[str]) -> str` [🔗2]
        *   `PUB:` FUN **build_dependency_report**`(root: Path, ignore_patterns: List[str]) -> str` [🔗3]
        *   `PUB:` FUN **build_dependency_mermaid**`(root: Path) -> str` [🔗2]
        *   `PUB:` FUN **generate_bom_section**`(root: Path, ignore_patterns: List[str]) -> str` [🔗2]
        *   `PUB:` FUN **generate_tech_section**`(root: Path, ignore_patterns: List[str]) -> str` [🔗3]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[archive_flow.py](archive_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: atoms, brain.vectordb, typing, models.config, pathlib, datetime
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[capability_flow.py](capability_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: pathlib, typing, models.config, atoms
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, auto_install: bool = True) -> bool` [🔗2341] ↳ Usage: [tests/test_capability_flow.py#L28]
        *   `PUB:` FUN **check_single_file**`(file_path: Path, auto_install: bool = True)` [🔗5] ↳ Usage: [tests/test_capability_flow.py#L47], [tests/test_capability_flow.py#L41]
*   **[check_flow.py](check_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: typing, models.config, models.context, pathlib, parsing, brain, core
    *   `@API`
        *   `PRV:` FUN _to_context`(scan_result: scanner.ScanResult, path: Path, root: Path) -> FileContext` [🔗5]
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: Optional[str] = None) -> bool` [🔗2341]
*   **[clean_flow.py](clean_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: pathlib, typing, ndoc.models.config, os
    *   `@API`
        *   `VAL->` VAR **GENERATED_FILES**` = [
    "_AI.md",
    "_MAP.md",
    "_TECH.md",
    "_DEPS.md...` [🔗4]
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None, force: bool = False) -> bool` [🔗2341]
*   **[config_flow.py](config_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, typing, ndoc.models.config, pathlib, ndoc.atoms
    *   `@API`
        *   `VAL->` VAR **RULES_TEMPLATE**` = """# Project Rules
> @CONTEXT: Configuration | @TAGS: @CONFI...` [🔗3]
        *   `PUB:` FUN **load_project_config**`(root_path: Path) -> ProjectConfig` [🔗3]
        *   `PUB:` FUN **ensure_rules_file**`(root_path: Path, force: bool = False) -> bool` [🔗4]
        *   `PRV:` FUN _parse_rules`(file_path: Path, config: ProjectConfig) -> None` [🔗3]
*   **[context_flow.py](context_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, parsing.ast, brain.vectordb, typing, models.config, models.context, test_map_flow, pathlib ...
    *   `@API`
        *   `PUB:` FUN **format_file_summary**`(ctx: FileContext, root: Optional[Path] = None) -> str` [🔗3]
        *   `PUB:` FUN **format_symbol_list**`(ctx: FileContext, use_skeleton: bool = False) -> str` [🔗3]
        *   `PRV:` FUN _format_single_symbol`(sym, level: int)` [🔗4]
        *   `PUB:` FUN **format_dependencies**`(ctx: FileContext) -> str` [🔗3]
        *   `PUB:` FUN **generate_dir_content**`(context: DirectoryContext) -> str` [🔗3]
        *   `PUB:` FUN **cleanup_legacy_map**`(file_path: Path) -> None` [🔗3]
        *   `PRV:` FUN _inject_test_usages`(f_ctx: FileContext, test_mapper: TestUsageMapper, config: ProjectConfig)` [🔗3]
        *   `PUB:` FUN **process_directory**`(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False, test_mapper: Optional[TestUsageMapper] = None, vectordb: Optional[VectorDB] = None) -> Optional[DirectoryContext]` [🔗5]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
        *   `PUB:` FUN **update_directory**`(path: Path, config: ProjectConfig) -> bool` [🔗3]
*   **[data_flow.py](data_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: atoms, typing, models.config, models.context, pathlib, dataclasses, datetime
    *   `@API`
        *   `PUB:` CLS **DataDefinition** [🔗5]
            *   `VAL->` VAR **name**`: str` [🔗25070]
            *   `VAL->` VAR **type**`: str` [🔗33686]
            *   `VAL->` VAR **path**`: str` [🔗8904]
            *   `VAL->` VAR **docstring**`: str` [🔗71]
            *   `VAL->` VAR **fields**`: List[str]` [🔗1474]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
        *   `PUB:` FUN **get_plural**`(name: str) -> str` [🔗3]
*   **[deps_flow.py](deps_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: collections, atoms, typing, models.config, pathlib, parsing, datetime
    *   `@API`
        *   `PUB:` FUN **collect_imports**`(root: Path) -> Dict[str, List[str]]` [🔗7]
        *   `PUB:` FUN **build_dependency_graph**`(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]` [🔗8]
        *   `PUB:` FUN **generate_mermaid_graph**`(graph: Dict[str, Set[str]]) -> str` [🔗3]
        *   `PUB:` FUN **find_circular_dependencies**`(graph: Dict[str, Set[str]]) -> List[List[str]]` [🔗4]
        *   `PUB:` FUN **strongconnect**`(v)` [🔗3]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[doctor_flow.py](doctor_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: shutil, typing, core.capabilities, sys, platform, models.config, pathlib, parsing ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
        *   `PRV:` FUN _pass`(msg: str)` [🔗8]
        *   `PRV:` FUN _fail`(msg: str)` [🔗6]
        *   `PRV:` FUN _warn`(msg: str)` [🔗5]
        *   `PRV:` FUN _check_import`(module_name: str) -> bool` [🔗3]
        *   `PRV:` FUN _check_tree_sitter_bindings`() -> bool` [🔗3]
        *   `PRV:` FUN _check_project_files`(config: ProjectConfig)` [🔗3]
*   **[impact_flow.py](impact_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: collections, deps_flow, typing, models.config, pathlib, parsing, subprocess
    *   `@API`
        *   `PUB:` FUN **get_changed_files**`(root: Path) -> List[str]` [🔗2]
        *   `PUB:` FUN **build_reverse_graph**`(graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]` [🔗2]
        *   `PUB:` FUN **find_impacted_nodes**`(changed_modules: List[str], rev_graph: Dict[str, Set[str]]) -> Set[str]` [🔗2]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[init_flow.py](init_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.flows, ndoc.models.config
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool` [🔗2341]
*   **[inject_flow.py](inject_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, atoms, typing, models.config, pathlib
    *   `@API`
        *   `VAL->` VAR **HEADER_START_TAG**` = "# <NIKI_AUTO_HEADER_START>\n"` [🔗4]
        *   `VAL->` VAR **HEADER_END_TAG**` = "# <NIKI_AUTO_HEADER_END>\n"` [🔗3]
        *   `VAL->` VAR **HEADER_START**` = f"{HEADER_START_TAG}# --------------------------------------...` [🔗3]
        *   `VAL->` VAR **HEADER_END**` = f"# --------------------------------------------------------...` [🔗3]
        *   `VAL->` VAR **RULE_REGEX**` = re.compile(r"##\s+!(RULE|CONST)(.*?)(?=\n##|\Z)", re.DOTALL)` [🔗2]
        *   `PUB:` FUN **extract_summary_rules**`(ai_path: Path) -> List[str]` [🔗3]
        *   `PUB:` FUN **generate_header**`(file_path: Path, config: ProjectConfig) -> str` [🔗3]
        *   `PUB:` FUN **inject_file**`(file_path: Path, config: ProjectConfig) -> bool` [🔗5]
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None)` [🔗2341]
*   **[lesson_flow.py](lesson_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: typing, models.config, pathlib, parsing, core
    *   `@API`
        *   `PUB:` FUN **run_check**`(config: ProjectConfig, target_files: List[str] = None) -> bool` [🔗2]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[map_flow.py](map_flow.py#L1)**: ------------------------------------------------------------------------------ @DEP: atoms, typing, models.config, pathlib, dataclasses, concurrent.futures, datetime
    *   `@API`
        *   `PUB:` CLS **MapContext** [🔗6]
            *   `VAL->` VAR **root**`: Path` [🔗1951]
            *   `VAL->` VAR **ignore_patterns**`: List[str]` [🔗97]
        *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str` [🔗6]
        *   `PUB:` FUN **format_file_entry**`(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str` [🔗6]
        *   `PUB:` FUN **extract_file_summary**`(path: Path) -> str` [🔗6]
        *   `PUB:` FUN **build_tree_lines**`(current_path: Path, context: MapContext, level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]` [🔗8]
        *   `PUB:` FUN **generate_tree_content**`(config: ProjectConfig) -> str` [🔗3]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[mind_flow.py](mind_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: collections, typing, models.config, pathlib, parsing, core
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[plan_flow.py](plan_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: models.config, pathlib, datetime, atoms
    *   `@API`
        *   `VAL->` VAR **PLAN_SYSTEM_PROMPT**` = """
You are a senior software architect and project manager....` [🔗3]
        *   `PUB:` FUN **run**`(config: ProjectConfig, objective: str) -> bool` [🔗2341]
*   **[prompt_flow.py](prompt_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, parsing.ast, atoms, brain.vectordb, typing, models.config, models.context, pathlib
    *   `@API`
        *   `VAL->` VAR **RULE_MARKER**` = "## !RULE"` [🔗2]
        *   `VAL->` VAR **CTX_START**` = "<!-- NIKI_CTX_START -->"` [🔗2]
        *   `PUB:` FUN **get_context_prompt**`(file_path: Path, config: ProjectConfig, focus: bool = False, use_skeleton: bool = False) -> str` [🔗5]
        *   `PRV:` FUN _get_full_context`(file_path: Path, root: Path) -> str` [🔗3]
        *   `PUB:` FUN **run**`(file_path: str, config: ProjectConfig, focus: bool = False) -> bool` [🔗2341]
*   **[stats_flow.py](stats_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, time, ndoc.models.config, os, pathlib, ndoc.atoms, datetime
    *   `@API`
        *   `PUB:` FUN **check_should_update**`(root_path: Path, force: bool) -> bool` [🔗3]
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool` [🔗2341]
*   **[status_flow.py](status_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, deps_flow, atoms, typing, os, models.config, pathlib, dataclasses ...
    *   `@API`
        *   `PUB:` CLS **TodoItem** [🔗20]
            *   `VAL->` VAR **file_path**`: Path` [🔗236]
            *   `VAL->` VAR **line**`: int` [🔗3227]
            *   `VAL->` VAR **type**`: str` [🔗33686]
            *   `VAL->` VAR **content**`: str` [🔗2268]
            *   `VAL->` VAR **task_id**`: Optional[str] = None` [🔗30]
            *   `GET->` PRP **priority_icon**`(self) -> str` [🔗6]
        *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]` [🔗6]
        *   `PUB:` FUN **format_todo_lines**`(todos: List[TodoItem], root: Path) -> str` [🔗6]
        *   `PUB:` FUN **sync_tasks**`(status_file: Path, todos: List[TodoItem]) -> bool` [🔗6]
        *   `PUB:` FUN **calculate_stats**`(root_path: Path, ignore_patterns: List[str]) -> Dict` [🔗3]
        *   `PUB:` FUN **generate_stats_section**`(stats: Dict, root: Path = None) -> str` [🔗3]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[symbols_flow.py](symbols_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: collections, atoms, typing, models.config, models.context, pathlib, datetime
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
        *   `PRV:` FUN _get_kind_icon`(kind: str) -> str` [🔗3]
*   **[syntax_flow.py](syntax_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: pathlib, ndoc.models.config, ndoc.atoms
    *   `@API`
        *   `VAL->` VAR **SYNTAX_TEMPLATE**` = r"""# PROJECT SYNTAX
> @CONTEXT: DSL 定义 | @TAGS: @SYNTAX @OP...` [🔗3]
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool` [🔗2341]
*   **[test_map_flow.py](test_map_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: typing, ndoc.models.config, pathlib, ast, ndoc.parsing.ast.discovery, ndoc.core.fs, ndoc.parsing.ast, ndoc.core.io
    *   `@API`
        *   `PUB:` CLS **TestUsageMapper** [🔗11]
            *   `PRV:` MET __init__`(self, config: ProjectConfig)` [🔗44]
            *   `PUB:` MET **scan**`(self)` [🔗280]
            *   `PRV:` MET _extract_import_aliases`(self, content: str) -> Dict[str, str]` [🔗3]
            *   `PRV:` MET _process_python_file`(self, file_path: Path)` [🔗3]
            *   `PRV:` MET _resolve_with_aliases`(self, call_name: str, import_map: Dict[str, str]) -> List[str]` [🔗3]
            *   `PUB:` MET **get_usages**`(self, symbol_full_name: str) -> List[Dict[str, Any]]` [🔗4]
        *   `PUB:` FUN **run_test_mapping**`(config: ProjectConfig) -> TestUsageMapper` [🔗4]
*   **[todo_flow.py](todo_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, atoms, typing, models.config, pathlib, dataclasses, datetime
    *   `@API`
        *   `PUB:` CLS **TodoItem** [🔗20]
            *   `VAL->` VAR **file_path**`: Path` [🔗236]
            *   `VAL->` VAR **line**`: int` [🔗3227]
            *   `VAL->` VAR **type**`: str` [🔗33686]
            *   `VAL->` VAR **content**`: str` [🔗2268]
            *   `VAL->` VAR **task_id**`: Optional[str] = None` [🔗30]
            *   `GET->` PRP **priority_icon**`(self) -> str` [🔗6]
        *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]` [🔗6]
        *   `PUB:` FUN **format_todo_lines**`(todos: List[TodoItem], root: Path) -> str` [🔗6]
        *   `PUB:` FUN **sync_tasks**`(config: ProjectConfig, todos: List[TodoItem]) -> bool` [🔗6]
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
*   **[update_flow.py](update_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: pathlib, typing, sys, subprocess
    *   `@API`
        *   `PRV:` FUN _is_git_repo`(path: Path) -> bool` [🔗4]
        *   `PUB:` FUN **run**`() -> bool` [🔗2341]
*   **[verify_flow.py](verify_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: atoms, ndoc.models.config, sys
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool` [🔗2341]
        *   `PRV:` FUN _verify_rules_content`(config: ProjectConfig) -> bool` [🔗3]
        *   `PRV:` FUN _check_architecture`(config: ProjectConfig) -> bool` [🔗3]
<!-- NIKI_AUTO_Context_END -->
