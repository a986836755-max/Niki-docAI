# Context: brain
> @CONTEXT: Local | brain | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:27:55

## !RULE
<!-- Add local rules here -->
*   **Violation Location**: `checker.Violation` 必须携带 `line` 与 `character`，以便 LSP 精确标注诊断位置。

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Brain: Intelligence Layer. @DEP: .cache, .checker, .hippocampus, .index, .llm @DEP: .index, .llm, .checker, .hippocampus, .cache
*   **[cache.py](cache.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: hashlib, json, pathlib, sqlite3, typing @DEP: sqlite3, typing, hashlib, json, pathlib
*   **[checker.py](checker.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..models.context, ..models.symbol, .index, dataclasses, pathlib, ... @DEP: .index, ..models.context, typing, ..models.symbol, dataclasses, pathlib
*   **[hippocampus.py](hippocampus.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: collections, dataclasses, enum, pathlib, time, ... @DEP: typing, time, enum, dataclasses, collections, pathlib
*   **[index.py](index.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..models.context, ..models.symbol, dataclasses, json, os, ... @DEP: ..models.context, typing, ..models.symbol, dataclasses, json, pathlib, os
*   **[llm.py](llm.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: json, os, typing, urllib @DEP: typing, json, urllib, os
*   **[vectordb.py](vectordb.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core.capabilities, chromadb, chromadb.config, os, pathlib, ... @DEP: ..core.capabilities, chromadb.config, typing, chromadb, pathlib, os
<!-- NIKI_AUTO_Context_END -->
