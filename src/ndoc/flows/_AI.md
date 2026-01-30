# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-30 18:57:09

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Flows: Business Logic Pipelines.
*   **[clean_flow.py](clean_flow.py#L1)**: Flow: Clean / Reset. @DEP: ndoc.models.config, os, pathlib, typing
*   **[config_flow.py](config_flow.py#L1)**: Flow: Configuration Loading. @DEP: ndoc.atoms, ndoc.models.config, pathlib, re, typing
*   **[context_flow.py](context_flow.py#L1)**: Flow: Recursive Context Generation. @DEP: atoms, dataclasses, datetime, models.config, models.context, pathlib, re, typing
*   **[deps_flow.py](deps_flow.py#L1)**: Flow: Dependency Graph Generation. @DEP: atoms, collections, datetime, models.config, pathlib, typing
*   **[doctor_flow.py](doctor_flow.py#L1)**: Flow: System Diagnostics. @DEP: importlib, ndoc.models.config, pathlib, platform, shutil, sys, tree_sitter, tree_sitter_python, typing
*   **[init_flow.py](init_flow.py#L1)**: Flow: Initialization. @DEP: ndoc.flows, ndoc.models.config
*   **[map_flow.py](map_flow.py#L1)**: Flow: Map Generation. @DEP: atoms, dataclasses, datetime, models.config, pathlib, typing
*   **[stats_flow.py](stats_flow.py#L1)**: Flow: Statistics. @DEP: datetime, ndoc.atoms, ndoc.models.config, os, pathlib, re, time
*   **[syntax_flow.py](syntax_flow.py#L1)**: Flow: Syntax Manual Sync. @DEP: ndoc.atoms, ndoc.models.config, pathlib
*   **[tech_flow.py](tech_flow.py#L1)**: Flow: Tech Stack Snapshot Generation. @DEP: datetime, ndoc.atoms, ndoc.models.config, pathlib
*   **[todo_flow.py](todo_flow.py#L1)**: Flow: Todo Aggregation. @DEP: atoms, dataclasses, datetime, models.config, pathlib, typing
*   **[update_flow.py](update_flow.py#L1)**: Flow: Self-Update Flow. @DEP: pathlib, subprocess, sys, typing
*   **[verify_flow.py](verify_flow.py#L1)**: Flow: Verification. @DEP: ndoc.models.config, sys
<!-- NIKI_AUTO_Context_END -->
