# Context: ndoc
> @CONTEXT: Local | ndoc | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-30 19:25:16

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[atoms/](atoms/_AI.md#L1)**
*   **[flows/](flows/_AI.md#L1)**
*   **[models/](models/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: Niki-docAI Source Root.
*   **[daemon.py](daemon.py#L1)**: Daemon: Live Context Watcher. @DEP: ndoc.flows, ndoc.models.config, pathlib, threading, time, typing, watchdog.events, watchdog.observers
    *   `@API`
        *   `PUB:` CLS **DocChangeHandler**
            *   `PRV:` MET __init__`(self, config: ProjectConfig, debounce_interval: float = 2.0)`
            *   `PUB:` MET **on_any_event**`(self, event: FileSystemEvent)`
            *   `PUB:` MET **trigger_update**`(self)`
            *   `PUB:` MET **run_update**`(self)`
        *   `PUB:` FUN **start_watch_mode**`(config: ProjectConfig)`
*   **[entry.py](entry.py#L1)**: Entry Point: CLI Execution. @DEP: argparse, ndoc.atoms, ndoc.daemon, ndoc.flows, ndoc.models.config, pathlib, sys
    *   `@API`
        *   `PUB:` FUN **main**`()`
<!-- NIKI_AUTO_Context_END -->
