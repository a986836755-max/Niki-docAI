# Context: nk_doc_ai
> @CONTEXT: Local | nk_doc_ai | @TAGS: @LOCAL @LSP @IDE @PROTO
> 最后更新 (Last Updated): 2026-02-24 14:59:54

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
- LSP 适配：所有 IDE 插件相关的语义能力通过 `ndoc.lsp_server` 暴露。
- 架构感知：IDE 插件应优先使用 `_MAP.md` 和 `_AI.md` 进行语义增强，而非仅依赖语法树。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[editors/](editors/_AI.md#L1)**
*   **[samples/](samples/_AI.md#L1)**
*   **[src/](src/_AI.md#L1)**
*   **[tests/](tests/_AI.md#L1)**
*   **[tools/](tools/_AI.md#L1)**
*   **[README.md](README.md#L1)**: Niki-docAI
*   **[_ARCH.md](_ARCH.md#L1)**: PROJECT ARCHITECTURE
*   **[_DATA.md](_DATA.md#L1)**: Data Registry
*   **[_DEPS.md](_DEPS.md#L1)**: Dependency Graph
*   **[_MAP.md](_MAP.md#L1)**: Project Map
*   **[_MEMORY.md](_MEMORY.md#L1)**: PROJECT MEMORY
*   **[_NEXT.md](_NEXT.md#L1)**: Todo List
*   **[_RULES.md](_RULES.md#L1)**: Project Rules
*   **[_STATS.md](_STATS.md#L1)**: 项目统计报告 (Project Statistics)
*   **[_SYMBOLS.md](_SYMBOLS.md#L1)**: Symbol Index
*   **[_SYNTAX.md](_SYNTAX.md#L1)**: PROJECT SYNTAX
*   **[_TECH.md](_TECH.md#L1)**: Tech Stack Snapshot
*   **[debug_scanner.py](debug_scanner.py#L1)** @DEP: pathlib, sys, ndoc.atoms, ndoc.models.context
    *   `@API`
        *   `PUB:` FUN **test**`()`
*   **[debug_symbols.py](debug_symbols.py#L1)** @DEP: pathlib, sys, ndoc.atoms.ast, ndoc.atoms.io
    *   `@API`
        *   `VAL->` VAR **file_path**` = Path("src/ndoc/atoms/deps/stats.py")`
        *   `VAL->` VAR **content**` = read_text(file_path)`
        *   `VAL->` VAR **tree**` = parse_code(content, file_path)`
        *   `VAL->` VAR **symbols**` = extract_symbols(tree, content.encode("utf-8"), file_path)`
*   **[lsp_test.log](lsp_test.log#L1)**
*   **[requirements.txt](requirements.txt#L1)**: Core Dependencies
*   **[setup.py](setup.py#L1)** @DEP: setuptools
*   **[symbols_log.txt](symbols_log.txt#L1)**
*   **[test_enhanced_doc.py](test_enhanced_doc.py#L1)**: """
    *   `@API`
        *   `PUB:` FUN **test_func**`(a: int, b: str) -> bool`
        *   `PUB:` CLS **TestClass**
            *   `VAL->` VAR **field**`: int = 10`
            *   `PUB:` MET **test_method**`(self)`
*   **[test_python_fix.py](test_python_fix.py#L1)** @DEP: pathlib, sys, os, ndoc.atoms
    *   `@API`
        *   `PUB:` FUN **test_python_parsing**`()`
*   **[test_regex.py](test_regex.py#L1)** @DEP: re
    *   `@API`
        *   `VAL->` VAR **TAG_REGEX**` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s...`
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
