# Tech Stack Snapshot
> @CONTEXT: Global | _TECH.md | @TAGS: @TECH @DEPS
> 最后更新 (Last Updated): 2026-01-30 19:25:20

## 1. Languages (语言分布)
*   **Markdown**: `███████░░░░░░░░░░░░░` 38.3%
*   **Python**: `█████░░░░░░░░░░░░░░░` 25.6%
*   **Dart**: `██░░░░░░░░░░░░░░░░░░` 14.3%
*   **YAML**: `░░░░░░░░░░░░░░░░░░░░` 4.5%
*   **C/C++ Header**: `░░░░░░░░░░░░░░░░░░░░` 3.8%
*   **JavaScript**: `░░░░░░░░░░░░░░░░░░░░` 3.0%
*   **JSON**: `░░░░░░░░░░░░░░░░░░░░` 3.0%
*   **C**: `░░░░░░░░░░░░░░░░░░░░` 2.3%
*   **Go**: `░░░░░░░░░░░░░░░░░░░░` 1.5%
*   **Rust**: `░░░░░░░░░░░░░░░░░░░░` 1.5%
*   **HTML**: `░░░░░░░░░░░░░░░░░░░░` 0.8%
*   **Shell**: `░░░░░░░░░░░░░░░░░░░░` 0.8%
*   **TypeScript**: `░░░░░░░░░░░░░░░░░░░░` 0.8%

## 2. Dependencies (依赖库)
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

### setup.py
*   `setuptools`

### src/ndoc/daemon.py
*   `ndoc.flows`
*   `ndoc.models.config`
*   `pathlib`
*   `threading`
*   `time`
*   `typing`
*   `watchdog.events`
*   `watchdog.observers`

### src/ndoc/entry.py
*   `argparse`
*   `ndoc.atoms`
*   `ndoc.daemon`
*   `ndoc.flows`
*   `ndoc.models.config`
*   `pathlib`
*   `sys`

### src/ndoc/atoms/ast.py
*   `dataclasses`
*   `models.context`
*   `pathlib`
*   `tree_sitter`
*   `tree_sitter_c_sharp`
*   `tree_sitter_cpp`
*   `tree_sitter_dart`
*   `tree_sitter_go`
*   `tree_sitter_java`
*   `tree_sitter_javascript`
*   `tree_sitter_python`
*   `tree_sitter_rust`
*   `tree_sitter_typescript`
*   `typing`

### src/ndoc/atoms/deps.py
*   `ast`
*   `configparser`
*   `json`
*   `pathlib`
*   `re`
*   `typing`

### src/ndoc/atoms/fs.py
*   `dataclasses`
*   `os`
*   `pathlib`
*   `re`
*   `typing`

### src/ndoc/atoms/io.py
*   `datetime`
*   `difflib`
*   `os`
*   `pathlib`
*   `re`
*   `typing`

### src/ndoc/atoms/scanner.py
*   `atoms.ast`
*   `dataclasses`
*   `models.context`
*   `pathlib`
*   `re`
*   `typing`

### src/ndoc/flows/clean_flow.py
*   `ndoc.models.config`
*   `os`
*   `pathlib`
*   `typing`

### src/ndoc/flows/config_flow.py
*   `ndoc.atoms`
*   `ndoc.models.config`
*   `pathlib`
*   `re`
*   `typing`

### src/ndoc/flows/context_flow.py
*   `atoms`
*   `dataclasses`
*   `datetime`
*   `models.config`
*   `models.context`
*   `pathlib`
*   `re`
*   `typing`

### src/ndoc/flows/deps_flow.py
*   `atoms`
*   `collections`
*   `datetime`
*   `models.config`
*   `pathlib`
*   `typing`

### src/ndoc/flows/doctor_flow.py
*   `importlib`
*   `ndoc.models.config`
*   `pathlib`
*   `platform`
*   `shutil`
*   `sys`
*   `tree_sitter`
*   `tree_sitter_python`
*   `typing`

### src/ndoc/flows/init_flow.py
*   `ndoc.flows`
*   `ndoc.models.config`

### src/ndoc/flows/map_flow.py
*   `atoms`
*   `dataclasses`
*   `datetime`
*   `models.config`
*   `pathlib`
*   `typing`

### src/ndoc/flows/stats_flow.py
*   `datetime`
*   `ndoc.atoms`
*   `ndoc.models.config`
*   `os`
*   `pathlib`
*   `re`
*   `time`

### src/ndoc/flows/syntax_flow.py
*   `ndoc.atoms`
*   `ndoc.models.config`
*   `pathlib`

### src/ndoc/flows/tech_flow.py
*   `datetime`
*   `ndoc.atoms`
*   `ndoc.models.config`
*   `pathlib`

### src/ndoc/flows/todo_flow.py
*   `atoms`
*   `dataclasses`
*   `datetime`
*   `models.config`
*   `pathlib`
*   `typing`

### src/ndoc/flows/update_flow.py
*   `pathlib`
*   `subprocess`
*   `sys`
*   `typing`

### src/ndoc/flows/verify_flow.py
*   `ndoc.models.config`
*   `sys`

### src/ndoc/models/config.py
*   `dataclasses`
*   `pathlib`
*   `typing`

### src/ndoc/models/context.py
*   `dataclasses`
*   `pathlib`
*   `typing`

### tests/conftest.py
*   `pathlib`
*   `sys`

### tests/test_ast.py
*   `ndoc.atoms.ast`
*   `ndoc.atoms.io`
*   `ndoc.models.context`
*   `pathlib`
*   `pytest`

### tests/test_scanner.py
*   `ndoc.atoms.scanner`
*   `pathlib`
*   `pytest`

### tests/fixtures/complex_api.py
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
*   `os.path`
*   `platform`
*   `setuptools`
*   `setuptools.command.build`
*   `wheel.bdist_wheel`

### vendors/tree-sitter-dart/bindings/node/binding.cc
*   `napi.h`

### vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/binding.c
*   `Python.h`

### vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/__init__.py
*   `_binding`

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
*   `package:freezed_annotation/freezed_annotation.dart`
*   `dart:io`
*   `dart:convert`
*   `package:args/args.dart`

### vendors/tree-sitter-dart/tree_sitter/example/tree_sitter.dart
*   `package:dylib/dylib.dart`
*   `package:tree_sitter/tree_sitter.dart`
*   `dart:io`

### vendors/tree-sitter-dart/tree_sitter/lib/tree_sitter.dart
*   `dart:typed_data`
*   `package:dylib/dylib.dart`
*   `package:ffi/ffi.dart`
*   `src/utils.dart`
*   `dart:io`
*   `dart:ffi`
*   `src/parser_generated_bindings.dart`
*   `package:tree_sitter/tree_sitter.dart`
*   `dart:convert`

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
*   `dart:io`
*   `package:tree_sitter/tree_sitter.dart`

## 3. Environment (开发环境)
*   **OS**: Windows (Detected)
*   **Python**: Detected via file extension

---
*Generated by Niki-docAI*
