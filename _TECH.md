# Tech Stack Snapshot
> @CONTEXT: Global | _TECH.md | @TAGS: @TECH @DEPS
> 最后更新 (Last Updated): 2026-01-31 16:50:58

## 1. Languages (语言分布)
*   **Python**: `████████░░░░░░░░░░░░` 40.6%
*   **Markdown**: `█████░░░░░░░░░░░░░░░` 29.7%
*   **Dart**: `██░░░░░░░░░░░░░░░░░░` 11.5%
*   **YAML**: `░░░░░░░░░░░░░░░░░░░░` 3.6%
*   **C/C++ Header**: `░░░░░░░░░░░░░░░░░░░░` 3.0%
*   **JavaScript**: `░░░░░░░░░░░░░░░░░░░░` 2.4%
*   **JSON**: `░░░░░░░░░░░░░░░░░░░░` 2.4%
*   **C**: `░░░░░░░░░░░░░░░░░░░░` 1.8%
*   **Go**: `░░░░░░░░░░░░░░░░░░░░` 1.2%
*   **Rust**: `░░░░░░░░░░░░░░░░░░░░` 1.2%
*   **C#**: `░░░░░░░░░░░░░░░░░░░░` 0.6%
*   **HTML**: `░░░░░░░░░░░░░░░░░░░░` 0.6%
*   **Shell**: `░░░░░░░░░░░░░░░░░░░░` 0.6%
*   **TypeScript**: `░░░░░░░░░░░░░░░░░░░░` 0.6%

## 2. Dependencies (依赖库)
### debug_scanner.py
*   `pathlib.Path`
*   `ndoc.atoms.scanner`
*   `ndoc.models.context`
*   `ndoc.models.context.Symbol`
*   `sys`
*   `ndoc.atoms`
*   `pathlib`

### debug_symbols.py
*   `ndoc.atoms.ast.extract_symbols`
*   `ndoc.atoms.ast.MAX_VALUE_LENGTH`
*   `ndoc.atoms.io.read_text`
*   `pathlib.Path`
*   `ndoc.atoms.ast.parse_code`
*   `ndoc.atoms.ast`
*   `sys`
*   `ndoc.atoms.io`
*   `pathlib`

### requirements.txt
*   `watchdog>=6.0.0`
*   `tree-sitter>=0.23.2`
*   `tree-sitter-python>=0.23.6`
*   `tree-sitter-cpp>=0.23.4`
*   `tree-sitter-javascript>=0.23.1`
*   `tree-sitter-typescript>=0.23.2`
*   `tree-sitter-go>=0.23.4`
*   `tree-sitter-rust>=0.23.2`
*   `tree-sitter-dart>=0.23.2`
*   `tree-sitter-c-sharp>=0.23.1`
*   `tree-sitter-java>=0.23.5`
*   `pytest>=8.4.2`
*   `colorama>=0.4.6`
*   `pygls>=1.3.1`

### setup.py
*   `setuptools.find_packages`
*   `setuptools`
*   `setuptools.setup`

### test_python_fix.py
*   `ndoc.atoms.queries`
*   `os`
*   `pathlib.Path`
*   `ndoc.atoms.ast`
*   `sys`
*   `ndoc.atoms`
*   `pathlib`

### test_regex.py
*   `re`

### samples/sample_csharp.cs
*   `System`

### src/ndoc/daemon.py
*   `watchdog.observers.Observer`
*   `ndoc.flows.symbols_flow`
*   `ndoc.flows.tech_flow`
*   `watchdog.events.FileSystemEvent`
*   `ndoc.flows.deps_flow`
*   `pathlib.Path`
*   `ndoc.flows`
*   `pathlib`
*   `typing.List`
*   `ndoc.flows.context_flow`
*   `typing.Callable`
*   `time`
*   `ndoc.flows.data_flow`
*   `ndoc.flows.map_flow`
*   `watchdog.events.FileSystemEventHandler`
*   `typing.Set`
*   `typing`
*   `ndoc.flows.archive_flow`
*   `ndoc.models.config`
*   `traceback`
*   `threading`
*   `ndoc.flows.todo_flow`
*   `watchdog.events`
*   `ndoc.models.config.ProjectConfig`
*   `watchdog.observers`

