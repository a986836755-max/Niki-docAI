# Context: models
> @CONTEXT: Local | models | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:27:57

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Core Context Models**: `context.py` defines `FileContext`, `DirectoryContext`, and `Symbol`. These are the primary data structures for documentation generation.
*   **Symbol Structure**: `Symbol` captures language-agnostic metadata (kind, visibility, line number) and now includes `test_usages` to link definitions to test cases.
*   **Symbol Refactoring**: `Symbol` class has been moved to `ndoc.models.symbol` to reduce coupling and improve maintainability.
*   **Quality Commands Config**: `ProjectConfig` stores `lint_commands` and `typecheck_commands` loaded from `_RULES.md` for quality gate execution.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Models: Data Definitions.
*   **[config.py](config.py#L1)**: Models: Configuration definitions. @DEP: dataclasses, pathlib, typing @DEP: pathlib, dataclasses, typing
*   **[context.py](context.py#L1)**: Models: Context Models. @DEP: .symbol, dataclasses, pathlib, typing @DEP: .symbol, pathlib, dataclasses, typing
*   **[symbol.py](symbol.py#L1)**: Models: Code Symbol. @DEP: dataclasses, typing @DEP: dataclasses, typing
<!-- NIKI_AUTO_Context_END -->
