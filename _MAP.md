# Project Map
> @CONTEXT: Map | Project Structure | @TAGS: @MAP
> 最后更新 (Last Updated): 2026-02-27 18:00:27

## @STRUCTURE
<!-- NIKI_MAP_START -->
*   **build_spec/**
    *   [`_AI.md`](build_spec/_AI.md#L1) - *Context: build_spec*
    *   [`ndoc.spec`](build_spec/ndoc.spec#L1) - *-*- mode: python ; coding: utf-8 -*-*
*   **docs/**
    *   **adr/**
        *   [`001_ecs_plugin_architecture.md`](docs/adr/001_ecs_plugin_architecture.md#L1) - *ADR-001: 基于 ECS 内核与插件化架构 (ECS-Based Kernel & Pl...*
        *   [`_AI.md`](docs/adr/_AI.md#L1) - *Context: adr*
    *   [`_AI.md`](docs/_AI.md#L1) - *Context: docs*
*   **editors/**
    *   **vscode/**
        *   **editors/**
            *   **vscode/**
                *   **server/**
                    *   **ndoc/**
                        *   **brain/**
                            *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/brain/_AI.md#L1) - *Context: brain*
                            *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/brain/__init__.py#L1) - *Brain: Intelligence Layer.*
                            *   [`checker.py`](editors/vscode/editors/vscode/server/ndoc/brain/checker.py#L1) - *Atoms: Constraint Checker (Prefrontal Cortex).*
                            *   [`hippocampus.py`](editors/vscode/editors/vscode/server/ndoc/brain/hippocampus.py#L1) - *Atoms: Hippocampus (Observation Buffer & Heatmap).*
                            *   [`index.py`](editors/vscode/editors/vscode/server/ndoc/brain/index.py#L1) - *Atoms: Semantic Index (Thalamus).*
                            *   [`ingest.py`](editors/vscode/editors/vscode/server/ndoc/brain/ingest.py#L1) - *Brain: Context Ingestion.*
                            *   [`vectordb.py`](editors/vscode/editors/vscode/server/ndoc/brain/vectordb.py#L1) - *Atoms: Vector Database (ChromaDB Wrapper).*
                        *   **core/**
                            *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/core/_AI.md#L1) - *Context: core*
                            *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/core/__init__.py#L1) - *Core: Infrastructure Utilities.*
                            *   [`bootstrap.py`](editors/vscode/editors/vscode/server/ndoc/core/bootstrap.py#L1)
                            *   [`cache.py`](editors/vscode/editors/vscode/server/ndoc/core/cache.py#L1) - *Atoms: Cache Management.*
                            *   [`capabilities.py`](editors/vscode/editors/vscode/server/ndoc/core/capabilities.py#L1) - *Atoms: Capability Manager.*
                            *   [`cli.py`](editors/vscode/editors/vscode/server/ndoc/core/cli.py#L1) - *Core: CLI Command Registry.*
                            *   [`errors.py`](editors/vscode/editors/vscode/server/ndoc/core/errors.py#L1) - *Custom exceptions for ndoc.*
                            *   [`fs.py`](editors/vscode/editors/vscode/server/ndoc/core/fs.py#L1) - *Atoms: File System Traversal.*
                            *   [`graph.py`](editors/vscode/editors/vscode/server/ndoc/core/graph.py#L1) - *Core: Graph Algorithms.*
                            *   [`io.py`](editors/vscode/editors/vscode/server/ndoc/core/io.py#L1) - *Atoms: Input/Output Operations.*
                            *   [`logger.py`](editors/vscode/editors/vscode/server/ndoc/core/logger.py#L1) - *Standardized logging for ndoc.*
                            *   [`map_builder.py`](editors/vscode/editors/vscode/server/ndoc/core/map_builder.py#L1) - *Core: Map Builder.*
                            *   [`native_builder.py`](editors/vscode/editors/vscode/server/ndoc/core/native_builder.py#L1) - *Native Builder: Handles local compilation of la...*
                            *   [`stats.py`](editors/vscode/editors/vscode/server/ndoc/core/stats.py#L1) - *Core: Project Statistics.*
                            *   [`task_manager.py`](editors/vscode/editors/vscode/server/ndoc/core/task_manager.py#L1) - *Core: Task Management.*
                            *   [`templates.py`](editors/vscode/editors/vscode/server/ndoc/core/templates.py#L1)
                            *   [`text_utils.py`](editors/vscode/editors/vscode/server/ndoc/core/text_utils.py#L1) - *Atoms: Text Processing Utilities.*
                            *   [`transforms.py`](editors/vscode/editors/vscode/server/ndoc/core/transforms.py#L1) - *Core: Data Transforms.*
                        *   **flows/**
                            *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/flows/_AI.md#L1) - *Context: flows*
                            *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/flows/__init__.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`adr_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/adr_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`arch_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/arch_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`archive_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/archive_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`capability_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/capability_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`check_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/check_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`clean_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/clean_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`config_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/config_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`context_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/context_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`data_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/data_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`deps_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/deps_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`doctor_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/doctor_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`impact_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/impact_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`init_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/init_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`inject_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/inject_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`lesson_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/lesson_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`map_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/map_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`mind_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/mind_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`prompt_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/prompt_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`quality_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/quality_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`search_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/search_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`status_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/status_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`syntax_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/syntax_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`update_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/update_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`verify_flow.py`](editors/vscode/editors/vscode/server/ndoc/flows/verify_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
                        *   **interfaces/**
                            *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/interfaces/_AI.md#L1) - *Context: interfaces*
                            *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/interfaces/__init__.py#L1) - *Interfaces: Entry Points.*
                            *   [`lsp.py`](editors/vscode/editors/vscode/server/ndoc/interfaces/lsp.py#L1) - *Atoms: Lightweight LSP-like features.*
                        *   **models/**
                            *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/models/_AI.md#L1) - *Context: models*
                            *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/models/__init__.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`config.py`](editors/vscode/editors/vscode/server/ndoc/models/config.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`context.py`](editors/vscode/editors/vscode/server/ndoc/models/context.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`map.py`](editors/vscode/editors/vscode/server/ndoc/models/map.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`scan.py`](editors/vscode/editors/vscode/server/ndoc/models/scan.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`status.py`](editors/vscode/editors/vscode/server/ndoc/models/status.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`symbol.py`](editors/vscode/editors/vscode/server/ndoc/models/symbol.py#L1) - *<NIKI_AUTO_HEADER_START>*
                        *   **parsing/**
                            *   **ast/**
                                *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/parsing/ast/_AI.md#L1) - *Context: ast*
                                *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/parsing/ast/__init__.py#L1) - *Atoms: AST Parsing (Tree-sitter Wrapper).*
                                *   [`base.py`](editors/vscode/editors/vscode/server/ndoc/parsing/ast/base.py#L1) - *Atoms: AST Parsing Base.*
                                *   [`discovery.py`](editors/vscode/editors/vscode/server/ndoc/parsing/ast/discovery.py#L1) - *Atoms: AST Symbol Discovery.*
                                *   [`skeleton.py`](editors/vscode/editors/vscode/server/ndoc/parsing/ast/skeleton.py#L1) - *Atoms: Semantic Skeleton Generator.*
                                *   [`symbols.py`](editors/vscode/editors/vscode/server/ndoc/parsing/ast/symbols.py#L1) - *Atoms: AST Symbol Extraction.*
                                *   [`utils.py`](editors/vscode/editors/vscode/server/ndoc/parsing/ast/utils.py#L1) - *Atoms: AST Parsing Utilities.*
                            *   **deps/**
                                *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/parsing/deps/_AI.md#L1) - *Context: deps*
                                *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/parsing/deps/__init__.py#L1)
                                *   [`api_extractor.py`](editors/vscode/editors/vscode/server/ndoc/parsing/deps/api_extractor.py#L1) - *Parsing: Dependency API Extractor.*
                                *   [`builder.py`](editors/vscode/editors/vscode/server/ndoc/parsing/deps/builder.py#L1) - *Parsing: Dependency Graph Builder.*
                                *   [`core.py`](editors/vscode/editors/vscode/server/ndoc/parsing/deps/core.py#L1) - *Core parsing logic for dependency manifests.*
                                *   [`stats.py`](editors/vscode/editors/vscode/server/ndoc/parsing/deps/stats.py#L1) - *Language Statistics.*
                                *   [`test_mapper.py`](editors/vscode/editors/vscode/server/ndoc/parsing/deps/test_mapper.py#L1) - *Deps: Test Usage Mapper.*
                            *   **langs/**
                                *   **bin/**
                                    *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/bin/_AI.md#L1) - *Context: bin*
                                    *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/bin/__init__.py#L1)
                                    *   [`tree_sitter_dart.dll`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/bin/tree_sitter_dart.dll#L1)
                                *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/_AI.md#L1) - *Context: langs*
                                *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/__init__.py#L1) - *Language Definition Protocol.*
                                *   [`cpp.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/cpp.py#L1)
                                *   [`csharp.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/csharp.py#L1)
                                *   [`dart.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/dart.py#L1)
                                *   [`go.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/go.py#L1)
                                *   [`java.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/java.py#L1)
                                *   [`javascript.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/javascript.py#L1)
                                *   [`python.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/python.py#L1)
                                *   [`rust.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/rust.py#L1)
                                *   [`typescript.py`](editors/vscode/editors/vscode/server/ndoc/parsing/langs/typescript.py#L1)
                            *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/parsing/_AI.md#L1) - *Context: parsing*
                            *   [`_LANGS.json`](editors/vscode/editors/vscode/server/ndoc/parsing/_LANGS.json#L1)
                            *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/parsing/__init__.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`extractors.py`](editors/vscode/editors/vscode/server/ndoc/parsing/extractors.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`rules.py`](editors/vscode/editors/vscode/server/ndoc/parsing/rules.py#L1) - *Parsing: Rule Extraction.*
                            *   [`scanner.py`](editors/vscode/editors/vscode/server/ndoc/parsing/scanner.py#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`universal.py`](editors/vscode/editors/vscode/server/ndoc/parsing/universal.py#L1) - *<NIKI_AUTO_HEADER_START>*
                        *   **templates/**
                            *   **components/**
                                *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/templates/components/_AI.md#L1) - *Context: components*
                                *   [`doc_footer.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/components/doc_footer.tpl#L1)
                                *   [`doc_header.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/components/doc_header.tpl#L1) - *{title}*
                            *   **templates/**
                                *   **components/**
                                    *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/templates/templates/components/_AI.md#L1) - *Context: components*
                                    *   [`doc_footer.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/components/doc_footer.tpl#L1)
                                    *   [`doc_header.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/components/doc_header.tpl#L1) - *{title}*
                                *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/templates/templates/_AI.md#L1) - *Context: templates*
                                *   [`ai.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/ai.md.tpl#L1) - *Context: {name}*
                                *   [`arch.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/arch.md.tpl#L1) - *# 1. Technology Stack*
                                *   [`deps.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/deps.md.tpl#L1) - *# 1. Instability Metrics (Core Modules)*
                                *   [`doctor_report.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/doctor_report.tpl#L1)
                                *   [`guide.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/guide.md.tpl#L1) - *AI Context Guide (Niki-docAI)*
                                *   [`header.py.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/header.py.tpl#L1) - *<NIKI_AUTO_HEADER_START>*
                                *   [`header_injection.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/header_injection.tpl#L1) - *<NIKI_AUTO_HEADER_START>*
                                *   [`impact.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/impact.md.tpl#L1) - *# 1. Changed Files (Scope)*
                                *   [`map.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/map.md.tpl#L1) - *# @STRUCTURE*
                                *   [`prompt.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/prompt.md.tpl#L1) - *Niki-docAI Context Prompt*
                                *   [`rules.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/rules.md.tpl#L1) - *Project Rules*
                                *   [`stats.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/stats.md.tpl#L1) - *# 核心指标 (Core Metrics)*
                                *   [`status.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/status.md.tpl#L1) - *# 1. Pending Tasks (TODOs)*
                                *   [`syntax.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/templates/syntax.md.tpl#L1) - *PROJECT SYNTAX*
                            *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/templates/_AI.md#L1) - *Context: templates*
                            *   [`ai.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/ai.md.tpl#L1) - *Context: {name}*
                            *   [`arch.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/arch.md.tpl#L1) - *# 1. Technology Stack*
                            *   [`deps.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/deps.md.tpl#L1) - *# 1. Instability Metrics (Core Modules)*
                            *   [`doctor_report.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/doctor_report.tpl#L1)
                            *   [`guide.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/guide.md.tpl#L1) - *AI Context Guide (Niki-docAI)*
                            *   [`header.py.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/header.py.tpl#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`header_injection.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/header_injection.tpl#L1) - *<NIKI_AUTO_HEADER_START>*
                            *   [`impact.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/impact.md.tpl#L1) - *# 1. Changed Files (Scope)*
                            *   [`map.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/map.md.tpl#L1) - *# @STRUCTURE*
                            *   [`prompt.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/prompt.md.tpl#L1) - *Niki-docAI Context Prompt*
                            *   [`rules.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/rules.md.tpl#L1) - *Project Rules*
                            *   [`stats.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/stats.md.tpl#L1) - *# 核心指标 (Core Metrics)*
                            *   [`status.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/status.md.tpl#L1) - *# 1. Pending Tasks (TODOs)*
                            *   [`syntax.md.tpl`](editors/vscode/editors/vscode/server/ndoc/templates/syntax.md.tpl#L1) - *PROJECT SYNTAX*
                        *   **views/**
                            *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/views/_AI.md#L1) - *Context: views*
                            *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/views/__init__.py#L1) - *Views: Output Rendering.*
                            *   [`context.py`](editors/vscode/editors/vscode/server/ndoc/views/context.py#L1) - *View: Context Rendering.*
                            *   [`header.py`](editors/vscode/editors/vscode/server/ndoc/views/header.py#L1) - *View: Header Injection.*
                            *   [`map.py`](editors/vscode/editors/vscode/server/ndoc/views/map.py#L1) - *View: Map Rendering.*
                            *   [`mermaid.py`](editors/vscode/editors/vscode/server/ndoc/views/mermaid.py#L1) - *View: Mermaid Graph Renderer.*
                            *   [`reports.py`](editors/vscode/editors/vscode/server/ndoc/views/reports.py#L1) - *View: Report Tables.*
                            *   [`status.py`](editors/vscode/editors/vscode/server/ndoc/views/status.py#L1) - *View: Status Reports.*
                        *   [`_AI.md`](editors/vscode/editors/vscode/server/ndoc/_AI.md#L1) - *Context: ndoc*
                        *   [`__init__.py`](editors/vscode/editors/vscode/server/ndoc/__init__.py#L1) - *Niki-docAI Source Root.*
                        *   [`__main__.py`](editors/vscode/editors/vscode/server/ndoc/__main__.py#L1)
                        *   [`api.py`](editors/vscode/editors/vscode/server/ndoc/api.py#L1) - *Public API: High-level interfaces for Agents an...*
                        *   [`daemon.py`](editors/vscode/editors/vscode/server/ndoc/daemon.py#L1) - *Daemon: Live Context Watcher.*
                        *   [`demo_violation.py`](editors/vscode/editors/vscode/server/ndoc/demo_violation.py#L1) - *@author Niki*
                        *   [`entry.py`](editors/vscode/editors/vscode/server/ndoc/entry.py#L1) - *Entry Point: CLI Execution.*
                        *   [`lsp_server.py`](editors/vscode/editors/vscode/server/ndoc/lsp_server.py#L1) - *LSP Server implementation using pygls.*
                    *   [`_AI.md`](editors/vscode/editors/vscode/server/_AI.md#L1) - *Context: server*
                *   [`_AI.md`](editors/vscode/editors/vscode/_AI.md#L1) - *Context: vscode*
            *   [`_AI.md`](editors/vscode/editors/_AI.md#L1) - *Context: editors*
        *   **out/**
            *   [`_AI.md`](editors/vscode/out/_AI.md#L1) - *Context: out*
            *   [`extension.js`](editors/vscode/out/extension.js#L1)
            *   [`extension.js.map`](editors/vscode/out/extension.js.map#L1)
        *   **src/**
            *   [`_AI.md`](editors/vscode/src/_AI.md#L1) - *Context: src*
            *   [`extension.ts`](editors/vscode/src/extension.ts#L1)
        *   [`LICENSE.md`](editors/vscode/LICENSE.md#L1)
        *   [`README.md`](editors/vscode/README.md#L1) - *Niki-docAI VS Code Extension*
        *   [`_AI.md`](editors/vscode/_AI.md#L1) - *Context: vscode*
        *   [`nk-doc-ai-vscode-0.1.2.vsix`](editors/vscode/nk-doc-ai-vscode-0.1.2.vsix#L1)
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
    *   [`bootstrap.py`](scripts/bootstrap.py#L1) - *Niki-docAI Remote Bootstrap Script.*
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
        *   **cli/**
            *   **commands/**
                *   [`_AI.md`](src/ndoc/cli/commands/_AI.md#L1) - *Context: commands*
                *   [`__init__.py`](src/ndoc/cli/commands/__init__.py#L1) - *CLI Commands Package.*
                *   [`adr.py`](src/ndoc/cli/commands/adr.py#L1) - *Command: Architecture Decision Records (ADR).*
                *   [`all.py`](src/ndoc/cli/commands/all.py#L1) - *Command: Run All Analysis (ECS Pipeline).*
                *   [`arch.py`](src/ndoc/cli/commands/arch.py#L1) - *Command: Architecture.*
                *   [`archive.py`](src/ndoc/cli/commands/archive.py#L1) - *Command: Archive.*
                *   [`caps.py`](src/ndoc/cli/commands/caps.py#L1) - *<NIKI_AUTO_HEADER_START>*
                *   [`check.py`](src/ndoc/cli/commands/check.py#L1) - *Command: Check Constraints.*
                *   [`clean.py`](src/ndoc/cli/commands/clean.py#L1) - *Command: Clean.*
                *   [`context.py`](src/ndoc/cli/commands/context.py#L1) - *Command: Context.*
                *   [`data.py`](src/ndoc/cli/commands/data.py#L1) - *Command: Data Schema Registry.*
                *   [`deps.py`](src/ndoc/cli/commands/deps.py#L1) - *Command: Dependencies.*
                *   [`doctor.py`](src/ndoc/cli/commands/doctor.py#L1) - *Command: Doctor.*
                *   [`impact.py`](src/ndoc/cli/commands/impact.py#L1) - *Command: Impact Analysis.*
                *   [`init.py`](src/ndoc/cli/commands/init.py#L1) - *Command: Init.*
                *   [`inject.py`](src/ndoc/cli/commands/inject.py#L1) - *Command: Inject.*
                *   [`lint.py`](src/ndoc/cli/commands/lint.py#L1) - *Command: Lint.*
                *   [`lsp.py`](src/ndoc/cli/commands/lsp.py#L1) - *Command: LSP Query.*
                *   [`map.py`](src/ndoc/cli/commands/map.py#L1) - *Command: Map.*
                *   [`pilot.py`](src/ndoc/cli/commands/pilot.py#L1) - *Command: Pilot (Legacy Alias).*
                *   [`prompt.py`](src/ndoc/cli/commands/prompt.py#L1) - *Command: AI Prompt.*
                *   [`search.py`](src/ndoc/cli/commands/search.py#L1) - *Command: Search.*
                *   [`server.py`](src/ndoc/cli/commands/server.py#L1) - *Command: LSP Server.*
                *   [`skeleton.py`](src/ndoc/cli/commands/skeleton.py#L1) - *Command: Skeleton Generator.*
                *   [`stats.py`](src/ndoc/cli/commands/stats.py#L1) - *Command: Project Statistics.*
                *   [`typecheck.py`](src/ndoc/cli/commands/typecheck.py#L1) - *Command: Typecheck.*
                *   [`update.py`](src/ndoc/cli/commands/update.py#L1) - *Command: Update.*
                *   [`verify.py`](src/ndoc/cli/commands/verify.py#L1) - *Command: Verify.*
                *   [`watch.py`](src/ndoc/cli/commands/watch.py#L1) - *Command: Watch Mode.*
            *   [`_AI.md`](src/ndoc/cli/_AI.md#L1) - *Context: cli*
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
            *   [`native_builder.py`](src/ndoc/core/native_builder.py#L1) - *Native Builder: Handles local compilation of la...*
            *   [`stats.py`](src/ndoc/core/stats.py#L1) - *Core: Project Statistics.*
            *   [`task_manager.py`](src/ndoc/core/task_manager.py#L1) - *Core: Task Management.*
            *   [`templates.py`](src/ndoc/core/templates.py#L1)
            *   [`text_utils.py`](src/ndoc/core/text_utils.py#L1) - *Atoms: Text Processing Utilities.*
            *   [`transforms.py`](src/ndoc/core/transforms.py#L1) - *Core: Data Transforms.*
        *   **flows/**
            *   [`_AI.md`](src/ndoc/flows/_AI.md#L1) - *Context: flows*
            *   [`__init__.py`](src/ndoc/flows/__init__.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`clean_flow.py`](src/ndoc/flows/clean_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`config_flow.py`](src/ndoc/flows/config_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`inject_flow.py`](src/ndoc/flows/inject_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`quality_flow.py`](src/ndoc/flows/quality_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`update_flow.py`](src/ndoc/flows/update_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`verify_flow.py`](src/ndoc/flows/verify_flow.py#L1) - *<NIKI_AUTO_HEADER_START>*
        *   **interfaces/**
            *   [`_AI.md`](src/ndoc/interfaces/_AI.md#L1) - *Context: interfaces*
            *   [`__init__.py`](src/ndoc/interfaces/__init__.py#L1) - *Interfaces: Entry Points.*
            *   [`lsp.py`](src/ndoc/interfaces/lsp.py#L1) - *Atoms: Lightweight LSP-like features.*
        *   **kernel/**
            *   [`_AI.md`](src/ndoc/kernel/_AI.md#L1) - *Context: kernel*
            *   [`__init__.py`](src/ndoc/kernel/__init__.py#L1) - *Niki-docAI Kernel.*
            *   [`bootstrap.py`](src/ndoc/kernel/bootstrap.py#L1) - *Bootstrap new ECS Kernel and load default plugins.*
            *   [`context.py`](src/ndoc/kernel/context.py#L1) - *Core Kernel Context (ECS World).*
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
        *   **plugins/**
            *   [`_AI.md`](src/ndoc/plugins/_AI.md#L1) - *Context: plugins*
            *   [`adr_report.py`](src/ndoc/plugins/adr_report.py#L1) - *ADR Report Plugin (Action).*
            *   [`arch_report.py`](src/ndoc/plugins/arch_report.py#L1) - *Architecture Report Plugin (Action).*
            *   [`capability_map.py`](src/ndoc/plugins/capability_map.py#L1) - *Capability Map Plugin (Action).*
            *   [`checker.py`](src/ndoc/plugins/checker.py#L1) - *Constraint Checker Plugin (Action).*
            *   [`collector.py`](src/ndoc/plugins/collector.py#L1) - *Standard File Collector Plugin.*
            *   [`context_report.py`](src/ndoc/plugins/context_report.py#L1) - *Context Report Plugin (Action).*
            *   [`data_schema.py`](src/ndoc/plugins/data_schema.py#L1) - *Data Schema Plugin (Action).*
            *   [`deps_report.py`](src/ndoc/plugins/deps_report.py#L1) - *Dependency Report Plugin (Action).*
            *   [`deps_sensor.py`](src/ndoc/plugins/deps_sensor.py#L1) - *Dependency Graph Sensor Plugin.*
            *   [`lesson_report.py`](src/ndoc/plugins/lesson_report.py#L1) - *Lesson Report Plugin (Action).*
            *   [`map_report.py`](src/ndoc/plugins/map_report.py#L1) - *Map Report Plugin (Action).*
            *   [`memory_report.py`](src/ndoc/plugins/memory_report.py#L1) - *Memory Report Plugin (Action).*
            *   [`mind_map.py`](src/ndoc/plugins/mind_map.py#L1) - *Mind Map Plugin (Action).*
            *   [`scanner.py`](src/ndoc/plugins/scanner.py#L1) - *Syntax Analysis Plugin (Sensor).*
            *   [`stats_report.py`](src/ndoc/plugins/stats_report.py#L1) - *Stats Report Plugin (Action).*
            *   [`status.py`](src/ndoc/plugins/status.py#L1) - *Status Report Plugin (Ported from Status Flow).*
            *   [`syntax_manual.py`](src/ndoc/plugins/syntax_manual.py#L1) - *Syntax Manual Plugin (Action).*
        *   **sdk/**
            *   [`_AI.md`](src/ndoc/sdk/_AI.md#L1) - *Context: sdk*
            *   [`__init__.py`](src/ndoc/sdk/__init__.py#L1) - *Niki-docAI SDK.*
            *   [`interfaces.py`](src/ndoc/sdk/interfaces.py#L1) - *Plugin Interface Definitions (HookSpecs)*
            *   [`models.py`](src/ndoc/sdk/models.py#L1) - *Core Data Models (Entities & Components)*
        *   **services/**
            *   [`_AI.md`](src/ndoc/services/_AI.md#L1) - *Context: services*
            *   [`check_service.py`](src/ndoc/services/check_service.py#L1) - *Check Service (Kernel-as-a-Service).*
            *   [`impact_service.py`](src/ndoc/services/impact_service.py#L1) - *Impact Service (Kernel-as-a-Service).*
            *   [`prompt_service.py`](src/ndoc/services/prompt_service.py#L1) - *Prompt Service (Kernel-as-a-Service).*
            *   [`search_service.py`](src/ndoc/services/search_service.py#L1) - *Search Service (Kernel-as-a-Service).*
        *   **templates/**
            *   **components/**
                *   [`_AI.md`](src/ndoc/templates/components/_AI.md#L1) - *Context: components*
                *   [`doc_footer.tpl`](src/ndoc/templates/components/doc_footer.tpl#L1)
                *   [`doc_header.tpl`](src/ndoc/templates/components/doc_header.tpl#L1) - *{{ title }}*
            *   [`_AI.md`](src/ndoc/templates/_AI.md#L1) - *Context: templates*
            *   [`ai.md.tpl`](src/ndoc/templates/ai.md.tpl#L1) - *# !RULE*
            *   [`arch.md.tpl`](src/ndoc/templates/arch.md.tpl#L1) - *# 1. Technology Stack*
            *   [`deps.md.tpl`](src/ndoc/templates/deps.md.tpl#L1) - *# 1. Instability Metrics (Core Modules)*
            *   [`doctor_report.tpl`](src/ndoc/templates/doctor_report.tpl#L1)
            *   [`guide.md.tpl`](src/ndoc/templates/guide.md.tpl#L1)
            *   [`header.py.tpl`](src/ndoc/templates/header.py.tpl#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`header_injection.tpl`](src/ndoc/templates/header_injection.tpl#L1) - *<NIKI_AUTO_HEADER_START>*
            *   [`impact.md.tpl`](src/ndoc/templates/impact.md.tpl#L1) - *# 1. Changed Files (Scope)*
            *   [`map.md.tpl`](src/ndoc/templates/map.md.tpl#L1) - *# @STRUCTURE*
            *   [`prompt.md.tpl`](src/ndoc/templates/prompt.md.tpl#L1) - *Niki-docAI Context Prompt*
            *   [`rules.md.tpl`](src/ndoc/templates/rules.md.tpl#L1) - *# Scanning Rules (扫描规则)*
            *   [`stats.md.tpl`](src/ndoc/templates/stats.md.tpl#L1) - *# 核心指标 (Core Metrics)*
            *   [`status.md.tpl`](src/ndoc/templates/status.md.tpl#L1) - *# 1. Pending Tasks (TODOs)*
            *   [`syntax.md.tpl`](src/ndoc/templates/syntax.md.tpl#L1)
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
        *   [`_AI.md`](src/niki_doc_ai.egg-info/_AI.md#L1) - *Context: niki_doc_ai.egg-info*
        *   [`dependency_links.txt`](src/niki_doc_ai.egg-info/dependency_links.txt#L1)
        *   [`entry_points.txt`](src/niki_doc_ai.egg-info/entry_points.txt#L1)
        *   [`requires.txt`](src/niki_doc_ai.egg-info/requires.txt#L1)
        *   [`top_level.txt`](src/niki_doc_ai.egg-info/top_level.txt#L1)
    *   [`_AI.md`](src/_AI.md#L1) - *Context: src*
*   **tests/**
    *   **fixtures/**
        *   [`_AI.md`](tests/fixtures/_AI.md#L1) - *Context: fixtures*
        *   [`complex_api.py`](tests/fixtures/complex_api.py#L1)
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
*   [`PROJECT_STATUS.md`](PROJECT_STATUS.md#L1) - *Niki-docAI 项目功能落地状态报告*
*   [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md#L1) - *Niki-docAI 项目核心功能综述*
*   [`README.md`](README.md#L1) - *Niki-docAI 2.0 (Rebirth)*
*   [`README_zh.md`](README_zh.md#L1) - *Niki-docAI 2.0 (重生版)*
*   [`_AI.md`](_AI.md#L1) - *Context: nk_doc_ai*
*   [`_ARCH.md`](_ARCH.md#L1) - *Project Architecture*
*   [`_DEPS.md`](_DEPS.md#L1) - *Dependency Analysis*
*   [`_DOGFOOD.md`](_DOGFOOD.md#L1) - *Niki-docAI 2.0: Dogfooding Report*
*   [`_GUIDE.md`](_GUIDE.md#L1) - *AI Context Guide (Niki-docAI)*
*   [`_MAP.md`](_MAP.md#L1) - *Project Map*
*   [`_MEMORY.md`](_MEMORY.md#L1) - *Project Memory*
*   [`_RULES.md`](_RULES.md#L1) - *Project Rules*
*   [`_STATUS.md`](_STATUS.md#L1) - *Project Status*
*   [`_STATUS_NEW.md`](_STATUS_NEW.md#L1) - *Project Status*
*   [`install.ps1`](install.ps1#L1) - *Niki-docAI Unified Installer (Windows)*
*   [`install.sh`](install.sh#L1) - *Niki-docAI Unified Installer (Unix/Linux/macOS)*
*   [`lsp_test.log`](lsp_test.log#L1)
*   [`ndoc.ps1`](ndoc.ps1#L1)
*   [`requirements.txt`](requirements.txt#L1)
*   [`setup.py`](setup.py#L1) - *-----------------------------------------------...*
<!-- NIKI_MAP_END -->

---
*Generated by Niki-docAI*
