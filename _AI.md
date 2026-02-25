# Context: nk_doc_ai
> @CONTEXT: Local | nk_doc_ai | @TAGS: @LOCAL @LSP @IDE @PROTO
> 最后更新 (Last Updated): 2026-02-25 12:15:58

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
- LSP 适配：所有 IDE 插件相关的语义能力通过 `ndoc.lsp_server` 暴露。
- 架构感知：IDE 插件应优先使用 `_MAP.md` 和 `_AI.md` 进行语义增强，而非仅依赖语法树。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[editors/](editors/_AI.md#L1)**
*   **[samples/](samples/_AI.md#L1)**
*   **[scripts/](scripts/_AI.md#L1)**
*   **[src/](src/_AI.md#L1)**
*   **[test_vectordb_root/](test_vectordb_root/_AI.md#L1)**
*   **[tests/](tests/_AI.md#L1)**
*   **[tools/](tools/_AI.md#L1)**
*   **[README.md](README.md#L1)**: Niki-docAI
*   **[_ARCH.md](_ARCH.md#L1)**: Project Architecture
*   **[_DATA.md](_DATA.md#L1)**: Data Registry
*   **[_DEPS.md](_DEPS.md#L1)**: Dependency Graph
*   **[_MAP.md](_MAP.md#L1)**: Project Map
*   **[_RULES.md](_RULES.md#L1)**: Project Rules
*   **[_STATUS.md](_STATUS.md#L1)**: Project Status Board
*   **[_SYNTAX.md](_SYNTAX.md#L1)**: PROJECT SYNTAX
*   **[debug_scanner.py](debug_scanner.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.models.context, pathlib, sys, ndoc.atoms
    *   `@API`
        *   `PUB:` FUN **test**`()` [🔗6021]
*   **[debug_symbols.py](debug_symbols.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.atoms.io, pathlib, ndoc.atoms.ast, sys
    *   `@API`
        *   `VAL->` VAR **file_path**` = Path("src/ndoc/atoms/deps/stats.py")` [🔗236]
        *   `VAL->` VAR **content**` = read_text(file_path)` [🔗2268]
        *   `VAL->` VAR **tree**` = parse_code(content, file_path)` [🔗640]
        *   `VAL->` VAR **symbols**` = extract_symbols(tree, content.encode("utf-8"), file_path)` [🔗702]
*   **[lsp_test.log](lsp_test.log#L1)**
*   **[requirements.txt](requirements.txt#L1)**
*   **[setup.py](setup.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: setuptools
*   **[symbols_log.txt](symbols_log.txt#L1)**
*   **[test_enhanced_doc.py](test_enhanced_doc.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` FUN **test_func**`(a: int, b: str) -> bool` [🔗5]
        *   `PUB:` CLS **TestClass** [🔗4]
            *   `VAL->` VAR **field**`: int = 10` [🔗1312]
            *   `PUB:` MET **test_method**`(self)` [🔗2]
*   **[test_python_fix.py](test_python_fix.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: pathlib, sys, os, ndoc.atoms
    *   `@API`
        *   `PUB:` FUN **test_python_parsing**`()` [🔗3]
*   **[test_regex.py](test_regex.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re
    *   `@API`
        *   `VAL->` VAR **TAG_REGEX**` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s...` [🔗9]
        *   `VAL->` VAR **text**` = """
Inner docstring for test_func.
    @INTERNAL
"""` [🔗6961]
        *   `VAL->` VAR **matches**` = list(TAG_REGEX.finditer(text))` [🔗1063]
        *   `VAL->` VAR **text2**` = """
# @CORE
# This is a core function.
"""` [🔗23]
        *   `VAL->` VAR **matches2**` = list(TAG_REGEX.finditer(text2))` [🔗4]
<!-- NIKI_AUTO_Context_END -->
