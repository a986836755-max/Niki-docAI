# Context: ndoc
> @CONTEXT: Local | ndoc | @TAGS: @LOCAL

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[atoms/](atoms/_AI.md)**
*   **[flows/](flows/_AI.md)**
*   **[models/](models/_AI.md)**
*   **[__init__.py](__init__.py)**: Niki-docAI Source Root.
*   **[daemon.py](daemon.py)**: Daemon: Live Context Watcher.
    *   `PUB:` CLS **DocChangeHandler**
    *   `PUB:` FUN **on_any_event**`(self, event: FileSystemEvent)`
    *   `PUB:` FUN **run_update**`(self)`
    *   `PUB:` FUN **start_watch_mode**`(config: ProjectConfig)`
    *   `PUB:` FUN **trigger_update**`(self)`
    *   `PRV:` FUN __init__`(self, config: ProjectConfig, debounce_interval: float = 2.0)`
    *   `@DEP` ndoc.flows, ndoc.models.config, pathlib, threading, time, typing, watchdog.events, watchdog.observers
*   **[entry.py](entry.py)**: Entry Point: CLI Execution.
    *   `PUB:` FUN **main**`()`
    *   `@DEP` argparse, ndoc.daemon, ndoc.flows, ndoc.models.config, pathlib, sys
<!-- NIKI_AUTO_Context_END -->
