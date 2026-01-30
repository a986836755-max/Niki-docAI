# Project Map
> @CONTEXT: Map | Project Structure
> 最后更新 (Last Updated): 2026-01-29 20:01:46

## @STRUCTURE
<!-- NIKI_MAP_START -->
*   **src/**
    *   **ndoc/**
        *   **atoms/**
            *   `_AI.md`
            *   `__init__.py` - *Atoms: File System Operations.*
            *   `ast.py` - *Atoms: AST Parsing (Tree-sitter Wrapper).*
            *   `deps.py` - *Atom: Dependency Parser.*
            *   `fs.py` - *Atoms: File System Traversal.*
            *   `io.py` - *Atoms: Input/Output Operations.*
            *   `queries.py`
            *   `scanner.py` - *Atoms: Content Scanner.*
        *   **flows/**
            *   `_AI.md`
            *   `__init__.py` - *Flows: Business Logic Pipelines.*
            *   `clean_flow.py` - *Flow: Clean / Reset.*
            *   `config_flow.py` - *Flow: Configuration Loading.*
            *   `context_flow.py` - *Flow: Recursive Context Generation.*
            *   `deps_flow.py` - *Flow: Dependency Graph Generation.*
            *   `doctor_flow.py` - *Flow: System Diagnostics.*
            *   `init_flow.py` - *Flow: Initialization.*
            *   `map_flow.py` - *Flow: Map Generation.*
            *   `stats_flow.py` - *Flow: Statistics.*
            *   `syntax_flow.py` - *Flow: Syntax Manual Sync.*
            *   `tech_flow.py` - *Flow: Tech Stack Snapshot Generation.*
            *   `todo_flow.py` - *Flow: Todo Aggregation.*
            *   `update_flow.py` - *Flow: Self-Update Flow.*
            *   `verify_flow.py` - *Flow: Verification.*
        *   **models/**
            *   `_AI.md`
            *   `__init__.py` - *Models: Data Definitions.*
            *   `config.py` - *Models: Configuration definitions.*
            *   `context.py` - *Models: Context Models.*
        *   `_AI.md`
        *   `__init__.py` - *Niki-docAI Source Root.*
        *   `daemon.py` - *Daemon: Live Context Watcher.*
        *   `entry.py` - *Entry Point: CLI Execution.*
    *   **niki_doc_ai.egg-info/**
        *   `PKG-INFO`
        *   `SOURCES.txt`
        *   `_AI.md`
        *   `dependency_links.txt`
        *   `entry_points.txt`
        *   `requires.txt`
        *   `top_level.txt`
    *   `_AI.md`
*   **tests/**
    *   **fixtures/**
        *   `_AI.md`
        *   `complex_api.py`
    *   **temp/**
    *   `_AI.md`
    *   `conftest.py`
    *   `test_ast.py`
    *   `test_scanner.py`
*   **tools/**
    *   `_AI.md`
    *   `doxygen.exe`
*   **vendors/**
    *   **tree-sitter-dart/**
        *   **assets/**
            *   `_AI.md`
            *   `playground.js`
            *   `tree-sitter.js`
        *   **bindings/**
            *   **c/**
                *   `_AI.md`
                *   `tree-sitter-dart.h`
                *   `tree-sitter-dart.pc.in`
            *   **go/**
                *   `_AI.md`
                *   `binding.go`
                *   `binding_test.go`
            *   **node/**
                *   `_AI.md`
                *   `binding.cc`
                *   `index.d.ts`
                *   `index.js`
            *   **python/**
                *   **tree_sitter_dart/**
                    *   `_AI.md`
                    *   `__init__.py`
                    *   `__init__.pyi`
                    *   `binding.c`
                    *   `py.typed`
                *   **tree_sitter_dart.egg-info/**
                    *   `PKG-INFO`
                    *   `SOURCES.txt`
                    *   `_AI.md`
                    *   `dependency_links.txt`
                    *   `not-zip-safe`
                    *   `requires.txt`
                    *   `top_level.txt`
            *   **rust/**
                *   `_AI.md`
                *   `build.rs`
                *   `lib.rs`
            *   **swift/**
                *   **TreeSitterDart/**
                    *   `_AI.md`
                    *   `dart.h`
        *   **queries/**
            *   `_AI.md`
            *   `highlights.scm`
            *   `tags.scm`
            *   `test.scm`
        *   **src/**
            *   **tree_sitter/**
                *   `_AI.md`
                *   `alloc.h`
                *   `array.h`
                *   `parser.h`
            *   `_AI.md`
            *   `grammar.json`
            *   `node-types.json`
            *   `parser.c`
            *   `scanner.c`
        *   **test/**
            *   **corpus/**
                *   `_AI.md`
                *   `annotations.txt`
                *   `big_tests.txt`
                *   `class_modifiers.txt`
                *   `comments.txt`
                *   `dart.txt`
                *   `declarations.txt`
                *   `enhanced_enums.txt`
                *   `errors.txt`
                *   `expressions.txt`
                *   `flutter.txt`
                *   `literals.txt`
                *   `more_expressions.txt`
                *   `patterns.txt`
                *   `records.txt`
                *   `types.txt`
            *   **highlight/**
                *   `_AI.md`
                *   `crash2.dart`
                *   `flutter.dart`
                *   `functions.dart`
                *   `keywords.dart`
                *   `types.dart`
            *   **tags/**
                *   `_AI.md`
                *   `flutter.dart`
                *   `functions.dart`
                *   `keywords.dart`
                *   `types.dart`
        *   **tester/**
            *   `_AI.md`
            *   `pubspec.yaml`
            *   `test.dart`
        *   **tree_sitter/**
            *   **bin/**
                *   `_AI.md`
                *   `gen_grammar.dart`
                *   `gen_grammar.freezed.dart`
                *   `gen_grammar.g.dart`
            *   **example/**
                *   `_AI.md`
                *   `tree_sitter.dart`
            *   **lib/**
                *   **src/**
                    *   `_AI.md`
                    *   `generated_bindings.dart`
                    *   `parser_generated_bindings.dart`
                    *   `utils.dart`
                *   `_AI.md`
                *   `tree_sitter.dart`
            *   **test/**
                *   `_AI.md`
                *   `tree_sitter_test.dart`
            *   **tree-sitter/**
            *   `CHANGELOG.md`
            *   `LICENSE`
            *   `Makefile`
            *   `README.md`
            *   `_AI.md`
            *   `analysis_options.yaml`
            *   `api_config.yaml`
            *   `parser_config.yaml`
            *   `pubspec.yaml`
        *   `Cargo.lock`
        *   `Cargo.toml`
        *   `Dart.g`
        *   `LICENSE`
        *   `Makefile`
        *   `Package.swift`
        *   `README.md`
        *   `_AI.md`
        *   `binding.gyp`
        *   `go.mod`
        *   `grammar.js`
        *   `package.json`
        *   `pubspec.yaml`
        *   `pyproject.toml`
        *   `setup.py`
        *   `test_all.sh`
        *   `testitem.html`
        *   `tree-sitter-dart.wasm`
        *   `tree-sitter.json`
*   `README.md`
*   `_AI.md`
*   `_ARCH.md`
*   `_DEPS.md`
*   `_MAP.md`
*   `_MEMORY.md`
*   `_NEXT.md`
*   `_RULES.md`
*   `_STATS.md`
*   `_SYNTAX.md`
*   `_TECH.md`
*   `requirements.txt`
*   `setup.py`
<!-- NIKI_MAP_END -->