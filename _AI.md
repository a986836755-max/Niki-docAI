# Context: nk_doc_ai
> @CONTEXT: Local | nk_doc_ai | @TAGS: @LOCAL @LSP @IDE @PROTO
> 最后更新 (Last Updated): 2026-02-26 12:28:12

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
- LSP 适配：所有 IDE 插件相关的语义能力通过 `ndoc.lsp_server` 暴露。
- 架构感知：IDE 插件应优先使用 `_MAP.md` 和 `_AI.md` 进行语义增强，而非仅依赖语法树。
- @TECH: Windows 环境下 Dart 解析依赖 `langs/bin/tree_sitter_dart.dll`，PyPI 依赖需跳过。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[editors/](editors/_AI.md#L1)**
*   **[samples/](samples/_AI.md#L1)**
*   **[scripts/](scripts/_AI.md#L1)**
*   **[src/](src/_AI.md#L1)**
*   **[temp_build_dart/](temp_build_dart/_AI.md#L1)**
*   **[test_vectordb_root/](test_vectordb_root/_AI.md#L1)**
*   **[tests/](tests/_AI.md#L1)**
*   **[tools/](tools/_AI.md#L1)**
*   **[README.md](README.md#L1)**: Niki-docAI 2.0 (Rebirth)
*   **[README_zh.md](README_zh.md#L1)**: Niki-docAI 2.0 (重生版)
*   **[_ARCH.md](_ARCH.md#L1)**: Project Architecture
*   **[_DATA.md](_DATA.md#L1)**: Data Registry
*   **[_DEPS.md](_DEPS.md#L1)**: Dependency Graph
*   **[_DOGFOOD.md](_DOGFOOD.md#L1)**: Niki-docAI 2.0: Dogfooding Report
*   **[_GUIDE.md](_GUIDE.md#L1)**: AI Context Guide (Niki-docAI)
*   **[_MAP.md](_MAP.md#L1)**: Project Map
*   **[_MEMORY.md](_MEMORY.md#L1)**: Project Memory
*   **[_RULES.md](_RULES.md#L1)**: Project Rules
*   **[_STATS.md](_STATS.md#L1)**: 项目统计报告 (Project Statistics)
*   **[_STATUS.md](_STATUS.md#L1)**: Project Status Board
*   **[_SYNTAX.md](_SYNTAX.md#L1)**: PROJECT SYNTAX
*   **[debug_cpp.py](debug_cpp.py#L1)** @DEP: importlib, pathlib, sys, tree_sitter, tree_sitter_cpp @DEP: tree_sitter, tree_sitter_cpp, sys, pathlib, importlib
*   **[debug_env.py](debug_env.py#L1)** @DEP: importlib, pkg_resources, sys, tree_sitter @DEP: pkg_resources, sys, importlib, tree_sitter
*   **[debug_scanner.py](debug_scanner.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.atoms, ndoc.models.context, pathlib, sys @DEP: ndoc.models.context, sys, pathlib, ndoc.atoms
*   **[debug_symbols.py](debug_symbols.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.core.io, ndoc.parsing.ast, pathlib, sys @DEP: sys, ndoc.core.io, pathlib, ndoc.parsing.ast
*   **[lsp_test.log](lsp_test.log#L1)**
*   **[ndoc.ps1](ndoc.ps1#L1)**
*   **[requirements.txt](requirements.txt#L1)**
*   **[setup.py](setup.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: setuptools @DEP: setuptools
*   **[symbols_log.txt](symbols_log.txt#L1)**
*   **[test_enhanced_doc.py](test_enhanced_doc.py#L1)**: <NIKI_AUTO_HEADER_START>
*   **[test_python_fix.py](test_python_fix.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.parsing, os, pathlib, sys @DEP: sys, ndoc.parsing, pathlib, os
*   **[test_regex.py](test_regex.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re @DEP: re
<!-- NIKI_AUTO_Context_END -->
