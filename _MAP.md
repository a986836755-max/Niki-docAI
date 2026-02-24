# Project Map
> @CONTEXT: Map | Project Structure
> 最后更新 (Last Updated): 2026-02-24 15:01:42

## @STRUCTURE
<!-- NIKI_MAP_START -->
*   **editors/**
    *   **vscode/**
        *   **editors/**
            *   **vscode/**
            *   [`_AI.md`](editors/vscode/editors/_AI.md#L1) - *Context: editors*
        *   **out/**
            *   [`_AI.md`](editors/vscode/out/_AI.md#L1) - *Context: out*
            *   [`extension.js`](editors/vscode/out/extension.js#L1)
            *   [`extension.js.map`](editors/vscode/out/extension.js.map#L1)
        *   **src/**
            *   [`_AI.md`](editors/vscode/src/_AI.md#L1) - *Context: src*
            *   [`extension.ts`](editors/vscode/src/extension.ts#L1)
        *   [`_AI.md`](editors/vscode/_AI.md#L1) - *Context: vscode*
        *   [`package-lock.json`](editors/vscode/package-lock.json#L1)
        *   [`package.json`](editors/vscode/package.json#L1)
        *   [`tsconfig.json`](editors/vscode/tsconfig.json#L1)
    *   [`_AI.md`](editors/_AI.md#L1) - *Context: editors*
*   **samples/**
    *   [`_AI.md`](samples/_AI.md#L1) - *Context: samples*
    *   [`sample_csharp.cs`](samples/sample_csharp.cs#L1)
*   **src/**
    *   **ndoc/**
        *   **atoms/**
            *   **ast/**
                *   [`_AI.md`](src/ndoc/atoms/ast/_AI.md#L1) - *Context: ast*
                *   [`__init__.py`](src/ndoc/atoms/ast/__init__.py#L1) - *"""*
                *   [`base.py`](src/ndoc/atoms/ast/base.py#L1) - *"""*
                *   [`discovery.py`](src/ndoc/atoms/ast/discovery.py#L1) - *"""*
                *   [`symbols.py`](src/ndoc/atoms/ast/symbols.py#L1) - *"""*
                *   [`utils.py`](src/ndoc/atoms/ast/utils.py#L1) - *"""*
            *   **deps/**
                *   [`_AI.md`](src/ndoc/atoms/deps/_AI.md#L1) - *Context: deps*
                *   [`__init__.py`](src/ndoc/atoms/deps/__init__.py#L1) - *"""*
                *   [`core.py`](src/ndoc/atoms/deps/core.py#L1) - *"""*
                *   [`manifests.py`](src/ndoc/atoms/deps/manifests.py#L1) - *"""*
                *   [`parsers.py`](src/ndoc/atoms/deps/parsers.py#L1) - *"""*
                *   [`stats.py`](src/ndoc/atoms/deps/stats.py#L1) - *"""*
            *   **langs/**
                *   [`_AI.md`](src/ndoc/atoms/langs/_AI.md#L1) - *Context: langs*
                *   [`__init__.py`](src/ndoc/atoms/langs/__init__.py#L1) - *"""*
                *   [`cpp.py`](src/ndoc/atoms/langs/cpp.py#L1)
                *   [`csharp.py`](src/ndoc/atoms/langs/csharp.py#L1)
                *   [`dart.py`](src/ndoc/atoms/langs/dart.py#L1)
                *   [`go.py`](src/ndoc/atoms/langs/go.py#L1)
                *   [`java.py`](src/ndoc/atoms/langs/java.py#L1)
                *   [`javascript.py`](src/ndoc/atoms/langs/javascript.py#L1)
                *   [`python.py`](src/ndoc/atoms/langs/python.py#L1)
                *   [`rust.py`](src/ndoc/atoms/langs/rust.py#L1)
                *   [`typescript.py`](src/ndoc/atoms/langs/typescript.py#L1)
            *   [`_AI.md`](src/ndoc/atoms/_AI.md#L1) - *Context: atoms*
            *   [`__init__.py`](src/ndoc/atoms/__init__.py#L1) - *"""*
            *   [`cache.py`](src/ndoc/atoms/cache.py#L1) - *"""*
            *   [`capabilities.py`](src/ndoc/atoms/capabilities.py#L1) - *"""*
            *   [`fs.py`](src/ndoc/atoms/fs.py#L1) - *"""*
            *   [`io.py`](src/ndoc/atoms/io.py#L1) - *"""*
            *   [`llm.py`](src/ndoc/atoms/llm.py#L1) - *"""*
            *   [`lsp.py`](src/ndoc/atoms/lsp.py#L1) - *"""*
            *   [`scanner.py`](src/ndoc/atoms/scanner.py#L1) - *"""*
            *   [`text_utils.py`](src/ndoc/atoms/text_utils.py#L1) - *"""*
        *   **flows/**
            *   [`_AI.md`](src/ndoc/flows/_AI.md#L1) - *Context: flows*
            *   [`__init__.py`](src/ndoc/flows/__init__.py#L1) - *"""*
            *   [`archive_flow.py`](src/ndoc/flows/archive_flow.py#L1) - *"""*
            *   [`capability_flow.py`](src/ndoc/flows/capability_flow.py#L1) - *"""*
            *   [`clean_flow.py`](src/ndoc/flows/clean_flow.py#L1) - *"""*
            *   [`config_flow.py`](src/ndoc/flows/config_flow.py#L1) - *"""*
            *   [`context_flow.py`](src/ndoc/flows/context_flow.py#L1) - *"""*
            *   [`data_flow.py`](src/ndoc/flows/data_flow.py#L1) - *"""*
            *   [`deps_flow.py`](src/ndoc/flows/deps_flow.py#L1) - *"""*
            *   [`doctor_flow.py`](src/ndoc/flows/doctor_flow.py#L1) - *"""*
            *   [`init_flow.py`](src/ndoc/flows/init_flow.py#L1) - *"""*
            *   [`map_flow.py`](src/ndoc/flows/map_flow.py#L1) - *"""*
            *   [`plan_flow.py`](src/ndoc/flows/plan_flow.py#L1) - *"""*
            *   [`prompt_flow.py`](src/ndoc/flows/prompt_flow.py#L1) - *"""*
            *   [`stats_flow.py`](src/ndoc/flows/stats_flow.py#L1) - *"""*
            *   [`symbols_flow.py`](src/ndoc/flows/symbols_flow.py#L1) - *"""*
            *   [`syntax_flow.py`](src/ndoc/flows/syntax_flow.py#L1) - *"""*
            *   [`tech_flow.py`](src/ndoc/flows/tech_flow.py#L1) - *"""*
            *   [`todo_flow.py`](src/ndoc/flows/todo_flow.py#L1) - *"""*
            *   [`update_flow.py`](src/ndoc/flows/update_flow.py#L1) - *"""*
            *   [`verify_flow.py`](src/ndoc/flows/verify_flow.py#L1) - *"""*
        *   **models/**
            *   [`_AI.md`](src/ndoc/models/_AI.md#L1) - *Context: models*
            *   [`__init__.py`](src/ndoc/models/__init__.py#L1) - *"""*
            *   [`config.py`](src/ndoc/models/config.py#L1) - *"""*
            *   [`context.py`](src/ndoc/models/context.py#L1) - *"""*
        *   [`_AI.md`](src/ndoc/_AI.md#L1) - *Context: ndoc*
        *   [`__init__.py`](src/ndoc/__init__.py#L1) - *"""*
        *   [`daemon.py`](src/ndoc/daemon.py#L1) - *"""*
        *   [`entry.py`](src/ndoc/entry.py#L1) - *"""*
        *   [`lsp_server.py`](src/ndoc/lsp_server.py#L1) - *"""*
    *   **niki_doc_ai.egg-info/**
        *   [`PKG-INFO`](src/niki_doc_ai.egg-info/PKG-INFO#L1)
        *   [`SOURCES.txt`](src/niki_doc_ai.egg-info/SOURCES.txt#L1)
        *   [`_AI.md`](src/niki_doc_ai.egg-info/_AI.md#L1)
        *   [`dependency_links.txt`](src/niki_doc_ai.egg-info/dependency_links.txt#L1)
        *   [`entry_points.txt`](src/niki_doc_ai.egg-info/entry_points.txt#L1)
        *   [`requires.txt`](src/niki_doc_ai.egg-info/requires.txt#L1)
        *   [`top_level.txt`](src/niki_doc_ai.egg-info/top_level.txt#L1)
    *   [`_AI.md`](src/_AI.md#L1) - *Context: src*
*   **tests/**
    *   **fixtures/**
        *   [`_AI.md`](tests/fixtures/_AI.md#L1) - *Context: fixtures*
        *   [`complex_api.py`](tests/fixtures/complex_api.py#L1)
    *   **temp/**
    *   [`_AI.md`](tests/_AI.md#L1) - *Context: tests*
    *   [`conftest.py`](tests/conftest.py#L1)
    *   [`test_ast.py`](tests/test_ast.py#L1)
    *   [`test_capabilities.py`](tests/test_capabilities.py#L1)
    *   [`test_capability_flow.py`](tests/test_capability_flow.py#L1)
    *   [`test_csharp_api.py`](tests/test_csharp_api.py#L1)
    *   [`test_lsp_server.py`](tests/test_lsp_server.py#L1) - *"""*
    *   [`test_scanner.py`](tests/test_scanner.py#L1)
*   **tools/**
    *   [`_AI.md`](tools/_AI.md#L1) - *Context: tools*
    *   [`doxygen.exe`](tools/doxygen.exe#L1)
*   [`README.md`](README.md#L1) - *Niki-docAI*
*   [`_AI.md`](_AI.md#L1) - *Context: nk_doc_ai*
*   [`_ARCH.md`](_ARCH.md#L1) - *PROJECT ARCHITECTURE*
*   [`_DATA.md`](_DATA.md#L1) - *Data Registry*
*   [`_DEPS.md`](_DEPS.md#L1) - *Dependency Graph*
*   [`_MAP.md`](_MAP.md#L1) - *Project Map*
*   [`_MEMORY.md`](_MEMORY.md#L1) - *PROJECT MEMORY*
*   [`_NEXT.md`](_NEXT.md#L1) - *Todo List*
*   [`_RULES.md`](_RULES.md#L1) - *Project Rules*
*   [`_STATS.md`](_STATS.md#L1) - *项目统计报告 (Project Statistics)*
*   [`_SYMBOLS.md`](_SYMBOLS.md#L1) - *Symbol Index*
*   [`_SYNTAX.md`](_SYNTAX.md#L1) - *PROJECT SYNTAX*
*   [`_TECH.md`](_TECH.md#L1) - *Tech Stack Snapshot*
*   [`debug_scanner.py`](debug_scanner.py#L1)
*   [`debug_symbols.py`](debug_symbols.py#L1)
*   [`requirements.txt`](requirements.txt#L1) - *Core Dependencies*
*   [`setup.py`](setup.py#L1)
*   [`symbols_log.txt`](symbols_log.txt#L1)
*   [`test_enhanced_doc.py`](test_enhanced_doc.py#L1) - *"""*
*   [`test_python_fix.py`](test_python_fix.py#L1)
*   [`test_regex.py`](test_regex.py#L1)
<!-- NIKI_MAP_END -->
