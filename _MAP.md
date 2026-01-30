# Project Map
> @CONTEXT: Map | Project Structure
> 最后更新 (Last Updated): 2026-01-30 19:04:13

## @STRUCTURE
<!-- NIKI_MAP_START -->
*   **src/**
    *   **ndoc/**
        *   **atoms/**
            *   [`_AI.md`](src/ndoc/atoms/_AI.md#L1)
            *   [`__init__.py`](src/ndoc/atoms/__init__.py#L1) - *Atoms: File System Operations.*
            *   [`ast.py`](src/ndoc/atoms/ast.py#L1) - *Atoms: AST Parsing (Tree-sitter Wrapper).*
            *   [`deps.py`](src/ndoc/atoms/deps.py#L1) - *Atom: Dependency Parser.*
            *   [`fs.py`](src/ndoc/atoms/fs.py#L1) - *Atoms: File System Traversal.*
            *   [`io.py`](src/ndoc/atoms/io.py#L1) - *Atoms: Input/Output Operations.*
            *   [`queries.py`](src/ndoc/atoms/queries.py#L1)
            *   [`scanner.py`](src/ndoc/atoms/scanner.py#L1) - *Atoms: Content Scanner.*
        *   **flows/**
            *   [`_AI.md`](src/ndoc/flows/_AI.md#L1)
            *   [`__init__.py`](src/ndoc/flows/__init__.py#L1) - *Flows: Business Logic Pipelines.*
            *   [`clean_flow.py`](src/ndoc/flows/clean_flow.py#L1) - *Flow: Clean / Reset.*
            *   [`config_flow.py`](src/ndoc/flows/config_flow.py#L1) - *Flow: Configuration Loading.*
            *   [`context_flow.py`](src/ndoc/flows/context_flow.py#L1) - *Flow: Recursive Context Generation.*
            *   [`deps_flow.py`](src/ndoc/flows/deps_flow.py#L1) - *Flow: Dependency Graph Generation.*
            *   [`doctor_flow.py`](src/ndoc/flows/doctor_flow.py#L1) - *Flow: System Diagnostics.*
            *   [`init_flow.py`](src/ndoc/flows/init_flow.py#L1) - *Flow: Initialization.*
            *   [`map_flow.py`](src/ndoc/flows/map_flow.py#L1) - *Flow: Map Generation.*
            *   [`stats_flow.py`](src/ndoc/flows/stats_flow.py#L1) - *Flow: Statistics.*
            *   [`syntax_flow.py`](src/ndoc/flows/syntax_flow.py#L1) - *Flow: Syntax Manual Sync.*
            *   [`tech_flow.py`](src/ndoc/flows/tech_flow.py#L1) - *Flow: Tech Stack Snapshot Generation.*
            *   [`todo_flow.py`](src/ndoc/flows/todo_flow.py#L1) - *Flow: Todo Aggregation.*
            *   [`update_flow.py`](src/ndoc/flows/update_flow.py#L1) - *Flow: Self-Update Flow.*
            *   [`verify_flow.py`](src/ndoc/flows/verify_flow.py#L1) - *Flow: Verification.*
        *   **models/**
            *   [`_AI.md`](src/ndoc/models/_AI.md#L1)
            *   [`__init__.py`](src/ndoc/models/__init__.py#L1) - *Models: Data Definitions.*
            *   [`config.py`](src/ndoc/models/config.py#L1) - *Models: Configuration definitions.*
            *   [`context.py`](src/ndoc/models/context.py#L1) - *Models: Context Models.*
        *   [`_AI.md`](src/ndoc/_AI.md#L1)
        *   [`__init__.py`](src/ndoc/__init__.py#L1) - *Niki-docAI Source Root.*
        *   [`daemon.py`](src/ndoc/daemon.py#L1) - *Daemon: Live Context Watcher.*
        *   [`entry.py`](src/ndoc/entry.py#L1) - *Entry Point: CLI Execution.*
    *   **niki_doc_ai.egg-info/**
        *   [`PKG-INFO`](src/niki_doc_ai.egg-info/PKG-INFO#L1)
        *   [`SOURCES.txt`](src/niki_doc_ai.egg-info/SOURCES.txt#L1)
        *   [`_AI.md`](src/niki_doc_ai.egg-info/_AI.md#L1)
        *   [`dependency_links.txt`](src/niki_doc_ai.egg-info/dependency_links.txt#L1)
        *   [`entry_points.txt`](src/niki_doc_ai.egg-info/entry_points.txt#L1)
        *   [`requires.txt`](src/niki_doc_ai.egg-info/requires.txt#L1)
        *   [`top_level.txt`](src/niki_doc_ai.egg-info/top_level.txt#L1)
    *   [`_AI.md`](src/_AI.md#L1)
*   **tests/**
    *   **fixtures/**
        *   [`_AI.md`](tests/fixtures/_AI.md#L1)
        *   [`complex_api.py`](tests/fixtures/complex_api.py#L1)
    *   **temp/**
        *   [`_AI.md`](tests/temp/_AI.md#L1)
    *   [`_AI.md`](tests/_AI.md#L1)
    *   [`conftest.py`](tests/conftest.py#L1)
    *   [`test_ast.py`](tests/test_ast.py#L1)
    *   [`test_scanner.py`](tests/test_scanner.py#L1)
*   **tools/**
    *   [`_AI.md`](tools/_AI.md#L1)
    *   [`doxygen.exe`](tools/doxygen.exe#L1)
*   **vendors/**
    *   **tree-sitter-dart/**
        *   **assets/**
            *   [`_AI.md`](vendors/tree-sitter-dart/assets/_AI.md#L1)
            *   [`playground.js`](vendors/tree-sitter-dart/assets/playground.js#L1)
            *   [`tree-sitter.js`](vendors/tree-sitter-dart/assets/tree-sitter.js#L1)
        *   **bindings/**
            *   **c/**
                *   [`_AI.md`](vendors/tree-sitter-dart/bindings/c/_AI.md#L1)
                *   [`tree-sitter-dart.h`](vendors/tree-sitter-dart/bindings/c/tree-sitter-dart.h#L1)
                *   [`tree-sitter-dart.pc.in`](vendors/tree-sitter-dart/bindings/c/tree-sitter-dart.pc.in#L1)
            *   **go/**
                *   [`_AI.md`](vendors/tree-sitter-dart/bindings/go/_AI.md#L1)
                *   [`binding.go`](vendors/tree-sitter-dart/bindings/go/binding.go#L1)
                *   [`binding_test.go`](vendors/tree-sitter-dart/bindings/go/binding_test.go#L1)
            *   **node/**
                *   [`_AI.md`](vendors/tree-sitter-dart/bindings/node/_AI.md#L1)
                *   [`binding.cc`](vendors/tree-sitter-dart/bindings/node/binding.cc#L1)
                *   [`index.d.ts`](vendors/tree-sitter-dart/bindings/node/index.d.ts#L1)
                *   [`index.js`](vendors/tree-sitter-dart/bindings/node/index.js#L1)
            *   **python/**
                *   **tree_sitter_dart/**
                    *   [`_AI.md`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/_AI.md#L1)
                    *   [`__init__.py`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/__init__.py#L1)
                    *   [`__init__.pyi`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/__init__.pyi#L1)
                    *   [`binding.c`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/binding.c#L1)
                    *   [`py.typed`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/py.typed#L1)
                *   **tree_sitter_dart.egg-info/**
                    *   [`PKG-INFO`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart.egg-info/PKG-INFO#L1)
                    *   [`SOURCES.txt`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart.egg-info/SOURCES.txt#L1)
                    *   [`_AI.md`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart.egg-info/_AI.md#L1)
                    *   [`dependency_links.txt`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart.egg-info/dependency_links.txt#L1)
                    *   [`not-zip-safe`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart.egg-info/not-zip-safe#L1)
                    *   [`requires.txt`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart.egg-info/requires.txt#L1)
                    *   [`top_level.txt`](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart.egg-info/top_level.txt#L1)
                *   [`_AI.md`](vendors/tree-sitter-dart/bindings/python/_AI.md#L1)
            *   **rust/**
                *   [`_AI.md`](vendors/tree-sitter-dart/bindings/rust/_AI.md#L1)
                *   [`build.rs`](vendors/tree-sitter-dart/bindings/rust/build.rs#L1)
                *   [`lib.rs`](vendors/tree-sitter-dart/bindings/rust/lib.rs#L1)
            *   **swift/**
                *   **TreeSitterDart/**
                    *   [`_AI.md`](vendors/tree-sitter-dart/bindings/swift/TreeSitterDart/_AI.md#L1)
                    *   [`dart.h`](vendors/tree-sitter-dart/bindings/swift/TreeSitterDart/dart.h#L1)
                *   [`_AI.md`](vendors/tree-sitter-dart/bindings/swift/_AI.md#L1)
            *   [`_AI.md`](vendors/tree-sitter-dart/bindings/_AI.md#L1)
        *   **queries/**
            *   [`_AI.md`](vendors/tree-sitter-dart/queries/_AI.md#L1)
            *   [`highlights.scm`](vendors/tree-sitter-dart/queries/highlights.scm#L1)
            *   [`tags.scm`](vendors/tree-sitter-dart/queries/tags.scm#L1)
            *   [`test.scm`](vendors/tree-sitter-dart/queries/test.scm#L1)
        *   **src/**
            *   **tree_sitter/**
                *   [`_AI.md`](vendors/tree-sitter-dart/src/tree_sitter/_AI.md#L1)
                *   [`alloc.h`](vendors/tree-sitter-dart/src/tree_sitter/alloc.h#L1)
                *   [`array.h`](vendors/tree-sitter-dart/src/tree_sitter/array.h#L1)
                *   [`parser.h`](vendors/tree-sitter-dart/src/tree_sitter/parser.h#L1)
            *   [`_AI.md`](vendors/tree-sitter-dart/src/_AI.md#L1)
            *   [`grammar.json`](vendors/tree-sitter-dart/src/grammar.json#L1)
            *   [`node-types.json`](vendors/tree-sitter-dart/src/node-types.json#L1)
            *   [`parser.c`](vendors/tree-sitter-dart/src/parser.c#L1)
            *   [`scanner.c`](vendors/tree-sitter-dart/src/scanner.c#L1)
        *   **test/**
            *   **corpus/**
                *   [`_AI.md`](vendors/tree-sitter-dart/test/corpus/_AI.md#L1)
                *   [`annotations.txt`](vendors/tree-sitter-dart/test/corpus/annotations.txt#L1)
                *   [`big_tests.txt`](vendors/tree-sitter-dart/test/corpus/big_tests.txt#L1)
                *   [`class_modifiers.txt`](vendors/tree-sitter-dart/test/corpus/class_modifiers.txt#L1)
                *   [`comments.txt`](vendors/tree-sitter-dart/test/corpus/comments.txt#L1)
                *   [`dart.txt`](vendors/tree-sitter-dart/test/corpus/dart.txt#L1)
                *   [`declarations.txt`](vendors/tree-sitter-dart/test/corpus/declarations.txt#L1)
                *   [`enhanced_enums.txt`](vendors/tree-sitter-dart/test/corpus/enhanced_enums.txt#L1)
                *   [`errors.txt`](vendors/tree-sitter-dart/test/corpus/errors.txt#L1)
                *   [`expressions.txt`](vendors/tree-sitter-dart/test/corpus/expressions.txt#L1)
                *   [`flutter.txt`](vendors/tree-sitter-dart/test/corpus/flutter.txt#L1)
                *   [`literals.txt`](vendors/tree-sitter-dart/test/corpus/literals.txt#L1)
                *   [`more_expressions.txt`](vendors/tree-sitter-dart/test/corpus/more_expressions.txt#L1)
                *   [`patterns.txt`](vendors/tree-sitter-dart/test/corpus/patterns.txt#L1)
                *   [`records.txt`](vendors/tree-sitter-dart/test/corpus/records.txt#L1)
                *   [`types.txt`](vendors/tree-sitter-dart/test/corpus/types.txt#L1)
            *   **highlight/**
                *   [`_AI.md`](vendors/tree-sitter-dart/test/highlight/_AI.md#L1)
                *   [`crash2.dart`](vendors/tree-sitter-dart/test/highlight/crash2.dart#L1)
                *   [`flutter.dart`](vendors/tree-sitter-dart/test/highlight/flutter.dart#L1)
                *   [`functions.dart`](vendors/tree-sitter-dart/test/highlight/functions.dart#L1)
                *   [`keywords.dart`](vendors/tree-sitter-dart/test/highlight/keywords.dart#L1)
                *   [`types.dart`](vendors/tree-sitter-dart/test/highlight/types.dart#L1)
            *   **tags/**
                *   [`_AI.md`](vendors/tree-sitter-dart/test/tags/_AI.md#L1)
                *   [`flutter.dart`](vendors/tree-sitter-dart/test/tags/flutter.dart#L1)
                *   [`functions.dart`](vendors/tree-sitter-dart/test/tags/functions.dart#L1)
                *   [`keywords.dart`](vendors/tree-sitter-dart/test/tags/keywords.dart#L1)
                *   [`types.dart`](vendors/tree-sitter-dart/test/tags/types.dart#L1)
            *   [`_AI.md`](vendors/tree-sitter-dart/test/_AI.md#L1)
        *   **tester/**
            *   [`_AI.md`](vendors/tree-sitter-dart/tester/_AI.md#L1)
            *   [`pubspec.yaml`](vendors/tree-sitter-dart/tester/pubspec.yaml#L1)
            *   [`test.dart`](vendors/tree-sitter-dart/tester/test.dart#L1)
        *   **tree_sitter/**
            *   **bin/**
                *   [`_AI.md`](vendors/tree-sitter-dart/tree_sitter/bin/_AI.md#L1)
                *   [`gen_grammar.dart`](vendors/tree-sitter-dart/tree_sitter/bin/gen_grammar.dart#L1)
                *   [`gen_grammar.freezed.dart`](vendors/tree-sitter-dart/tree_sitter/bin/gen_grammar.freezed.dart#L1)
                *   [`gen_grammar.g.dart`](vendors/tree-sitter-dart/tree_sitter/bin/gen_grammar.g.dart#L1)
            *   **example/**
                *   [`_AI.md`](vendors/tree-sitter-dart/tree_sitter/example/_AI.md#L1)
                *   [`tree_sitter.dart`](vendors/tree-sitter-dart/tree_sitter/example/tree_sitter.dart#L1)
            *   **lib/**
                *   **src/**
                    *   [`_AI.md`](vendors/tree-sitter-dart/tree_sitter/lib/src/_AI.md#L1)
                    *   [`generated_bindings.dart`](vendors/tree-sitter-dart/tree_sitter/lib/src/generated_bindings.dart#L1)
                    *   [`parser_generated_bindings.dart`](vendors/tree-sitter-dart/tree_sitter/lib/src/parser_generated_bindings.dart#L1)
                    *   [`utils.dart`](vendors/tree-sitter-dart/tree_sitter/lib/src/utils.dart#L1)
                *   [`_AI.md`](vendors/tree-sitter-dart/tree_sitter/lib/_AI.md#L1)
                *   [`tree_sitter.dart`](vendors/tree-sitter-dart/tree_sitter/lib/tree_sitter.dart#L1)
            *   **test/**
                *   [`_AI.md`](vendors/tree-sitter-dart/tree_sitter/test/_AI.md#L1)
                *   [`tree_sitter_test.dart`](vendors/tree-sitter-dart/tree_sitter/test/tree_sitter_test.dart#L1)
            *   **tree-sitter/**
            *   [`CHANGELOG.md`](vendors/tree-sitter-dart/tree_sitter/CHANGELOG.md#L1)
            *   [`LICENSE`](vendors/tree-sitter-dart/tree_sitter/LICENSE#L1)
            *   [`Makefile`](vendors/tree-sitter-dart/tree_sitter/Makefile#L1)
            *   [`README.md`](vendors/tree-sitter-dart/tree_sitter/README.md#L1)
            *   [`_AI.md`](vendors/tree-sitter-dart/tree_sitter/_AI.md#L1)
            *   [`analysis_options.yaml`](vendors/tree-sitter-dart/tree_sitter/analysis_options.yaml#L1)
            *   [`api_config.yaml`](vendors/tree-sitter-dart/tree_sitter/api_config.yaml#L1)
            *   [`parser_config.yaml`](vendors/tree-sitter-dart/tree_sitter/parser_config.yaml#L1)
            *   [`pubspec.yaml`](vendors/tree-sitter-dart/tree_sitter/pubspec.yaml#L1)
        *   [`Cargo.lock`](vendors/tree-sitter-dart/Cargo.lock#L1)
        *   [`Cargo.toml`](vendors/tree-sitter-dart/Cargo.toml#L1)
        *   [`Dart.g`](vendors/tree-sitter-dart/Dart.g#L1)
        *   [`LICENSE`](vendors/tree-sitter-dart/LICENSE#L1)
        *   [`Makefile`](vendors/tree-sitter-dart/Makefile#L1)
        *   [`Package.swift`](vendors/tree-sitter-dart/Package.swift#L1)
        *   [`README.md`](vendors/tree-sitter-dart/README.md#L1)
        *   [`_AI.md`](vendors/tree-sitter-dart/_AI.md#L1)
        *   [`binding.gyp`](vendors/tree-sitter-dart/binding.gyp#L1)
        *   [`go.mod`](vendors/tree-sitter-dart/go.mod#L1)
        *   [`grammar.js`](vendors/tree-sitter-dart/grammar.js#L1)
        *   [`package.json`](vendors/tree-sitter-dart/package.json#L1)
        *   [`pubspec.yaml`](vendors/tree-sitter-dart/pubspec.yaml#L1)
        *   [`pyproject.toml`](vendors/tree-sitter-dart/pyproject.toml#L1)
        *   [`setup.py`](vendors/tree-sitter-dart/setup.py#L1)
        *   [`test_all.sh`](vendors/tree-sitter-dart/test_all.sh#L1)
        *   [`testitem.html`](vendors/tree-sitter-dart/testitem.html#L1)
        *   [`tree-sitter-dart.wasm`](vendors/tree-sitter-dart/tree-sitter-dart.wasm#L1)
        *   [`tree-sitter.json`](vendors/tree-sitter-dart/tree-sitter.json#L1)
    *   [`_AI.md`](vendors/_AI.md#L1)
*   [`README.md`](README.md#L1)
*   [`_AI.md`](_AI.md#L1)
*   [`_ARCH.md`](_ARCH.md#L1)
*   [`_DEPS.md`](_DEPS.md#L1)
*   [`_MAP.md`](_MAP.md#L1)
*   [`_MEMORY.md`](_MEMORY.md#L1)
*   [`_NEXT.md`](_NEXT.md#L1)
*   [`_RULES.md`](_RULES.md#L1)
*   [`_STATS.md`](_STATS.md#L1)
*   [`_SYNTAX.md`](_SYNTAX.md#L1)
*   [`_TECH.md`](_TECH.md#L1)
*   [`requirements.txt`](requirements.txt#L1)
*   [`setup.py`](setup.py#L1)
<!-- NIKI_MAP_END -->