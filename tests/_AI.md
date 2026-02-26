# Context: tests
> @CONTEXT: Local | tests | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 18:10:31

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[fixtures/](fixtures/_AI.md#L1)**
*   **[temp/](temp/_AI.md#L1)**
*   **[benchmark_e2e.py](benchmark_e2e.py#L1)** @DEP: os, pathlib, shutil, subprocess, sys, ...
    *   `@API`
        *   `PUB:` FUN **run_command**`(cmd, cwd=None)`
        *   `PUB:` CLS **Result**
            *   `PRV:` MET __init__`(self, rc, out, err)`
        *   `PUB:` FUN **main**`()`
*   **[conftest.py](conftest.py#L1)** @DEP: pathlib, sys, tree_sitter
    *   `@API`
        *   `VAL->` VAR **root**` = Path(__file__).parent.parent`
        *   `VAL->` VAR **lib_path**` = root / ".ndoc" / "lib"`
*   **[test_ast.py](test_ast.py#L1)** @DEP: ndoc.core.io, ndoc.models.context, ndoc.parsing.ast, pathlib, pytest
    *   `@API`
        *   `VAL->` VAR **SAMPLE_CODE**` = """
class MyClass:
    '''Class Docstring'''
    
    def me...`
        *   `PUB:` FUN **test_extract_symbols_basic**`()`
        *   `PUB:` FUN **test_extract_complex_api**`()`
        *   `PUB:` FUN **find_sym**`(name)`
        *   `PUB:` FUN **find_member**`(cls_name, name)`
*   **[test_capabilities.py](test_capabilities.py#L1)** @DEP: ndoc.core.capabilities, os, sys, unittest, unittest.mock
    *   `@API`
        *   `PUB:` CLS **TestCapabilityManager**
            *   `PUB:` MET **test_get_language_installed**`(self)`
            *   `PUB:` MET **test_try_import_python**`(self)`
            *   `PUB:` MET **test_try_import_unknown**`(self)`
*   **[test_capability_flow.py](test_capability_flow.py#L1)** @DEP: ndoc.flows, ndoc.models.config, os, pathlib, sys, ...
    *   `@API`
        *   `PUB:` CLS **TestCapabilityFlow**
            *   `PUB:` MET **setUp**`(self)`
            *   `PUB:` MET **test_run_detects_languages**`(self, mock_ensure, mock_walk)`
            *   `PUB:` MET **test_check_single_file**`(self, mock_ensure)`
            *   `PUB:` MET **test_check_single_file_unknown**`(self, mock_ensure)`
*   **[test_csharp_api.py](test_csharp_api.py#L1)** @DEP: ndoc.core, ndoc.parsing, pathlib, sys
    *   `@API`
        *   `PUB:` FUN **test_csharp_extraction**`()`
*   **[test_lsp_server.py](test_lsp_server.py#L1)**: LSP Server Test Client (Refined) @DEP: json, os, subprocess, sys, threading, ...
    *   `@API`
        *   `PUB:` FUN **log**`(msg)`
        *   `PUB:` FUN **read_stream**`(stream, name)`
        *   `PUB:` FUN **test_lsp**`()`
*   **[test_scanner.py](test_scanner.py#L1)** @DEP: ndoc.parsing.scanner, pathlib, pytest
    *   `@API`
        *   `VAL->` VAR **SAMPLE_CONTENT**` = """
# @TAG arg1 arg2
<!-- NIKI_TEST_START -->
Some Content
<...`
        *   `PUB:` FUN **test_scan_file_content_mixed**`()`
        *   `PUB:` FUN **test_scan_file_content_text_only**`()`
<!-- NIKI_AUTO_Context_END -->
