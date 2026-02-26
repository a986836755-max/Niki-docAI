# Context: ndoc
> @CONTEXT: Local | ndoc | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 18:10:28

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[brain/](brain/_AI.md#L1)**
*   **[core/](core/_AI.md#L1)**
*   **[flows/](flows/_AI.md#L1)**
*   **[interfaces/](interfaces/_AI.md#L1)**
*   **[models/](models/_AI.md#L1)**
*   **[parsing/](parsing/_AI.md#L1)**
*   **[views/](views/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: .core.bootstrap
*   **[__main__.py](__main__.py#L1)** @DEP: ndoc.entry
*   **[api.py](api.py#L1)**: Public API: High-level interfaces for Agents and MCP Servers. @DEP: .flows, .models.config, pathlib, typing
    *   `@API`
        *   `PUB:` CLS **NdocAPI**
            *   `PRV:` MET __init__`(self, root_path: str = ".")`
            *   `PUB:` MET **refresh_context**`(self) -> bool`
            *   `PUB:` MET **get_semantic_context**`(self, query_or_file: str, focus: bool = True) -> str`
            *   `PUB:` MET **validate_architecture**`(self) -> bool`
            *   `PUB:` MET **analyze_impact**`(self) -> bool`
            *   `PUB:` MET **get_module_dependencies**`(self, target: Optional[str] = None) -> bool`
            *   `PUB:` MET **search_codebase**`(self, query: str, limit: int = 5) -> bool`
*   **[daemon.py](daemon.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.brain.hippocampus, ndoc.core.logger, ndoc.flows, ndoc.interfaces, ndoc.models.config, ...
    *   `@API`
        *   `PUB:` CLS **DocChangeHandler**
            *   `PRV:` MET __init__`(self, config: ProjectConfig, debounce_interval: float = 2.0)`
            *   `PUB:` MET **on_any_event**`(self, event: FileSystemEvent)`
            *   `PUB:` MET **trigger_update**`(self)`
            *   `PUB:` MET **run_update**`(self)`
        *   `PUB:` FUN **start_watch_mode**`(config: ProjectConfig)`
*   **[demo_violation.py](demo_violation.py#L1)**: @author Niki
    *   `@API`
        *   `PUB:` FUN **old_function**`()`
*   **[entry.py](entry.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: argparse, logging, ndoc, ndoc.core, ndoc.core.bootstrap, ...
    *   `@API`
        *   `PUB:` FUN **main**`()`
*   **[lsp_server.py](lsp_server.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: logging, lsprotocol.types, ndoc.brain, ndoc.brain.vectordb, ndoc.core, ...
    *   `@API`
        *   `VAL->` VAR **server**` = LanguageServer("ndoc-lsp", "0.1.0")`
        *   `VAL->` VAR _services` = {}`
        *   `PUB:` FUN **get_service**`(root_path: str) -> Optional[LSPService]`
        *   `PRV:` FUN _uri_to_path`(uri: str) -> Path`
        *   `PUB:` FUN **validate_document**`(ls: LanguageServer, uri: str)`
        *   `PUB:` FUN **hover**`(ls: LanguageServer, params: HoverParams)`
        *   `PUB:` FUN **code_lens**`(ls: LanguageServer, params: CodeLensParams)`
        *   `PUB:` FUN **execute_command**`(ls: LanguageServer, params: ExecuteCommandParams)`
        *   `PUB:` FUN **did_open**`(ls: LanguageServer, params: DidOpenTextDocumentParams)`
        *   `PUB:` FUN **did_save**`(ls: LanguageServer, params: DidSaveTextDocumentParams)`
        *   `PUB:` FUN **run**`()`
<!-- NIKI_AUTO_Context_END -->
