# Context: nk_doc_ai
> @CONTEXT: Local | nk_doc_ai | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 16:50:18

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[samples/](samples/_AI.md#L1)**
*   **[src/](src/_AI.md#L1)**
*   **[tests/](tests/_AI.md#L1)**
*   **[tools/](tools/_AI.md#L1)**
*   **[vendors/](vendors/_AI.md#L1)**
*   **[README.md](README.md#L1)**
*   **[_ARCH.md](_ARCH.md#L1)**
*   **[_DATA.md](_DATA.md#L1)**
*   **[_DEPS.md](_DEPS.md#L1)**
*   **[_MAP.md](_MAP.md#L1)**
*   **[_MEMORY.md](_MEMORY.md#L1)**
*   **[_NEXT.md](_NEXT.md#L1)**
*   **[_RULES.md](_RULES.md#L1)**
*   **[_STATS.md](_STATS.md#L1)**
*   **[_SYMBOLS.md](_SYMBOLS.md#L1)**
*   **[_SYNTAX.md](_SYNTAX.md#L1)**
*   **[_TECH.md](_TECH.md#L1)**
*   **[debug_scanner.py](debug_scanner.py#L1)** @DEP: pathlib.Path, ndoc.atoms.scanner, ndoc.models.context, ndoc.models.context.Symbol, sys, ndoc.atoms, pathlib
    *   `@API`
        *   `PUB:` FUN **test**`()`
*   **[debug_symbols.py](debug_symbols.py#L1)** @DEP: ndoc.atoms.ast.extract_symbols, ndoc.atoms.ast.MAX_VALUE_LENGTH, ndoc.atoms.io.read_text, pathlib.Path, ndoc.atoms.ast.parse_code, ndoc.atoms.ast, sys, ndoc.atoms.io, pathlib
    *   `@API`
        *   `VAL->` VAR **file_path**` = Path("src/ndoc/atoms/deps/stats.py")`
        *   `VAL->` VAR **content**` = read_text(file_path)`
        *   `VAL->` VAR **tree**` = parse_code(content, file_path)`
        *   `VAL->` VAR **symbols**` = extract_symbols(tree, content.encode("utf-8"), file_path)`
*   **[requirements.txt](requirements.txt#L1)**
*   **[setup.py](setup.py#L1)** @DEP: setuptools.find_packages, setuptools, setuptools.setup
*   **[symbols_log.txt](symbols_log.txt#L1)**
*   **[test_enhanced_doc.py](test_enhanced_doc.py#L1)**: @MODULE TestModule
    *   `@API`
        *   `PUB:` FUN **test_func**`(a: int, b: str) -> bool`
        *   `PUB:` CLS **TestClass**
            *   `VAL->` VAR **field**`: int = 10`
            *   `PUB:` MET **test_method**`(self)`
*   **[test_python_fix.py](test_python_fix.py#L1)** @DEP: ndoc.atoms.queries, os, pathlib.Path, ndoc.atoms.ast, sys, ndoc.atoms, pathlib
    *   `@API`
        *   `PUB:` FUN **test_python_parsing**`()`
*   **[test_regex.py](test_regex.py#L1)** @DEP: re
    *   `@API`
        *   `VAL->` VAR **TAG_REGEX**` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s+(.*?))?(?:\s*(?:-->))?\s*$",
    re.MULTILINE,
)`
        *   `VAL->` VAR **text**` = """
Inner docstring for test_func.
    @INTERNAL
"""`
        *   `VAL->` VAR **matches**` = list(TAG_REGEX.finditer(text))`
        *   `VAL->` VAR **text2**` = """
# @CORE
# This is a core function.
"""`
        *   `VAL->` VAR **matches2**` = list(TAG_REGEX.finditer(text2))`
<!-- NIKI_AUTO_Context_END -->