### src/ndoc/entry.py
*   `ndoc.flows.config_flow`
*   `ndoc.flows.tech_flow`
*   `ndoc.flows.syntax_flow`
*   `ndoc.flows.verify_flow`
*   `ndoc.flows.deps_flow`
*   `ndoc.flows.doctor_flow`
*   `ndoc.flows.clean_flow`
*   `ndoc.models.config.ScanConfig`
*   `pathlib.Path`
*   `ndoc.flows`
*   `ndoc.atoms.lsp`
*   `sys`
*   `ndoc.flows.init_flow`
*   `ndoc.flows.plan_flow`
*   `ndoc.atoms`
*   `pathlib`
*   `ndoc.flows.stats_flow`
*   `ndoc.flows.context_flow`
*   `argparse`
*   `ndoc.flows.update_flow`
*   `ndoc.flows.data_flow`
*   `ndoc.flows.map_flow`
*   `ndoc.daemon`
*   `ndoc.flows.archive_flow`
*   `ndoc.models.config`
*   `ndoc.flows.todo_flow`
*   `ndoc.atoms.fs`
*   `ndoc.atoms.io`
*   `ndoc.daemon.start_watch_mode`
*   `ndoc.models.config.ProjectConfig`
*   `ndoc.flows.symbols_flow`

### src/ndoc/lsp_server.py
*   `lsprotocol.types.INITIALIZE`
*   `pygls.server.LanguageServer`
*   `pathlib.Path`
*   `ndoc.atoms.lsp`
*   `sys`
*   `lsprotocol.types`
*   `ndoc.atoms`
*   `lsprotocol.types.TEXT_DOCUMENT_DID_OPEN`
*   `pathlib`
*   `typing.List`
*   `pygls.server`
*   `lsprotocol.types.TextDocumentItem`
*   `lsprotocol.types.HoverParams`
*   `ndoc.atoms.scanner`
*   `lsprotocol.types.MarkupContent`
*   `typing`
*   `ndoc.models`
*   `ndoc.models.config`
*   `os`
*   `lsprotocol.types.TEXT_DOCUMENT_HOVER`
*   `ndoc.atoms.fs`
*   `typing.Optional`
*   `lsprotocol.types.MarkupKind`
*   `lsprotocol.types.Hover`

### src/ndoc/atoms/cache.py
*   `json`
*   `typing.Any`
*   `typing`
*   `pathlib.Path`
*   `typing.Dict`
*   `hashlib`
*   `typing.Optional`
*   `pathlib`

### src/ndoc/atoms/fs.py
*   `typing.List`
*   `typing.Set`
*   `typing`
*   `os`
*   `dataclasses`
*   `pathlib.Path`
*   `dataclasses.dataclass`
*   `dataclasses.field`
*   `typing.Iterator`
*   `pathspec`
*   `typing.Optional`
*   `re`
*   `typing.Pattern`
*   `typing.Callable`
*   `pathlib`

### src/ndoc/atoms/io.py
*   `typing.List`
*   `typing.Any`
*   `typing`
*   `datetime`
*   `datetime.datetime`
*   `os`
*   `pathlib.Path`
*   `typing.Optional`
*   `typing.Union`
*   `re`
*   `typing.Callable`
*   `difflib`
*   `pathlib`

### src/ndoc/atoms/llm.py
*   `json`
*   `typing.Any`
*   `typing`
*   `os`
*   `typing.Dict`
*   `typing.Optional`
*   `urllib.request`

