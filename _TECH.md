# Tech Stack Snapshot
> @CONTEXT: Global | _TECH.md | @TAGS: @TECH @DEPS
> 最后更新 (Last Updated): 2026-02-24 15:01:50

## 1. Languages (语言分布)
*   **Python**: `█████████████░░░░░░░` 66.0%
*   **Markdown**: `█████░░░░░░░░░░░░░░░` 28.3%
*   **JSON**: `░░░░░░░░░░░░░░░░░░░░` 2.8%
*   **JavaScript**: `░░░░░░░░░░░░░░░░░░░░` 0.9%
*   **TypeScript**: `░░░░░░░░░░░░░░░░░░░░` 0.9%
*   **C#**: `░░░░░░░░░░░░░░░░░░░░` 0.9%

## 2. Dependencies (依赖库)
### debug_scanner.py
*   `pathlib`
*   `sys`
*   `ndoc.atoms`
*   `ndoc.models.context`

### debug_symbols.py
*   `pathlib`
*   `sys`
*   `ndoc.atoms.ast`
*   `ndoc.atoms.io`

### requirements.txt
*   `watchdog>=6.0.0`
*   `tree-sitter>=0.23.2`
*   `pytest>=8.4.2`
*   `colorama>=0.4.6`
*   `pygls>=1.3.1`

### setup.py
*   `setuptools`

### test_python_fix.py
*   `pathlib`
*   `sys`
*   `os`
*   `ndoc.atoms`

### test_regex.py
*   `re`

### editors/vscode/package.json
*   `vscode-languageclient (^8.1.0)`
*   `@types/node (dev: ^18.14.6)`
*   `@types/vscode (dev: ^1.75.0)`
*   `typescript (dev: ^4.9.5)`

### samples/sample_csharp.cs
*   `System`

### src/ndoc/daemon.py
*   `threading`
*   `pathlib`
*   `watchdog.observers`
*   `time`
*   `ndoc.models.config`
*   `traceback`
*   `ndoc.flows`
*   `typing`
*   `watchdog.events`

### src/ndoc/entry.py
*   `sys`
*   `ndoc.daemon`
*   `pathlib`
*   `ndoc.models.config`
*   `argparse`
*   `ndoc.flows`
*   `ndoc.atoms`

### src/ndoc/lsp_server.py
*   `sys`
*   `lsprotocol.types`
*   `pathlib`
*   `os`
*   `ndoc.models`
*   `ndoc.atoms`
*   `typing`
*   `pygls.lsp.server`

### src/ndoc/atoms/cache.py
*   `pathlib`
*   `json`
*   `typing`
*   `hashlib`

### src/ndoc/atoms/capabilities.py
*   `sys`
*   `subprocess`
*   `typing`
*   `importlib`
*   `tree_sitter`

### src/ndoc/atoms/fs.py
*   `re`
*   `pathlib`
*   `os`
*   `pathspec`
*   `typing`
*   `dataclasses`

### src/ndoc/atoms/io.py
*   `re`
*   `datetime`
*   `pathlib`
*   `os`
*   `typing`
*   `difflib`

### src/ndoc/atoms/llm.py
*   `typing`
*   `os`
*   `json`
*   `urllib.request`

### src/ndoc/atoms/lsp.py
*   `pathlib`
*   `re`
*   `typing`
*   `models.context`

### src/ndoc/atoms/scanner.py
*   `text_utils`
*   `re`
*   `pathlib`
*   `atoms`
*   `models.context`
*   `typing`
*   `ast`
*   `dataclasses`
*   `atoms.ast`

### src/ndoc/atoms/text_utils.py
*   `re`
*   `typing`
*   `models.context`

### src/ndoc/atoms/ast/base.py
*   `capabilities`
*   `pathlib`
*   `typing`
*   `dataclasses`
*   `tree_sitter`

### src/ndoc/atoms/ast/discovery.py
*   `base`
*   `tree_sitter`
*   `typing`

### src/ndoc/atoms/ast/symbols.py
*   `text_utils`
*   `pathlib`
*   `utils`
*   `models.context`
*   `base`
*   `typing`
*   `tree_sitter`

### src/ndoc/atoms/ast/utils.py
*   `base`
*   `tree_sitter`
*   `typing`

### src/ndoc/atoms/ast/__init__.py
*   `base`
*   `utils`
*   `discovery`
*   `symbols`

### src/ndoc/atoms/deps/core.py
*   `stats`
*   `pathlib`
*   `typing`
*   `manifests`
*   `parsers`

### src/ndoc/atoms/deps/manifests.py
*   `pathlib`
*   `json`
*   `re`
*   `typing`

### src/ndoc/atoms/deps/parsers.py
*   `typing`
*   `re`
*   `ast`

### src/ndoc/atoms/deps/stats.py
*   `pathlib`
*   `typing`

