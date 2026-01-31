# Context: atoms
> @CONTEXT: Local | atoms | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 02:25:59

## !RULE
*   **Cache Logic**: `cache.py` uses MD5 hashing to detect file changes. Cache is stored in `.ndoc/cache/scan_cache.json`.
*   **AST Dependency**: `deps.py` prefers AST-based extraction for Python to avoid regex false positives, but falls back to regex if syntax is invalid.
*   **AST Symbol Extraction**: `ast.py` is the core engine for extracting classes, functions, and metadata (decorators, bases). It is language-agnostic via SCM queries.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[langs/](langs/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: Atoms: File System Operations.
*   **[ast.py](ast.py#L1)**: Atoms: AST Parsing (Tree-sitter Wrapper). @DEP: dataclasses, models.context, pathlib, tree_sitter, tree_sitter_c_sharp, tree_sitter_cpp, tree_sitter_dart, tree_sitter_go, tree_sitter_java, tree_sitter_javascript, tree_sitter_python, tree_sitter_rust, tree_sitter_typescript, typing
*   **[cache.py](cache.py#L1)**: Atoms: Cache Management. @DEP: hashlib, json, pathlib, typing
*   **[deps.py](deps.py#L1)**: Atom: Dependency Parser. @DEP: ast, configparser, json, pathlib, re, typing
*   **[fs.py](fs.py#L1)**: Atoms: File System Traversal. @DEP: dataclasses, os, pathlib, pathspec, re, typing
*   **[io.py](io.py#L1)**: Atoms: Input/Output Operations. @DEP: datetime, difflib, os, pathlib, re, typing
*   **[llm.py](llm.py#L1)**: Atoms: LLM Connector. @DEP: json, os, typing, urllib.request
*   **[scanner.py](scanner.py#L1)**: Atoms: Content Scanner. @DEP: atoms, atoms.ast, dataclasses, models.context, pathlib, re, typing
<!-- NIKI_AUTO_Context_END -->
