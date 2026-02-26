# Context: langs
> @CONTEXT: Local | langs | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:28:00

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Python Dual Docstrings**: Python 模块应同时支持传统的 `#` 注释（位于定义上方）和 PEP 257 定义的内部字符串字面量（定义内部第一行）。`python.py` 已经增强了 `extract_docstring` 来合并这两者，确保语义提取的完整性。
*   **Tree-sitter Dart on Windows**: Windows 环境下 PyPI 的 `tree-sitter-dart` 缺失预编译二进制。必须使用 MSVC (vcvars64.bat) 本地编译并将 `tree_sitter_dart.dll` 放置在 `langs/bin/` 目录下。`capabilities.py` 已增加自定义加载逻辑。
*   **SCM Query Precision**: C++ `preproc_include` 必须显式捕获 `path` 节点；Dart `import_directive` 必须清理引号和 `package:` 前缀。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[bin/](bin/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ...core.text_utils, importlib, json, pathlib, pkgutil, ... @DEP: pkgutil, tree_sitter, typing, ...core.text_utils, json, pathlib, importlib
*   **[cpp.py](cpp.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: . @DEP: .
*   **[csharp.py](csharp.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: . @DEP: .
*   **[dart.py](dart.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ., re @DEP: re, .
*   **[go.py](go.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: . @DEP: .
*   **[java.py](java.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: . @DEP: .
*   **[javascript.py](javascript.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: . @DEP: .
*   **[python.py](python.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ., ...core.text_utils, tree_sitter, typing @DEP: ., tree_sitter, typing, ...core.text_utils
*   **[rust.py](rust.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: . @DEP: .
*   **[typescript.py](typescript.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: . @DEP: .
<!-- NIKI_AUTO_Context_END -->
