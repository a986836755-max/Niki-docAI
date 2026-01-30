# Context: tests
> @CONTEXT: Local | tests | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-30 19:25:17

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[fixtures/](fixtures/_AI.md#L1)**
*   **[temp/](temp/_AI.md#L1)**
*   **[conftest.py](conftest.py#L1)** @DEP: pathlib, sys
*   **[test_ast.py](test_ast.py#L1)** @DEP: ndoc.atoms.ast, ndoc.atoms.io, ndoc.models.context, pathlib, pytest
    *   `@API`
        *   `PUB:` FUN **test_extract_symbols_basic**`()`
        *   `PUB:` FUN **test_extract_complex_api**`()`
        *   `PUB:` FUN **find_sym**`(name)`
        *   `PUB:` FUN **find_member**`(cls_name, name)`
*   **[test_scanner.py](test_scanner.py#L1)** @DEP: ndoc.atoms.scanner, pathlib, pytest
    *   `@API`
        *   `PUB:` FUN **test_scan_file_content_mixed**`()`
        *   `PUB:` FUN **test_scan_file_content_text_only**`()`
<!-- NIKI_AUTO_Context_END -->
