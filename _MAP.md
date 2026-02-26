# Project Map
> @CONTEXT: Map | Project Structure
> 最后更新 (Last Updated): 2026-02-26 20:34:28

## @STRUCTURE
<!-- NIKI_MAP_START -->
*   **build_spec/**
    *   [`_AI.md`](build_spec/_AI.md#L1)
    *   [`ndoc.spec`](build_spec/ndoc.spec#L1)
*   **editors/**
    *   **vscode/**
        *   **out/**
            *   [`_AI.md`](editors/vscode/out/_AI.md#L1)
            *   [`extension.js`](editors/vscode/out/extension.js#L1)
            *   [`extension.js.map`](editors/vscode/out/extension.js.map#L1)
        *   **src/**
            *   [`_AI.md`](editors/vscode/src/_AI.md#L1) - *Context: src*
            *   [`extension.ts`](editors/vscode/src/extension.ts#L1)
        *   [`LICENSE.md`](editors/vscode/LICENSE.md#L1)
        *   [`README.md`](editors/vscode/README.md#L1) - *Niki-docAI VS Code Extension*
        *   [`_AI.md`](editors/vscode/_AI.md#L1) - *Context: vscode*
        *   [`nk-doc-ai-vscode-0.1.0.vsix`](editors/vscode/nk-doc-ai-vscode-0.1.0.vsix#L1)
        *   [`nk-doc-ai-vscode-0.1.1.vsix`](editors/vscode/nk-doc-ai-vscode-0.1.1.vsix#L1)
        *   [`package-lock.json`](editors/vscode/package-lock.json#L1)
        *   [`package.json`](editors/vscode/package.json#L1)
        *   [`tsconfig.json`](editors/vscode/tsconfig.json#L1)
    *   [`_AI.md`](editors/_AI.md#L1) - *Context: editors*
*   **samples/**
    *   [`_AI.md`](samples/_AI.md#L1) - *Context: samples*
    *   [`sample_csharp.cs`](samples/sample_csharp.cs#L1)
*   **scripts/**
    *   [`_AI.md`](scripts/_AI.md#L1) - *Context: scripts*
    *   [`add_context_marker.py`](scripts/add_context_marker.py#L1)
*   **src/**
    *   **ndoc/**
        *   **brain/**
            *   [`_AI.md`](src/ndoc/brain/_AI.md#L1) - *Context: brain*
            *   [`__init__.py`](src/ndoc/brain/__init__.py#L1) - *Brain: Intelligence Layer.*
            *   [`checker.py`](src/ndoc/brain/checker.py#L1) - *Atoms: Constraint Checker (Prefrontal Cortex).*
            *   [`hippocampus.py`](src/ndoc/brain/hippocampus.py#L1) - *Atoms: Hippocampus (Observation Buffer & Heatmap).*
            *   [`index.py`](src/ndoc/brain/index.py#L1) - *Atoms: Semantic Index (Thalamus).*
            *   [`ingest.py`](src/ndoc/brain/ingest.py#L1) - *Brain: Context Ingestion.*
            *   [`vectordb.py`](src/ndoc/brain/vectordb.py#L1) - *Atoms: Vector Database (ChromaDB Wrapper).*
        *   **core/**
            *   [`_AI.md`](src/ndoc/core/_AI.md#L1) - *Context: core*
            *   [`__init__.py`](src/ndoc/core/__init__.py#L1) - *Core: Infrastructure Utilities.*
            *   [`bootstrap.py`](src/ndoc/core/bootstrap.py#L1)
            *   [`cache.py`](src/ndoc/core/cache.py#L1) - *Atoms: Cache Management.*
            *   [`capabilities.py`](src/ndoc/core/capabilities.py#L1) - *Atoms: Capability Manager.*
            *   [`cli.py`](src/ndoc/core/cli.py#L1) - *Core: CLI Command Registry.*
            *   [`errors.py`](src/ndoc/core/errors.py#L1) - *Custom exceptions for ndoc.*
            *   [`fs.py`](src/ndoc/core/fs.py#L1) - *Atoms: File System Traversal.*
            *   [`graph.py`](src/ndoc/core/graph.py#L1) - *Core: Graph Algorithms.*
            *   [`io.py`](src/ndoc/core/io.py#L1) - *Atoms: Input/Output Operations.*
            *   [`logger.py`](src/ndoc/core/logger.py#L1) - *Standardized logging for ndoc.*
            *   [`map_builder.py`](src/ndoc/core/map_builder.py#L1) - *Core: Map Builder.*
            *   [`native_builder.py`](src/ndoc/core/native_builder.py#L1) - *Native Builder: Handles local compilation of la...*
            *   [`stats.py`](src/ndoc/core/stats.py#L1) - *Core: Project Statistics.*
            *   [`task_manager.py`](src/ndoc/core/task_manager.py#L1) - *Core: Task Management.*
            *   [`templates.py`](src/ndoc/core/templates.py#L1)
            *   [`text_utils.py`](src/ndoc/core/text_utils.py#L1) - *Atoms: Text Processing Utilities.*
            *   [`transforms.py`](src/ndoc/core/transforms.py#L1) - *Core: Data Transforms.*
        *   **flows/**
            *   [`_AI.md`](src/ndoc/flows/_AI.md#L1) - *Context: flows*
            *   [`__init__.py`](src/ndoc/flows/__init__.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`adr_flow.py`](src/ndoc/flows/adr_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`arch_flow.py`](src/ndoc/flows/arch_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`archive_flow.py`](src/ndoc/flows/archive_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`capability_flow.py`](src/ndoc/flows/capability_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`check_flow.py`](src/ndoc/flows/check_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`clean_flow.py`](src/ndoc/flows/clean_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`config_flow.py`](src/ndoc/flows/config_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`context_flow.py`](src/ndoc/flows/context_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`data_flow.py`](src/ndoc/flows/data_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`deps_flow.py`](src/ndoc/flows/deps_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`doctor_flow.py`](src/ndoc/flows/doctor_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`impact_flow.py`](src/ndoc/flows/impact_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`init_flow.py`](src/ndoc/flows/init_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`inject_flow.py`](src/ndoc/flows/inject_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`lesson_flow.py`](src/ndoc/flows/lesson_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`map_flow.py`](src/ndoc/flows/map_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`mind_flow.py`](src/ndoc/flows/mind_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`prompt_flow.py`](src/ndoc/flows/prompt_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`quality_flow.py`](src/ndoc/flows/quality_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`search_flow.py`](src/ndoc/flows/search_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`status_flow.py`](src/ndoc/flows/status_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`syntax_flow.py`](src/ndoc/flows/syntax_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`update_flow.py`](src/ndoc/flows/update_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`verify_flow.py`](src/ndoc/flows/verify_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
        *   **interfaces/**
            *   [`_AI.md`](src/ndoc/interfaces/_AI.md#L1) - *Context: interfaces*
            *   [`__init__.py`](src/ndoc/interfaces/__init__.py#L1) - *Interfaces: Entry Points.*
            *   [`lsp.py`](src/ndoc/interfaces/lsp.py#L1) - *Atoms: Lightweight LSP-like features.*
        *   **models/**
            *   [`_AI.md`](src/ndoc/models/_AI.md#L1) - *Context: models*
            *   [`__init__.py`](src/ndoc/models/__init__.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`config.py`](src/ndoc/models/config.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`context.py`](src/ndoc/models/context.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`map.py`](src/ndoc/models/map.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`scan.py`](src/ndoc/models/scan.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`status.py`](src/ndoc/models/status.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`symbol.py`](src/ndoc/models/symbol.py#L1) - *<NIKI_AUTO_HEADER_START>*
        *   **parsing/**
            *   **ast/**
                *   [`_AI.md`](src/ndoc/parsing/ast/_AI.md#L1) - *Context: ast*
                *   [`__init__.py`](src/ndoc/parsing/ast/__init__.py#L1) - *Atoms: AST Parsing (Tree-sitter Wrapper).*
                *   [`base.py`](src/ndoc/parsing/ast/base.py#L1) - *Atoms: AST Parsing Base.*
                *   [`discovery.py`](src/ndoc/parsing/ast/discovery.py#L1) - *Atoms: AST Symbol Discovery.*
                *   [`skeleton.py`](src/ndoc/parsing/ast/skeleton.py#L1) - *Atoms: Semantic Skeleton Generator.*
                *   [`symbols.py`](src/ndoc/parsing/ast/symbols.py#L1) - *Atoms: AST Symbol Extraction.*
                *   [`utils.py`](src/ndoc/parsing/ast/utils.py#L1) - *Atoms: AST Parsing Utilities.*
            *   **deps/**
                *   [`_AI.md`](src/ndoc/parsing/deps/_AI.md#L1) - *Context: deps*
                *   [`__init__.py`](src/ndoc/parsing/deps/__init__.py#L1)
                *   [`api_extractor.py`](src/ndoc/parsing/deps/api_extractor.py#L1) - *Parsing: Dependency API Extractor.*
                *   [`builder.py`](src/ndoc/parsing/deps/builder.py#L1) - *Parsing: Dependency Graph Builder.*
                *   [`core.py`](src/ndoc/parsing/deps/core.py#L1) - *Core parsing logic for dependency manifests.*
                *   [`stats.py`](src/ndoc/parsing/deps/stats.py#L1) - *Language Statistics.*
                *   [`test_mapper.py`](src/ndoc/parsing/deps/test_mapper.py#L1) - *Deps: Test Usage Mapper.*
            *   **langs/**
                *   **bin/**
                    *   [`_AI.md`](src/ndoc/parsing/langs/bin/_AI.md#L1) - *Context: bin*
                    *   [`__init__.py`](src/ndoc/parsing/langs/bin/__init__.py#L1)
                    *   [`tree_sitter_dart.dll`](src/ndoc/parsing/langs/bin/tree_sitter_dart.dll#L1)
                *   [`_AI.md`](src/ndoc/parsing/langs/_AI.md#L1) - *Context: langs*
                *   [`__init__.py`](src/ndoc/parsing/langs/__init__.py#L1) - *Language Definition Protocol.*
                *   [`cpp.py`](src/ndoc/parsing/langs/cpp.py#L1)
                *   [`csharp.py`](src/ndoc/parsing/langs/csharp.py#L1)
                *   [`dart.py`](src/ndoc/parsing/langs/dart.py#L1)
                *   [`go.py`](src/ndoc/parsing/langs/go.py#L1)
                *   [`java.py`](src/ndoc/parsing/langs/java.py#L1)
                *   [`javascript.py`](src/ndoc/parsing/langs/javascript.py#L1)
                *   [`python.py`](src/ndoc/parsing/langs/python.py#L1)
                *   [`rust.py`](src/ndoc/parsing/langs/rust.py#L1)
                *   [`typescript.py`](src/ndoc/parsing/langs/typescript.py#L1)
            *   [`_AI.md`](src/ndoc/parsing/_AI.md#L1) - *Context: parsing*
            *   [`_LANGS.json`](src/ndoc/parsing/_LANGS.json#L1)
            *   [`__init__.py`](src/ndoc/parsing/__init__.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`extractors.py`](src/ndoc/parsing/extractors.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`rules.py`](src/ndoc/parsing/rules.py#L1) - *Parsing: Rule Extraction.*
            *   [`scanner.py`](src/ndoc/parsing/scanner.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`universal.py`](src/ndoc/parsing/universal.py#L1) - *<NIKI_AUTO_HEADER_START>*
        *   **templates/**
            *   **components/**
                *   [`doc_footer.tpl`](src/ndoc/templates/components/doc_footer.tpl#L1)
                *   [`doc_header.tpl`](src/ndoc/templates/components/doc_header.tpl#L1) - *{title}*
            *   [`ai.md.tpl`](src/ndoc/templates/ai.md.tpl#L1) - *Context: {name}*
            *   [`arch.md.tpl`](src/ndoc/templates/arch.md.tpl#L1) - *# 1. Technology Stack*
            *   [`deps.md.tpl`](src/ndoc/templates/deps.md.tpl#L1) - *# 1. Instability Metrics (Core Modules)*
            *   [`doctor_report.tpl`](src/ndoc/templates/doctor_report.tpl#L1)
            *   [`guide.md.tpl`](src/ndoc/templates/guide.md.tpl#L1) - *AI Context Guide (Niki-docAI)*
            *   [`header.py.tpl`](src/ndoc/templates/header.py.tpl#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`header_injection.tpl`](src/ndoc/templates/header_injection.tpl#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`impact.md.tpl`](src/ndoc/templates/impact.md.tpl#L1) - *# 1. Changed Files (Scope)*
            *   [`map.md.tpl`](src/ndoc/templates/map.md.tpl#L1) - *# @STRUCTURE*
            *   [`prompt.md.tpl`](src/ndoc/templates/prompt.md.tpl#L1) - *Niki-docAI Context Prompt*
            *   [`rules.md.tpl`](src/ndoc/templates/rules.md.tpl#L1) - *Project Rules*
            *   [`stats.md.tpl`](src/ndoc/templates/stats.md.tpl#L1) - *# 核心指标 (Core Metrics)*
            *   [`status.md.tpl`](src/ndoc/templates/status.md.tpl#L1) - *# 1. Pending Tasks (TODOs)*
            *   [`syntax.md.tpl`](src/ndoc/templates/syntax.md.tpl#L1) - *PROJECT SYNTAX*
        *   **views/**
            *   [`_AI.md`](src/ndoc/views/_AI.md#L1) - *Context: views*
            *   [`__init__.py`](src/ndoc/views/__init__.py#L1) - *Views: Output Rendering.*
            *   [`context.py`](src/ndoc/views/context.py#L1) - *View: Context Rendering.*
            *   [`header.py`](src/ndoc/views/header.py#L1) - *View: Header Injection.*
            *   [`map.py`](src/ndoc/views/map.py#L1) - *View: Map Rendering.*
            *   [`mermaid.py`](src/ndoc/views/mermaid.py#L1) - *View: Mermaid Graph Renderer.*
            *   [`reports.py`](src/ndoc/views/reports.py#L1) - *View: Report Tables.*
            *   [`status.py`](src/ndoc/views/status.py#L1) - *View: Status Reports.*
        *   [`_AI.md`](src/ndoc/_AI.md#L1) - *Context: ndoc*
        *   [`__init__.py`](src/ndoc/__init__.py#L1) - *Niki-docAI Source Root.*
        *   [`__main__.py`](src/ndoc/__main__.py#L1)
        *   [`api.py`](src/ndoc/api.py#L1) - *Public API: High-level interfaces for Agents an...*
        *   [`daemon.py`](src/ndoc/daemon.py#L1) - *Daemon: Live Context Watcher.*
        *   [`demo_violation.py`](src/ndoc/demo_violation.py#L1) - *@author Niki*
        *   [`entry.py`](src/ndoc/entry.py#L1) - *Entry Point: CLI Execution.*
        *   [`lsp_server.py`](src/ndoc/lsp_server.py#L1) - *LSP Server implementation using pygls.*
    *   **niki_doc_ai.egg-info/**
        *   [`PKG-INFO`](src/niki_doc_ai.egg-info/PKG-INFO#L1)
        *   [`SOURCES.txt`](src/niki_doc_ai.egg-info/SOURCES.txt#L1)
        *   [`_AI.md`](src/niki_doc_ai.egg-info/_AI.md#L1)
        *   [`dependency_links.txt`](src/niki_doc_ai.egg-info/dependency_links.txt#L1)
        *   [`entry_points.txt`](src/niki_doc_ai.egg-info/entry_points.txt#L1)
        *   [`requires.txt`](src/niki_doc_ai.egg-info/requires.txt#L1)
        *   [`top_level.txt`](src/niki_doc_ai.egg-info/top_level.txt#L1)
    *   [`_AI.md`](src/_AI.md#L1) - *Context: src*
*   **test_vectordb_root/**
*   **tests/**
    *   **fixtures/**
        *   [`_AI.md`](tests/fixtures/_AI.md#L1) - *Context: fixtures*
        *   [`complex_api.py`](tests/fixtures/complex_api.py#L1)
    *   **temp/**
    *   [`_AI.md`](tests/_AI.md#L1) - *Context: tests*
    *   [`benchmark_e2e.py`](tests/benchmark_e2e.py#L1)
    *   [`conftest.py`](tests/conftest.py#L1)
    *   [`test_ast.py`](tests/test_ast.py#L1)
    *   [`test_capabilities.py`](tests/test_capabilities.py#L1)
    *   [`test_capability_flow.py`](tests/test_capability_flow.py#L1)
    *   [`test_csharp_api.py`](tests/test_csharp_api.py#L1)
    *   [`test_lsp_server.py`](tests/test_lsp_server.py#L1) - *LSP Server Test Client (Refined)*
    *   [`test_scanner.py`](tests/test_scanner.py#L1)
*   **tools/**
    *   **packaging/**
        *   [`README.md`](tools/packaging/README.md#L1) - *Self-Contained Release*
        *   [`_AI.md`](tools/packaging/_AI.md#L1) - *Context: packaging*
        *   [`build.ps1`](tools/packaging/build.ps1#L1)
        *   [`build.sh`](tools/packaging/build.sh#L1)
        *   [`ndoc_entry.py`](tools/packaging/ndoc_entry.py#L1)
        *   [`requirements-packaging.txt`](tools/packaging/requirements-packaging.txt#L1)
        *   [`run_pyinstaller.py`](tools/packaging/run_pyinstaller.py#L1)
    *   [`_AI.md`](tools/_AI.md#L1) - *Context: tools*
*   [`MANIFEST.in`](MANIFEST.in#L1)
*   [`README.md`](README.md#L1) - *Niki-docAI 2.0 (Rebirth)*
*   [`README_zh.md`](README_zh.md#L1) - *Niki-docAI 2.0 (重生版)*
*   [`_AI.md`](_AI.md#L1) - *Context: nk_doc_ai*
*   [`_ARCH.md`](_ARCH.md#L1) - *Project Architecture*
*   [`_DATA.md`](_DATA.md#L1) - *Data Registry*
*   [`_DEPS.md`](_DEPS.md#L1) - *Dependency Graph*
*   [`_DOGFOOD.md`](_DOGFOOD.md#L1) - *Niki-docAI 2.0: Dogfooding Report*
*   [`_GUIDE.md`](_GUIDE.md#L1) - *AI Context Guide (Niki-docAI)*
*   [`_MAP.md`](_MAP.md#L1) - *Project Map*
*   [`_MEMORY.md`](_MEMORY.md#L1) - *Project Memory*
*   [`_RULES.md`](_RULES.md#L1) - *Project Rules*
*   [`_STATS.md`](_STATS.md#L1) - *项目统计报告 (Project Statistics)*
*   [`_STATUS.md`](_STATUS.md#L1) - *Project Status*
*   [`_SYNTAX.md`](_SYNTAX.md#L1) - *PROJECT SYNTAX*
*   [`ndoc.ps1`](ndoc.ps1#L1)
*   [`requirements.txt`](requirements.txt#L1)
*   [`setup.py`](setup.py#L1) - *-----------------------------------------------...*
<!-- NIKI_MAP_END -->
