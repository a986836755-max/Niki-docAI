# Context: tests
> @CONTEXT: Local | tests | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:56

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[fixtures/](fixtures/_AI.md#L1)**
*   **[temp/](temp/_AI.md#L1)**
*   **[conftest.py](conftest.py#L1)** @DEP: pathlib, sys
    *   `@API`
        *   `VAL->` VAR **root**` = Path(__file__).parent.parent` [🔗1951]
*   **[test_ast.py](test_ast.py#L1)** @DEP: ndoc.models.context, ndoc.atoms.ast, pathlib, pytest, ndoc.atoms.io
    *   `@API`
        *   `VAL->` VAR **SAMPLE_CODE**` = """
class MyClass:
    '''Class Docstring'''
    
    def me...` [🔗4]
        *   `PUB:` FUN **test_extract_symbols_basic**`()` [🔗2]
        *   `PUB:` FUN **test_extract_complex_api**`()` [🔗2]
        *   `PUB:` FUN **find_sym**`(name)` [🔗6]
        *   `PUB:` FUN **find_member**`(cls_name, name)` [🔗5]
*   **[test_capabilities.py](test_capabilities.py#L1)** @DEP: sys, unittest, os, ndoc.atoms.capabilities, unittest.mock
    *   `@API`
        *   `PUB:` CLS **TestCapabilityManager** [🔗2]
            *   `PUB:` MET **test_get_language_installed**`(self)` [🔗2]
            *   `PUB:` MET **test_try_import_python**`(self)` [🔗2]
            *   `PUB:` MET **test_try_import_unknown**`(self)` [🔗2]
*   **[test_capability_flow.py](test_capability_flow.py#L1)** @DEP: ndoc.flows, ndoc.models.config, sys, unittest, os, pathlib, unittest.mock
    *   `@API`
        *   `PUB:` CLS **TestCapabilityFlow** [🔗2]
            *   `PUB:` MET **setUp**`(self)` [🔗2]
            *   `PUB:` MET **test_run_detects_languages**`(self, mock_ensure, mock_walk)` [🔗2]
            *   `PUB:` MET **test_check_single_file**`(self, mock_ensure)` [🔗2]
            *   `PUB:` MET **test_check_single_file_unknown**`(self, mock_ensure)` [🔗2]
*   **[test_csharp_api.py](test_csharp_api.py#L1)** @DEP: pathlib, sys, ndoc.atoms
    *   `@API`
        *   `PUB:` FUN **test_csharp_extraction**`()` [🔗3]
*   **[test_lsp_server.py](test_lsp_server.py#L1)**: """ @DEP: threading, time, sys, os, json, subprocess
    *   `@API`
        *   `PUB:` FUN **log**`(msg)` [🔗2873]
        *   `PUB:` FUN **read_stream**`(stream, name)` [🔗4]
        *   `PUB:` FUN **test_lsp**`()` [🔗3]
*   **[test_scanner.py](test_scanner.py#L1)** @DEP: pytest, pathlib, ndoc.atoms.scanner
    *   `@API`
        *   `VAL->` VAR **SAMPLE_CONTENT**` = """
# @TAG arg1 arg2
<!-- NIKI_TEST_START -->
Some Content
<...` [🔗3]
        *   `PUB:` FUN **test_scan_file_content_mixed**`()` [🔗2]
        *   `PUB:` FUN **test_scan_file_content_text_only**`()` [🔗2]
<!-- NIKI_AUTO_Context_END -->
