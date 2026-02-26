# Context: deps
> @CONTEXT: Local | deps | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:27:58

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)** @DEP: . @DEP: .
*   **[core.py](core.py#L1)**: Core parsing logic for dependency manifests. @DEP: ...core, json, pathlib, re, typing @DEP: re, ...core, typing, json, pathlib
*   **[stats.py](stats.py#L1)**: Language Statistics. @DEP: ...core, ..langs, pathlib, typing @DEP: ..langs, ...core, pathlib, typing
<!-- NIKI_AUTO_Context_END -->