### src/ndoc/atoms/lsp.py
*   `typing.List`
*   `typing.Any`
*   `typing`
*   `pathlib.Path`
*   `typing.Dict`
*   `typing.Optional`
*   `re`
*   `models.context.Symbol`
*   `models.context`
*   `pathlib`

### src/ndoc/atoms/scanner.py
*   `atoms.ast.extract_symbols`
*   `typing.Dict`
*   `typing.Pattern`
*   `atoms.io`
*   `dataclasses.dataclass`
*   `dataclasses`
*   `pathlib.Path`
*   `ast.get_lang_key`
*   `atoms.ast.parse_code`
*   `models.context.Section`
*   `ast.find_calls`
*   `atoms.ast`
*   `models.context`
*   `pathlib`
*   `typing.List`
*   `typing.Any`
*   `text_utils`
*   `text_utils.TAG_REGEX`
*   `atoms.cache`
*   `text_utils.clean_docstring`
*   `models.context.Tag`
*   `atoms`
*   `typing`
*   `ast`
*   `ast.find_imports`
*   `dataclasses.field`
*   `typing.Iterator`
*   `typing.Optional`
*   `re`
*   `models.context.Symbol`
*   `text_utils.extract_tags_from_text`

### src/ndoc/atoms/text_utils.py
*   `models.context.Tag`
*   `typing.List`
*   `typing`
*   `typing.Optional`
*   `re`
*   `models.context`

### src/ndoc/atoms/ast/base.py
*   `tree_sitter_c_sharp`
*   `typing.Dict`
*   `tree_sitter_typescript`
*   `tree_sitter.Language`
*   `tree_sitter_cpp`
*   `tree_sitter_go`
*   `pathlib.Path`
*   `dataclasses`
*   `tree_sitter.Tree`
*   `dataclasses.dataclass`
*   `tree_sitter_python`
*   `tree_sitter_dart`
*   `tree_sitter_javascript`
*   `pathlib`
*   `typing`
*   `tree_sitter.Parser`
*   `dataclasses.field`
*   `typing.Optional`
*   `tree_sitter_java`
*   `tree_sitter`
*   `tree_sitter_rust`

### src/ndoc/atoms/ast/discovery.py
*   `typing.List`
*   `base`
*   `typing`
*   `base.query_tree`
*   `tree_sitter.Tree`
*   `base.get_language`
*   `tree_sitter`

### src/ndoc/atoms/ast/symbols.py
*   `utils._is_inside_function`
*   `utils.MAX_VALUE_LENGTH`
*   `utils.truncate`
*   `pathlib.Path`
*   `tree_sitter.Tree`
*   `utils`
*   `models.context`
*   `pathlib`
*   `utils._get_parent_name`
*   `typing.List`
*   `text_utils`
*   `utils._extract_docstring_from_node`
*   `base.get_language`
*   `base`
*   `typing`
*   `utils.MAX_CONTENT_LENGTH`
*   `typing.Optional`
*   `models.context.Symbol`
*   `tree_sitter`
*   `utils._is_async_function`
*   `text_utils.extract_tags_from_text`

### src/ndoc/atoms/ast/utils.py
*   `base`
*   `typing`
*   `base.query_tree`
*   `base.AstNode`
*   `tree_sitter.Node`
*   `typing.Optional`
*   `tree_sitter`

### src/ndoc/atoms/ast/__init__.py
*   `base`
*   `base.get_parser`
*   `utils.MAX_VALUE_LENGTH`
*   `base.query_tree`
*   `discovery.find_calls`
*   `base.AstNode`
*   `utils.MAX_CONTENT_LENGTH`
*   `utils.truncate`
*   `base.get_language`
*   `symbols`
*   `base.parse_code`
*   `utils`
*   `symbols.extract_symbols`
*   `discovery.find_imports`
*   `base.get_lang_key`
*   `discovery`
*   `utils.node_to_data`

