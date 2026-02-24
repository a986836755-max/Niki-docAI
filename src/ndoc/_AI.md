# Context: ndoc
> @CONTEXT: Local | ndoc | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 15:39:20

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Proactive Capability Check**: `entry.py` serves as the primary gatekeeper. It must invoke `capability_flow` to ensure all necessary language parsers are installed *before* executing documentation generation flows (`map`, `context`, `all`).
*   **Dynamic Watchdog**: `daemon.py` monitors file system events. When a new file type is detected (e.g., a `.rs` file added to a python project), it must trigger a capability check to auto-provision the parser on the fly, ensuring zero-configuration support for polyglot projects.
*   **CLI Robustness**: All CLI commands (including `lsp`) must handle missing capabilities gracefully, either by attempting auto-installation or falling back to regex-based scanning without crashing.
*   **LSP Protocol Integrity**: `entry.py`'s `server` command MUST NOT print anything to `stdout` other than JSON-RPC messages. All logs must go to `stderr`.
*   **Context Awareness**: `lsp_server.py` implements "Thinking Context" via `textDocument/hover`, aggregating rules and memories from `_AI.md` hierarchy.

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
*   **[entry.py](entry.py#L1)**: """ @DEP: sys, ndoc.daemon, pathlib, ndoc.models.config, argparse, ndoc.flows, ndoc.atoms, ndoc
    *   `@API`
        *   `PUB:` FUN **main**`()`
*   **[lsp_server.py](lsp_server.py#L1)**: """ @DEP: sys, lsprotocol.types, pathlib, logging, os, typing, pygls.lsp.server, ndoc.atoms.lsp
    *   `@API`
        *   `VAL->` VAR **server**` = LanguageServer("ndoc-lsp", "0.1.0")`
        *   `VAL->` VAR _services` = {}`
        *   `PUB:` FUN **get_service**`(root_path: str) -> Optional[LSPService]`
        *   `PUB:` FUN **did_open**`(ls: LanguageServer, params: DidOpenTextDocumentParams)`
        *   `PUB:` FUN **hover**`(ls: LanguageServer, params: HoverParams) -> Optional[Hover]`
        *   `PUB:` FUN **execute_command**`(ls: LanguageServer, params: ExecuteCommandParams)`
        *   `PUB:` FUN **run**`()`
<!-- NIKI_AUTO_Context_END -->
