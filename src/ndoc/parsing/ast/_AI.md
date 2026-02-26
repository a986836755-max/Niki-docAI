# Context: ast
> @CONTEXT: Local | ast | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:27:58

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Centralized Language Access**: All AST operations must obtain language instances via `base.get_language()` or `base.get_parser()`, which internally delegates to `CapabilityManager`. Do not bypass this layer.
<!-- Add local rules here -->
*   **Decoupled AST Logic**: Language-specific queries are isolated in `langs/`. `discovery.py` uses these queries for generic operations (find calls/imports).
*   **Location-Aware Discovery**: `find_calls_with_loc` provides line-level precision for symbol usages, enabling precise linking in `_AI.md`.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: .base, .discovery, .symbols, .utils @DEP: .utils, .discovery, .symbols, .base
*   **[base.py](base.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: .., ...core.capabilities, dataclasses, pathlib, tree_sitter, ... @DEP: ...core.capabilities, tree_sitter, typing, .., dataclasses, pathlib
*   **[discovery.py](discovery.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: .., .base, tree_sitter, typing @DEP: .., tree_sitter, typing, .base
*   **[skeleton.py](skeleton.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: .., .base, ndoc.core.capabilities, pathlib, tree_sitter, ... @DEP: tree_sitter, typing, .., .base, ndoc.core.capabilities, pathlib
*   **[symbols.py](symbols.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: .., ...core.text_utils, ...models.symbol, .base, .utils, ... @DEP: ...models.symbol, .utils, tree_sitter, typing, ...core.text_utils, .., .base, pathlib
*   **[utils.py](utils.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: .., .base, tree_sitter, typing @DEP: .., tree_sitter, typing, .base
<!-- NIKI_AUTO_Context_END -->