### src/ndoc/atoms/deps/core.py
*   `parsers.extract_imports`
*   `typing.Dict`
*   `manifests.parse_csproj`
*   `manifests.parse_pyproject_toml`
*   `stats.DEFAULT_IGNORE_PATTERNS`
*   `parsers.extract_dart_imports`
*   `pathlib.Path`
*   `manifests.parse_package_json`
*   `pathlib`
*   `typing.List`
*   `manifests`
*   `manifests.parse_pubspec_yaml`
*   `typing.Set`
*   `parsers.extract_csharp_usings`
*   `manifests.parse_cmake_lists`
*   `typing`
*   `parsers.extract_cpp_includes`
*   `stats`
*   `manifests.parse_requirements_txt`
*   `parsers`

### src/ndoc/atoms/deps/manifests.py
*   `json`
*   `typing.List`
*   `typing`
*   `pathlib.Path`
*   `re`
*   `pathlib`

### src/ndoc/atoms/deps/parsers.py
*   `typing.List`
*   `typing`
*   `re`
*   `ast`

### src/ndoc/atoms/deps/stats.py
*   `typing.Set`
*   `typing`
*   `pathlib.Path`
*   `typing.Dict`
*   `typing.Counter`
*   `pathlib`

### src/ndoc/atoms/deps/__init__.py
*   `core.get_project_dependencies`
*   `parsers.extract_imports`
*   `stats.detect_languages`
*   `manifests.parse_csproj`
*   `manifests.parse_pyproject_toml`
*   `core`
*   `stats.DEFAULT_IGNORE_PATTERNS`
*   `parsers.extract_dart_imports`
*   `core.extract_dependencies`
*   `stats.LANGUAGE_EXTENSIONS`
*   `manifests.parse_package_json`
*   `core.SOURCE_PARSERS`
*   `manifests`
*   `manifests.parse_pubspec_yaml`
*   `parsers.extract_csharp_usings`
*   `manifests.parse_cmake_lists`
*   `parsers.extract_cpp_includes`
*   `stats`
*   `manifests.parse_requirements_txt`
*   `parsers`

### src/ndoc/atoms/langs/python.py
*   `typing.Any`
*   `typing`
*   `tree_sitter.Node`
*   `typing.Optional`
*   `tree_sitter`

### src/ndoc/atoms/langs/__init__.py
*   `typing.List`
*   `typing.Type`
*   `typing.Any`
*   `pkgutil`
*   `typing`
*   `text_utils`
*   `pathlib.Path`
*   `importlib`
*   `typing.Dict`
*   `tree_sitter.Node`
*   `typing.Optional`
*   `tree_sitter`
*   `pathlib`
*   `text_utils.clean_docstring`

### src/ndoc/flows/archive_flow.py
*   `atoms`
*   `datetime.datetime`
*   `datetime`
*   `atoms.llm`
*   `atoms.io`
*   `models.config.ProjectConfig`
*   `pathlib.Path`
*   `re`
*   `models.config`
*   `pathlib`

### src/ndoc/flows/clean_flow.py
*   `typing.List`
*   `typing`
*   `ndoc.models.config`
*   `os`
*   `pathlib.Path`
*   `typing.Optional`
*   `ndoc.models.config.ProjectConfig`
*   `pathlib`

### src/ndoc/flows/config_flow.py
*   `typing.List`
*   `typing.Set`
*   `typing`
*   `ndoc.models.config`
*   `ndoc.models.config.ScanConfig`
*   `pathlib.Path`
*   `re`
*   `ndoc.atoms`
*   `ndoc.atoms.io`
*   `ndoc.models.config.ProjectConfig`
*   `pathlib`