### src/ndoc/atoms/deps/__init__.py
*   `parsers`
*   `stats`
*   `manifests`
*   `core`

### src/ndoc/atoms/langs/python.py
*   `tree_sitter`
*   `typing`

### src/ndoc/atoms/langs/__init__.py
*   `text_utils`
*   `pkgutil`
*   `pathlib`
*   `typing`
*   `importlib`
*   `tree_sitter`

### src/ndoc/flows/archive_flow.py
*   `re`
*   `datetime`
*   `pathlib`
*   `models.config`
*   `atoms`

### src/ndoc/flows/capability_flow.py
*   `pathlib`
*   `models.config`
*   `typing`
*   `atoms`

### src/ndoc/flows/clean_flow.py
*   `pathlib`
*   `ndoc.models.config`
*   `os`
*   `typing`

### src/ndoc/flows/config_flow.py
*   `re`
*   `pathlib`
*   `ndoc.models.config`
*   `ndoc.atoms`
*   `typing`

### src/ndoc/flows/context_flow.py
*   `re`
*   `datetime`
*   `pathlib`
*   `models.config`
*   `atoms`
*   `models.context`
*   `typing`
*   `dataclasses`

### src/ndoc/flows/data_flow.py
*   `datetime`
*   `pathlib`
*   `models.config`
*   `atoms`
*   `models.context`
*   `typing`
*   `dataclasses`

### src/ndoc/flows/deps_flow.py
*   `datetime`
*   `pathlib`
*   `models.config`
*   `atoms`
*   `typing`
*   `collections`

### src/ndoc/flows/doctor_flow.py
*   `sys`
*   `platform`
*   `pathlib`
*   `atoms.capabilities`
*   `ndoc.models.config`
*   `typing`
*   `importlib`
*   `tree_sitter`
*   `shutil`

### src/ndoc/flows/init_flow.py
*   `ndoc.models.config`
*   `ndoc.flows`

### src/ndoc/flows/map_flow.py
*   `datetime`
*   `pathlib`
*   `models.config`
*   `concurrent.futures`
*   `atoms`
*   `typing`
*   `dataclasses`

### src/ndoc/flows/plan_flow.py
*   `pathlib`
*   `models.config`
*   `datetime`
*   `atoms`

### src/ndoc/flows/prompt_flow.py
*   `re`
*   `pathlib`
*   `models.config`
*   `atoms`
*   `typing`

### src/ndoc/flows/stats_flow.py
*   `re`
*   `datetime`
*   `pathlib`
*   `time`
*   `os`
*   `ndoc.models.config`
*   `ndoc.atoms`

### src/ndoc/flows/symbols_flow.py
*   `datetime`
*   `pathlib`
*   `models.config`
*   `atoms`
*   `models.context`
*   `typing`
*   `collections`

### src/ndoc/flows/syntax_flow.py
*   `pathlib`
*   `ndoc.models.config`
*   `ndoc.atoms`

### src/ndoc/flows/tech_flow.py
*   `pathlib`
*   `ndoc.models.config`
*   `ndoc.atoms`
*   `datetime`

### src/ndoc/flows/todo_flow.py
*   `re`
*   `datetime`
*   `pathlib`
*   `models.config`
*   `atoms`
*   `typing`
*   `dataclasses`

### src/ndoc/flows/update_flow.py
*   `pathlib`
*   `sys`
*   `subprocess`
*   `typing`

### src/ndoc/flows/verify_flow.py
*   `sys`
*   `ndoc.models.config`
*   `atoms`

### src/ndoc/models/config.py
*   `pathlib`
*   `typing`
*   `dataclasses`

### src/ndoc/models/context.py
*   `pathlib`
*   `typing`
*   `dataclasses`

### tests/conftest.py
*   `pathlib`
*   `sys`

### tests/test_ast.py
*   `ndoc.atoms.ast`
*   `ndoc.models.context`
*   `pathlib`
*   `pytest`
*   `ndoc.atoms.io`

### tests/test_capabilities.py
*   `unittest`
*   `sys`
*   `ndoc.atoms.capabilities`
*   `os`
*   `unittest.mock`

### tests/test_capability_flow.py
*   `unittest`
*   `sys`
*   `pathlib`
*   `ndoc.models.config`
*   `os`
*   `ndoc.flows`
*   `unittest.mock`

### tests/test_csharp_api.py
*   `pathlib`
*   `sys`
*   `ndoc.atoms`

### tests/test_lsp_server.py
*   `sys`
*   `json`
*   `threading`
*   `time`
*   `os`
*   `subprocess`

### tests/test_scanner.py
*   `pathlib`
*   `pytest`
*   `ndoc.atoms.scanner`

### tests/fixtures/complex_api.py
*   `typing`
*   `dataclasses`

## 3. Environment (开发环境)
*   **OS**: Windows (Detected)
*   **Python**: Detected via file extension

---
*Generated by Niki-docAI*
