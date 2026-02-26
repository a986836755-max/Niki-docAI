# Context: core
> @CONTEXT: Local | core | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:27:55

## !RULE
*   **Explicit Exports**: `__init__.py` MUST remain empty. Consumers MUST import submodules directly (e.g., `from ndoc.core import fs`) to avoid circular dependencies and namespace pollution.
*   **Unified Logging**: ALL internal status/debug messages MUST use `ndoc.core.logger`. `print()` is forbidden except for CLI data output.
*   **Unified File Scanning**: ALL file traversal logic MUST use `fs.scan_project_files`. This generator centralizes `.gitignore` handling, binary file filtering, and extension filtering.
*   **Safe IO**: ALL file operations MUST use `io.safe_io` or `io.read_*/write_*` helpers to ensure encoding safety and consistent error handling.
*   **Error Handling**: Use `ndoc.core.errors.NdocError` hierarchy for domain-specific exceptions.
*   **Native Bindings**: `capabilities.py` must support loading manually compiled language bindings (e.g., `tree_sitter_dart.dll`) from `langs/bin/` to bypass PyPI package limitations on Windows.
*   **Dart DLL Compatibility**: Dart DLL 加载需同时兼容 `Language(path, name)` 与 `Language.load(path)` 两种 API 形式。
*   **Dart Install Guard**: Windows 下不得尝试通过 PyPI 安装 `tree-sitter-dart`，必须优先使用 `langs/bin/tree_sitter_dart.dll`。
*   **@ANALYSIS**: 能力加载前必须初始化本地 `.ndoc/lib`，避免混用全局 `tree_sitter`。
*   **Capability Isolation**: `capabilities.py` prioritizes project-local `.ndoc/lib` for dependency installation if `.ndoc` exists in the current working directory. This ensures project-specific isolation while falling back to `~/.ndoc/lib` for global use.
*   **Tree-sitter Bootstrap**: `_init_local_lib` runs the tree-sitter bootstrap once per process to avoid repeated pip installs during multi-language checks.
*   **Tree-sitter Version Gate**: 本地 `tree-sitter` 版本需满足语言绑定对 PyCapsule 的要求，必要时自动升级。

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Core: Infrastructure Utilities.
*   **[capabilities.py](capabilities.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: importlib, ndoc, os, pathlib, subprocess, ... @DEP: subprocess, ndoc, tree_sitter, typing, time, pathlib, sys, importlib ...
*   **[errors.py](errors.py#L1)**: Custom exceptions for ndoc.
*   **[fs.py](fs.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: dataclasses, os, pathlib, pathspec, re, ... @DEP: re, pathspec, typing, dataclasses, pathlib, os
*   **[io.py](io.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: datetime, difflib, os, pathlib, re, ... @DEP: re, difflib, typing, datetime, pathlib, os
*   **[logger.py](logger.py#L1)**: Standardized logging for ndoc. @DEP: logging, sys, typing @DEP: sys, typing, logging
*   **[native_builder.py](native_builder.py#L1)**: Native Builder: Handles local compilation of language bindings on Windows. @DEP: .logger, os, pathlib, shutil, subprocess, ... @DEP: subprocess, typing, .logger, shutil, sys, pathlib, os
*   **[text_utils.py](text_utils.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..models.context, re, typing @DEP: ..models.context, re, typing
<!-- NIKI_AUTO_Context_END -->