### src/ndoc/flows/context_flow.py
*   `models.context.FileContext`
*   `datetime`
*   `atoms.io`
*   `dataclasses.dataclass`
*   `dataclasses`
*   `pathlib.Path`
*   `atoms.scanner`
*   `atoms.ast`
*   `models.context`
*   `models.config`
*   `pathlib`
*   `models.context.DirectoryContext`
*   `atoms.deps`
*   `typing.List`
*   `datetime.datetime`
*   `models.config.ProjectConfig`
*   `atoms`
*   `typing`
*   `dataclasses.field`
*   `typing.Optional`
*   `re`
*   `atoms.fs`

### src/ndoc/flows/data_flow.py
*   `typing.Dict`
*   `datetime`
*   `atoms.io`
*   `pathlib.Path`
*   `dataclasses`
*   `dataclasses.dataclass`
*   `atoms.scanner`
*   `atoms.ast`
*   `models.context`
*   `models.config`
*   `pathlib`
*   `typing.List`
*   `typing.Any`
*   `datetime.datetime`
*   `models.config.ProjectConfig`
*   `atoms`
*   `typing`
*   `models.context.Symbol`
*   `atoms.fs`

### src/ndoc/flows/deps_flow.py
*   `atoms`
*   `typing.List`
*   `typing.Set`
*   `atoms.deps`
*   `typing`
*   `datetime.datetime`
*   `datetime`
*   `atoms.io`
*   `models.config.ProjectConfig`
*   `collections.defaultdict`
*   `pathlib.Path`
*   `typing.Dict`
*   `models.config`
*   `atoms.fs`
*   `pathlib`
*   `collections`

### src/ndoc/flows/doctor_flow.py
*   `typing.List`
*   `typing`
*   `ndoc.models.config`
*   `tree_sitter.Language`
*   `platform`
*   `importlib`
*   `pathlib.Path`
*   `tree_sitter.Parser`
*   `tree_sitter_python`
*   `sys`
*   `tree_sitter`
*   `shutil`
*   `typing.Tuple`
*   `ndoc.models.config.ProjectConfig`
*   `pathlib`

### src/ndoc/flows/init_flow.py
*   `ndoc.flows.config_flow`
*   `ndoc.models.config`
*   `ndoc.flows`
*   `ndoc.flows.syntax_flow`
*   `ndoc.models.config.ProjectConfig`

### src/ndoc/flows/map_flow.py
*   `atoms`
*   `typing.List`
*   `datetime.datetime`
*   `datetime`
*   `typing`
*   `concurrent.futures.ThreadPoolExecutor`
*   `atoms.io`
*   `models.config.ProjectConfig`
*   `dataclasses`
*   `pathlib.Path`
*   `dataclasses.dataclass`
*   `typing.Dict`
*   `concurrent.futures`
*   `atoms.scanner`
*   `typing.Callable`
*   `models.config`
*   `atoms.fs`
*   `pathlib`

### src/ndoc/flows/plan_flow.py
*   `atoms`
*   `datetime.datetime`
*   `datetime`
*   `atoms.llm`
*   `atoms.io`
*   `models.config.ProjectConfig`
*   `pathlib.Path`
*   `models.config`
*   `atoms.fs`
*   `pathlib`

### src/ndoc/flows/stats_flow.py
*   `datetime.datetime`
*   `datetime`
*   `ndoc.models.config`
*   `os`
*   `pathlib.Path`
*   `re`
*   `ndoc.atoms`
*   `ndoc.atoms.io`
*   `time`
*   `ndoc.models.config.ProjectConfig`
*   `pathlib`

### src/ndoc/flows/symbols_flow.py
*   `typing.Dict`
*   `collections`
*   `datetime`
*   `atoms.io`
*   `collections.defaultdict`
*   `pathlib.Path`
*   `atoms.lsp`
*   `atoms.scanner`
*   `atoms.ast`
*   `models.context`
*   `models.config`
*   `pathlib`
*   `typing.List`
*   `datetime.datetime`
*   `models.config.ProjectConfig`
*   `atoms`
*   `typing`
*   `typing.Optional`
*   `models.context.Symbol`
*   `atoms.fs`

