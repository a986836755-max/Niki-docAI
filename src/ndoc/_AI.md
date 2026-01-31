# Context: ndoc
> @CONTEXT: Local | ndoc | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 16:51:14

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[atoms/](atoms/_AI.md#L1)**
*   **[flows/](flows/_AI.md#L1)**
*   **[models/](models/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: Niki-docAI Source Root.
*   **[daemon.py](daemon.py#L1)**: Daemon: Live Context Watcher. @DEP: watchdog.observers.Observer, ndoc.flows.symbols_flow, ndoc.flows.tech_flow, watchdog.events.FileSystemEvent, ndoc.flows.deps_flow, pathlib.Path, ndoc.flows, pathlib, typing.List, ndoc.flows.context_flow, typing.Callable, time, ndoc.flows.data_flow, ndoc.flows.map_flow, watchdog.events.FileSystemEventHandler, typing.Set, typing, ndoc.flows.archive_flow, ndoc.models.config, traceback, threading, ndoc.flows.todo_flow, watchdog.events, ndoc.models.config.ProjectConfig, watchdog.observers
    *   `@API`
        *   `PUB:` CLS **DocChangeHandler**
            *   `PRV:` MET __init__`(self, config: ProjectConfig, debounce_interval: float = 2.0)`
            *   `PUB:` MET **on_any_event**`(self, event: FileSystemEvent)`
            *   `PUB:` MET **trigger_update**`(self)`
            *   `PUB:` MET **run_update**`(self)`
        *   `PUB:` FUN **start_watch_mode**`(config: ProjectConfig)`
*   **[entry.py](entry.py#L1)**: Entry Point: CLI Execution. @DEP: ndoc.flows.config_flow, ndoc.flows.tech_flow, ndoc.flows.syntax_flow, ndoc.flows.verify_flow, ndoc.flows.deps_flow, ndoc.flows.doctor_flow, ndoc.flows.clean_flow, ndoc.models.config.ScanConfig, pathlib.Path, ndoc.flows, ndoc.atoms.lsp, sys, ndoc.flows.init_flow, ndoc.flows.plan_flow, ndoc.atoms, pathlib, ndoc.flows.stats_flow, ndoc.flows.context_flow, argparse, ndoc.flows.update_flow, ndoc.flows.data_flow, ndoc.flows.map_flow, ndoc.daemon, ndoc.flows.archive_flow, ndoc.models.config, ndoc.flows.todo_flow, ndoc.atoms.fs, ndoc.atoms.io, ndoc.daemon.start_watch_mode, ndoc.models.config.ProjectConfig, ndoc.flows.symbols_flow
    *   `@API`
        *   `PUB:` FUN **main**`()`
*   **[lsp_server.py](lsp_server.py#L1)**: LSP Server implementation using pygls. @DEP: lsprotocol.types.INITIALIZE, pygls.server.LanguageServer, pathlib.Path, ndoc.atoms.lsp, sys, lsprotocol.types, ndoc.atoms, lsprotocol.types.TEXT_DOCUMENT_DID_OPEN, pathlib, typing.List, pygls.server, lsprotocol.types.TextDocumentItem, lsprotocol.types.HoverParams, ndoc.atoms.scanner, lsprotocol.types.MarkupContent, typing, ndoc.models, ndoc.models.config, os, lsprotocol.types.TEXT_DOCUMENT_HOVER, ndoc.atoms.fs, typing.Optional, lsprotocol.types.MarkupKind, lsprotocol.types.Hover
    *   `@API`
        *   `PUB:` CLS **NDocLanguageServer**
            *   `PRV:` MET __init__`(self, *args, **kwargs)`
        *   `VAL->` VAR **server**` = NDocLanguageServer("ndoc-ai-server", "v0.1.0")`
        *   `PUB:` FUN **lsp_initialize**`(ls: NDocLanguageServer, params)`
        *   `PUB:` FUN **did_open**`(ls: NDocLanguageServer, params)`
        *   `PUB:` FUN **hover**`(ls: NDocLanguageServer, params: HoverParams)`
        *   `PUB:` FUN **main**`()`
<!-- NIKI_AUTO_Context_END -->
