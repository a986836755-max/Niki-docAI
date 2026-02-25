# Context: ndoc
> @CONTEXT: Local | ndoc | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:54

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Proactive Capability Check**: `entry.py` serves as the primary gatekeeper. It must invoke `capability_flow` to ...ensure all necessary language parsers are installed *before* executing documentation generation flows (`map`, `context`, `all`).
*   **Dynamic Watchdog**: `daemon.py` monitors file system events. When a new file type is detected (e.g., a `.rs` file added to a python project), it must trigger a capability check to auto-provision the parser on the fly, ensuring zero-configuration support for polyglot projects.
*   **CLI Robustness**: All CLI commands (including `lsp`) must handle missing capabilities gracefully, either by attempting auto-installation or falling back to regex-based scanning without crashing.
*   **LSP Protocol Integrity**: `entry.py`'s `server` command MUST NOT print anything to `stdout` other than JSON-RPC messages. All logs must go to `stderr`.
*   **Context Awareness**: `lsp_server.py` implements "Thinking Context" via `textDocument/hover`, aggregating rules and memories from `_AI.md` hierarchy.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[atoms/](atoms/_AI.md#L1)**
*   **[brain/](brain/_AI.md#L1)**
*   **[core/](core/_AI.md#L1)**
*   **[flows/](flows/_AI.md#L1)**
*   **[interfaces/](interfaces/_AI.md#L1)**
*   **[models/](models/_AI.md#L1)**
*   **[parsing/](parsing/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START>
*   **[daemon.py](daemon.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.flows, watchdog.observers, threading, time, typing, ndoc.models.config, ndoc.brain.hippocampus, pathlib ...
    *   `@API`
        *   `PUB:` CLS **DocChangeHandler** [🔗3]
            *   `PRV:` MET __init__`(self, config: ProjectConfig, debounce_interval: float = 2.0)` [🔗44]
            *   `PUB:` MET **on_any_event**`(self, event: FileSystemEvent)` [🔗2]
            *   `PUB:` MET **trigger_update**`(self)` [🔗3]
            *   `PUB:` MET **run_update**`(self)` [🔗3]
        *   `PUB:` FUN **start_watch_mode**`(config: ProjectConfig)` [🔗4]
*   **[demo_violation.py](demo_violation.py#L1)**: @author Niki
    *   `@API`
        *   `PUB:` FUN **old_function**`()` [🔗2]
*   **[entry.py](entry.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.flows, ndoc, ndoc.models.config, sys, pathlib, ndoc.daemon, argparse, ndoc.atoms ...
    *   `@API`
        *   `PUB:` FUN **main**`()` [🔗908]
*   **[lsp_server.py](lsp_server.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.parsing, ndoc.models.context, typing, lsprotocol.types, logging, sys, os, ndoc.brain.vectordb ...
    *   `@API`
        *   `VAL->` VAR **server**` = LanguageServer("ndoc-lsp", "0.1.0")` [🔗2409]
        *   `VAL->` VAR _services` = {}` [🔗5]
        *   `PUB:` FUN **get_service**`(root_path: str) -> Optional[LSPService]` [🔗11]
        *   `PUB:` FUN **validate_document**`(ls: LanguageServer, uri: str)` [🔗4]
        *   `PUB:` FUN **hover**`(ls: LanguageServer, params: HoverParams)` [🔗147]
        *   `PUB:` FUN **did_open**`(ls: LanguageServer, params: DidOpenTextDocumentParams)` [🔗2]
        *   `PUB:` FUN **did_save**`(ls: LanguageServer, params: DidSaveTextDocumentParams)` [🔗2]
        *   `PUB:` FUN **run**`()` [🔗2341]
<!-- NIKI_AUTO_Context_END -->