### src/ndoc/flows/syntax_flow.py
*   `ndoc.models.config`
*   `pathlib.Path`
*   `ndoc.atoms`
*   `ndoc.atoms.io`
*   `ndoc.models.config.ProjectConfig`
*   `pathlib`

### src/ndoc/flows/tech_flow.py
*   `datetime.datetime`
*   `datetime`
*   `ndoc.models.config`
*   `pathlib.Path`
*   `ndoc.atoms`
*   `ndoc.atoms.io`
*   `ndoc.models.config.ProjectConfig`
*   `pathlib`
*   `ndoc.atoms.deps`

### src/ndoc/flows/todo_flow.py
*   `atoms`
*   `typing.List`
*   `datetime.datetime`
*   `datetime`
*   `typing`
*   `atoms.io`
*   `models.config.ProjectConfig`
*   `pathlib.Path`
*   `dataclasses`
*   `dataclasses.dataclass`
*   `typing.Dict`
*   `typing.Optional`
*   `re`
*   `atoms.scanner`
*   `models.config`
*   `atoms.fs`
*   `pathlib`

### src/ndoc/flows/update_flow.py
*   `typing`
*   `pathlib.Path`
*   `typing.Optional`
*   `sys`
*   `subprocess`
*   `pathlib`

### src/ndoc/flows/verify_flow.py
*   `atoms`
*   `ndoc.models.config`
*   `atoms.io`
*   `atoms.fs`
*   `sys`
*   `atoms.scanner`
*   `ndoc.models.config.ProjectConfig`

### src/ndoc/models/config.py
*   `typing.List`
*   `typing`
*   `dataclasses.dataclass`
*   `pathlib.Path`
*   `dataclasses`
*   `dataclasses.field`
*   `typing.Optional`
*   `pathlib`

### src/ndoc/models/context.py
*   `typing.List`
*   `typing.Any`
*   `typing`
*   `dataclasses.dataclass`
*   `pathlib.Path`
*   `dataclasses`
*   `dataclasses.field`
*   `typing.Dict`
*   `typing.Optional`
*   `pathlib`

### tests/conftest.py
*   `sys`
*   `pathlib.Path`
*   `pathlib`

### tests/test_ast.py
*   `ndoc.atoms.ast.extract_symbols`
*   `ndoc.atoms.io.read_text`
*   `pathlib.Path`
*   `ndoc.atoms.ast.parse_code`
*   `ndoc.models.context`
*   `ndoc.atoms.ast`
*   `ndoc.models.context.Symbol`
*   `ndoc.atoms.io`
*   `pytest`
*   `pathlib`

### tests/test_csharp_api.py
*   `pathlib.Path`
*   `ndoc.atoms.ast`
*   `sys`
*   `ndoc.atoms`
*   `ndoc.atoms.io`
*   `pathlib`

### tests/test_lsp_server.py
*   `json`
*   `time`
*   `sys`
*   `subprocess`

### tests/test_scanner.py
*   `pathlib.Path`
*   `ndoc.atoms.scanner`
*   `ndoc.atoms.scanner.scan_file_content`
*   `pytest`
*   `pathlib`

### tests/fixtures/complex_api.py
*   `dataclasses.dataclass`
*   `dataclasses`
*   `typing`

### vendors/tree-sitter-dart/package.json
*   `node-addon-api (^7.1.0)`
*   `node-gyp-build (^4.8.0)`
*   `node-gyp (dev: ^10.2.0)`
*   `npm-watch (dev: ^0.13.0)`
*   `tree-sitter-cli (dev: ^0.25.10)`
*   `prebuildify (dev: ^6.0.0)`

### vendors/tree-sitter-dart/pubspec.yaml
*   `path`

