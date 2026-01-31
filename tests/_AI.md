# Context: tests
> @CONTEXT: Local | tests | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 16:50:58

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[fixtures/](fixtures/_AI.md#L1)**
*   **[temp/](temp/_AI.md#L1)**
*   **[conftest.py](conftest.py#L1)** @DEP: sys, pathlib.Path, pathlib
    *   `@API`
        *   `VAL->` VAR **root**` = Path(__file__).parent.parent`
*   **[test_ast.py](test_ast.py#L1)** @DEP: ndoc.atoms.ast.extract_symbols, ndoc.atoms.io.read_text, pathlib.Path, ndoc.atoms.ast.parse_code, ndoc.models.context, ndoc.atoms.ast, ndoc.models.context.Symbol, ndoc.atoms.io, pytest, pathlib
    *   `@API`
        *   `VAL->` VAR **SAMPLE_CODE**` = """
class MyClass:
    '''Class Docstring'''
    
    def method_one(self, a, b):
        '''Method One Doc'''
        return a + b
        
    @property
    def prop_one(self):
        '''Property One Doc'''
        return 1
        
    @classmethod
    def class_method(cls):
        '''Class Method Doc'''
        pass
        
    @staticmethod
    def static_method():
        pass

def global_func(x: int) -> int:
    '''Global Func Doc'''
    return x * 2
"""`
        *   `PUB:` FUN **test_extract_symbols_basic**`()`
        *   `PUB:` FUN **test_extract_complex_api**`()`
        *   `PUB:` FUN **find_sym**`(name)`
        *   `PUB:` FUN **find_member**`(cls_name, name)`
*   **[test_csharp_api.py](test_csharp_api.py#L1)** @DEP: pathlib.Path, ndoc.atoms.ast, sys, ndoc.atoms, ndoc.atoms.io, pathlib
    *   `@API`
        *   `PUB:` FUN **test_csharp_extraction**`()`
*   **[test_lsp_server.py](test_lsp_server.py#L1)**: Simple test client to verify LSP Server initialization. @DEP: json, time, sys, subprocess
    *   `@API`
        *   `PUB:` FUN **test_lsp_init**`()`
*   **[test_scanner.py](test_scanner.py#L1)** @DEP: pathlib.Path, ndoc.atoms.scanner, ndoc.atoms.scanner.scan_file_content, pytest, pathlib
    *   `@API`
        *   `VAL->` VAR **SAMPLE_CONTENT**` = """
# @TAG arg1 arg2
<!-- NIKI_TEST_START -->
Some Content
<!-- NIKI_TEST_END -->

class TestClass:
    '''Doc'''
    pass
"""`
        *   `PUB:` FUN **test_scan_file_content_mixed**`()`
        *   `PUB:` FUN **test_scan_file_content_text_only**`()`
<!-- NIKI_AUTO_Context_END -->
