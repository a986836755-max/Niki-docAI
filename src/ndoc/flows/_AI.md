# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py)**: Flows: Business Logic Pipelines.
*   **[context_flow.py](context_flow.py)**: Flow: Recursive Context Generation.
    *   `PUB:` FUN **cleanup_legacy_map**`(file_path: Path) -> None`
    *   `PUB:` FUN **format_dependencies**`(ctx: FileContext) -> str`
    *   `PUB:` FUN **format_file_summary**`(ctx: FileContext) -> str`
    *   `PUB:` FUN **format_symbol_list**`(ctx: FileContext) -> str`
    *   `PUB:` FUN **generate_dir_content**`(context: DirectoryContext) -> str`
    *   `PUB:` FUN **process_directory**`(path: Path, config: ProjectConfig, recursive: bool = True) -> None`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
    *   `PUB:` FUN **update_directory**`(path: Path, config: ProjectConfig) -> bool`
    *   `@DEP` atoms, dataclasses, models.config, models.context, pathlib, re, typing
*   **[deps_flow.py](deps_flow.py)**: Flow: Dependency Graph Generation.
    *   `PUB:` FUN **build_dependency_graph**`(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]`
    *   `PUB:` FUN **collect_imports**`(root: Path) -> Dict[str, List[str]]`
    *   `PUB:` FUN **generate_mermaid_graph**`(graph: Dict[str, Set[str]]) -> str`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
    *   `@DEP` atoms, collections, models.config, pathlib, typing
*   **[map_flow.py](map_flow.py)**: Flow: Map Generation.
    *   `PUB:` CLS **MapContext**
    *   `PUB:` FUN **build_tree_lines**`(current_path: Path, context: MapContext, level: int = 0) -> List[str]`
    *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str`
    *   `PUB:` FUN **format_file_entry**`(path: Path, level: int) -> str`
    *   `PUB:` FUN **generate_tree_content**`(config: ProjectConfig) -> str`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
    *   `@DEP` atoms, dataclasses, models.config, pathlib, typing
*   **[tech_flow.py](tech_flow.py)**: Flow: Tech Stack Snapshot Generation.
    *   `PUB:` FUN **generate_tech_content**`(config: ProjectConfig) -> str`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
    *   `@DEP` ndoc.atoms, ndoc.models.config, pathlib
*   **[todo_flow.py](todo_flow.py)**: Flow: Todo Aggregation.
    *   `PUB:` CLS **TodoItem**
    *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]`
    *   `PUB:` FUN **format_todo_lines**`(todos: List[TodoItem], root: Path) -> str`
    *   `GET->` VAR **priority_icon**`(self) -> str`
    *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
    *   `@DEP` atoms, dataclasses, models.config, pathlib, typing
<!-- NIKI_AUTO_Context_END -->