### vendors/tree-sitter-dart/setup.py
*   `platform.system`
*   `setuptools.setup`
*   `setuptools.Extension`
*   `platform`
*   `wheel.bdist_wheel`
*   `wheel.bdist_wheel.bdist_wheel`
*   `setuptools.command.build.build`
*   `setuptools.command.build`
*   `setuptools`
*   `setuptools.find_packages`
*   `os.path.join`
*   `os.path`
*   `os.path.isdir`

### vendors/tree-sitter-dart/bindings/node/binding.cc
*   `napi.h`

### vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/binding.c
*   `Python.h`

### vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/__init__.py
*   `_binding`
*   `_binding.language`

### vendors/tree-sitter-dart/src/parser.c
*   `tree_sitter/parser.h`

### vendors/tree-sitter-dart/src/scanner.c
*   `tree_sitter/parser.h`
*   `wctype.h`

### vendors/tree-sitter-dart/src/tree_sitter/alloc.h
*   `stdbool.h`
*   `stdio.h`
*   `stdlib.h`

### vendors/tree-sitter-dart/src/tree_sitter/array.h
*   `./alloc.h`
*   `assert.h`
*   `stdbool.h`
*   `stdint.h`
*   `stdlib.h`
*   `string.h`

### vendors/tree-sitter-dart/src/tree_sitter/parser.h
*   `stdbool.h`
*   `stdint.h`
*   `stdlib.h`

### vendors/tree-sitter-dart/test/highlight/flutter.dart
*   `package:flutter/material.dart`

### vendors/tree-sitter-dart/test/highlight/keywords.dart
*   `foo.dart`

### vendors/tree-sitter-dart/test/tags/flutter.dart
*   `package:flutter/material.dart`

### vendors/tree-sitter-dart/test/tags/keywords.dart
*   `foo.dart`

### vendors/tree-sitter-dart/tester/pubspec.yaml
*   `glob`
*   `path`
*   `dcli (dev)`

### vendors/tree-sitter-dart/tester/test.dart
*   `package:path/path.dart`
*   `dart:io`

### vendors/tree-sitter-dart/tree_sitter/pubspec.yaml
*   `dylib`
*   `args`
*   `ffi`
*   `freezed_annotation`
*   `path`
*   `json_annotation`
*   `lints (dev)`
*   `test (dev)`
*   `ffigen (dev)`
*   `freezed (dev)`
*   `json_serializable (dev)`
*   `build_runner (dev)`

### vendors/tree-sitter-dart/tree_sitter/bin/gen_grammar.dart
*   `dart:convert`
*   `package:freezed_annotation/freezed_annotation.dart`
*   `dart:io`
*   `package:args/args.dart`

### vendors/tree-sitter-dart/tree_sitter/example/tree_sitter.dart
*   `package:dylib/dylib.dart`
*   `package:tree_sitter/tree_sitter.dart`
*   `dart:io`

### vendors/tree-sitter-dart/tree_sitter/lib/tree_sitter.dart
*   `dart:convert`
*   `src/utils.dart`
*   `dart:typed_data`
*   `package:dylib/dylib.dart`
*   `dart:ffi`
*   `package:tree_sitter/tree_sitter.dart`
*   `src/parser_generated_bindings.dart`
*   `dart:io`
*   `package:ffi/ffi.dart`

### vendors/tree-sitter-dart/tree_sitter/lib/src/generated_bindings.dart
*   `dart:ffi`

### vendors/tree-sitter-dart/tree_sitter/lib/src/parser_generated_bindings.dart
*   `dart:ffi`

### vendors/tree-sitter-dart/tree_sitter/lib/src/utils.dart
*   `dart:ffi`
*   `dart:io`

### vendors/tree-sitter-dart/tree_sitter/test/tree_sitter_test.dart
*   `package:dylib/dylib.dart`
*   `package:test/test.dart`
*   `package:tree_sitter/tree_sitter.dart`
*   `dart:io`

## 3. Environment (开发环境)
*   **OS**: Windows (Detected)
*   **Python**: Detected via file extension

---
*Generated by Niki-docAI*
