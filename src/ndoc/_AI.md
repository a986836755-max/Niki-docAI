# Context: ndoc
> @CONTEXT: Local | ndoc | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 14:59:54

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Proactive Capability Check**: `entry.py` serves as the primary gatekeeper. It must invoke `capability_flow` to ensure all necessary language parsers are installed *before* executing documentation generation flows (`map`, `context`, `all`).
*   **Dynamic Watchdog**: `daemon.py` monitors file system events. When a new file type is detected (e.g., a `.rs` file added to a python project), it must trigger a capability check to auto-provision the parser on the fly, ensuring zero-configuration support for polyglot projects.
*   **CLI Robustness**: All CLI commands (including `lsp`) must handle missing capabilities gracefully, either by attempting auto-installation or falling back to regex-based scanning without crashing.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[atoms/](atoms/_AI.md#L1)**
*   **[flows/](flows/_AI.md#L1)**
*   **[models/](models/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: """
*   **[daemon.py](daemon.py#L1)**: """ @DEP: threading, pathlib, watchdog.observers, time, ndoc.models.config, traceback, ndoc.flows, typing ...
    *   `@API`
        *   `PUB:` CLS **DocChangeHandler**
            *   `PRV:` MET __init__`(self, config: ProjectConfig, debounce_interval: float = 2.0)`
            *   `PUB:` MET **on_any_event**`(self, event: FileSystemEvent)`
            *   `PUB:` MET **trigger_update**`(self)`
            *   `PUB:` MET **run_update**`(self)`
        *   `PUB:` FUN **start_watch_mode**`(config: ProjectConfig)`
*   **[entry.py](entry.py#L1)**: """ @DEP: sys, ndoc.daemon, pathlib, ndoc.models.config, argparse, ndoc.flows, ndoc.atoms
    *   `@API`
        *   `PUB:` FUN **main**`()`
*   **[lsp_server.py](lsp_server.py#L1)**: """ @DEP: sys, lsprotocol.types, pathlib, os, ndoc.models, ndoc.atoms, typing, pygls.lsp.server
    *   `@API`
        *   `VAL->` VAR **BASE_DIR**` = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."...`
        *   `PUB:` CLS **NDocLanguageServer**
            *   `PRV:` MET __init__`(self, *args, **kwargs)`
        *   `VAL->` VAR **server**` = NDocLanguageServer("ndoc-ai-server", "v0.1.0")`
        *   `PUB:` FUN **lsp_initialize**`(ls: NDocLanguageServer, params)`
        *   `PUB:` FUN **check_architecture**`(ls: NDocLanguageServer, doc_uri: str)`
        *   `PUB:` FUN **did_open**`(ls: NDocLanguageServer, params)`
        *   `PUB:` FUN **did_save**`(ls: NDocLanguageServer, params: DidSaveTextDocumentParams)`
        *   `PUB:` FUN **hover**`(ls: NDocLanguageServer, params: HoverParams)`
        *   `PUB:` FUN **main**`()`
<!-- NIKI_AUTO_Context_END -->
