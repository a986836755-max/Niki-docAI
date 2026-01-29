# Context: tests
> @CONTEXT: Local | tests | @TAGS: @LOCAL

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[conftest.py](conftest.py)**
    *   `@DEP` pathlib, sys
*   **[test_ast.py](test_ast.py)**
    *   `PUB:` FUN **test_extract_symbols_basic**`()`
    *   `@DEP` ndoc.atoms.ast, ndoc.models.context, pytest
*   **[test_scanner.py](test_scanner.py)**
    *   `PUB:` FUN **test_scan_file_content_mixed**`()`
    *   `PUB:` FUN **test_scan_file_content_text_only**`()`
    *   `@DEP` ndoc.atoms.scanner, pathlib, pytest
<!-- NIKI_AUTO_Context_END -->
