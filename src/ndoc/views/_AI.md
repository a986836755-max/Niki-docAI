# Context: views
> @CONTEXT: Local | views | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 18:10:28

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Views: Output Rendering.
*   **[context.py](context.py#L1)**: View: Context Rendering. @DEP: ..core, ..interfaces, ..models.context, pathlib, typing
    *   `@API`
        *   `PUB:` FUN **format_file_summary**`(ctx: FileContext, root: Optional[Path] = None) -> str`
        *   `PUB:` FUN **format_symbol_list**`(ctx: FileContext, root_path: Path = None) -> str`
        *   `PRV:` FUN _format_single_symbol`(sym, level: int)`
        *   `PUB:` FUN **format_dependencies**`(ctx: FileContext) -> str`
        *   `PUB:` FUN **generate_dir_content**`(context: DirectoryContext, root_path: Path = None) -> str`
*   **[mermaid.py](mermaid.py#L1)**: View: Mermaid Graph Renderer. @DEP: typing
    *   `@API`
        *   `PUB:` FUN **sanitize_node**`(name: str) -> str`
        *   `PUB:` FUN **simplify_module_name**`(name: str) -> str`
        *   `PUB:` FUN **generate_mermaid_graph**`(graph: Dict[str, Set[str]], metrics: Dict[str, Dict[str, float]], core_only: bool = False, is_core_func=None) -> str`
*   **[reports.py](reports.py#L1)**: View: Report Tables. @DEP: .mermaid, typing
    *   `@API`
        *   `PUB:` FUN **generate_instability_table**`(metrics: Dict[str, Dict[str, float]], is_core_func=None) -> str`
        *   `PUB:` FUN **generate_dependency_matrix**`(graph: Dict[str, Set[str]], modules: List[str], is_core_func=None) -> str`
<!-- NIKI_AUTO_Context_END -->
