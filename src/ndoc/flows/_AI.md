# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:27:56

## !RULE
*   **Dependency Injection**: Flows (especially `verify_flow`) SHOULD accept dependencies (`fs`, `io`, `scanner`, `logger`) as optional arguments in `run()` to enable unit testing without mocking global modules.
*   **Standardized Logging**: Use `ndoc.core.logger` for all execution status updates. `print()` is reserved strictly for CLI command output (e.g., `ndoc prompt`, `ndoc map`).
*   **Idempotency**: All flows MUST be idempotent. Running a flow multiple times should produce the same result and not duplicate content.
*   **Atomic Writes**: File generation should prepare content in memory and write once using `io.write_text`.
*   **Local Capability Path**: Flow-level import checks must initialize `CapabilityManager` to include project-local `.ndoc/lib` on `sys.path`.
*   **Quality Gates**: `quality_flow` executes lint/typecheck commands defined in `_RULES.md` and must fail fast on non-zero exit codes.
*   **Command Execution Mode**: `quality_flow` runs commands without shell unless shell operators are present, to reduce risk and improve portability.
*   **Unified Status Entry**: `status_flow` is the single source of truth for TODO/Stats aggregation; legacy flows must delegate without duplicating logic.
*   **@OVERVIEW**: Status/Todo/Stats 聚合统一由 `status_flow` 生成与维护。
*   **!RULE**: 任何任务聚合或统计变更必须落在 `status_flow`，禁止新增并行实现。
*   **@ANALYSIS**: Pitfall - 多处触发独立统计会重复扫描，需复用 `collect_full_stats` 结果。

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Dynamic Capability Loading**: New flows (like `capability_flow.py`) must be registered in `entry.py` to ensure they are executed during the relevant lifecycle phases (e.g., `init`, `map`, `all`).
*   **Auto-Provisioning**: `capability_flow` acts as the project's "immune system", proactively detecting and installing missing language capabilities based on file extensions. This logic should remain lightweight and idempotent.
*   **Modular Architecture**: The project now follows a layered architecture:
    *   `core/`: Infrastructure (FS, IO, Capabilities)
    *   `parsing/`: Code analysis (Scanner, AST, Deps, Langs)
    *   `brain/`: Intelligence (Index, Memory, Checker, LLM)
    *   `interfaces/`: Entry points (LSP, Daemon)
    *   `flows/`: Business logic (Context, Arch, Check, etc.)
*   **Architecture Split**: `arch_flow` now generates three separate files:
    *   `_ARCH.md`: High-level technology stack and Third-Party Dependencies (BOM).
    *   `_MAP.md`: Detailed file structure tree.
    *   `_DEPS.md`: Component Relationships with Instability Metrics (Ca/Ce/I) and Layered Topology.
*   **Universal AST Adapter**: `universal.py` uses `_LANGS.json` to drive multi-language dependency extraction (Python, JS, Java, C++, etc.), replacing the previous Python-only regex approach.
*   **Recommended API Mapping**: To support agent integration (MCP/Tool), the following flows map to high-level actions:
    *   `refresh_context()` -> `context_flow.run()` + `arch_flow.run()` (or `ndoc all`)
    *   `get_semantic_context()` -> `prompt_flow.run(focus=True)` (with VectorDB retrieval)
    *   `validate_architecture()` -> `check_flow.run()`
    *   `analyze_impact()` -> `impact_flow.run()`
    *   `get_module_dependencies()` -> `deps_flow.run()`
    *   `search_codebase()` -> `search_flow.run()` (Direct VectorDB query)

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: . @DEP: .
*   **[adr_flow.py](adr_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..models.config, ..parsing, collections, pathlib, ... @DEP: ..parsing, ..models.config, ..core, typing, collections, pathlib
*   **[arch_flow.py](arch_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ., ..core, ..core.logger, ..models.config, ..parsing, ... @DEP: ..parsing, ..models.config, ..core, typing, ..core.logger, ., collections, datetime ...
*   **[archive_flow.py](archive_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..brain.vectordb, ..core, ..models.config, ..parsing, datetime, ... @DEP: ..parsing, ..models.config, ..core, ..brain.vectordb, typing, datetime, pathlib
*   **[capability_flow.py](capability_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..models.config, ..parsing, pathlib, typing @DEP: ..parsing, ..models.config, ..core, typing, pathlib
*   **[check_flow.py](check_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..brain, ..core, ..models.config, ..models.context, ..parsing, ... @DEP: ..parsing, ..models.context, ..models.config, ..core, typing, ..brain, pathlib
*   **[clean_flow.py](clean_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.models.config, os, pathlib, typing @DEP: typing, ndoc.models.config, pathlib, os
*   **[config_flow.py](config_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ndoc.models.config, pathlib, re, typing @DEP: re, ..core, typing, ndoc.models.config, pathlib
*   **[context_flow.py](context_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..brain.vectordb, ..core, ..core.logger, ..interfaces, ..models.config, ... @DEP: ..parsing, re, ..models.config, ..models.context, ..core, ..brain.vectordb, ..interfaces, typing ...
*   **[data_flow.py](data_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..core.logger, ..models.config, ..models.context, ..parsing, ... @DEP: ..parsing, ..models.config, ..models.context, ..core, typing, ..core.logger, dataclasses, datetime ...
*   **[deps_flow.py](deps_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..core.logger, ..models.config, ..parsing, collections, ... @DEP: ..parsing, ..models.config, ..core, typing, ..core.logger, collections, datetime, pathlib
*   **[doctor_flow.py](doctor_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..core.capabilities, ..core.logger, ..models.config, ..parsing, ... @DEP: ..parsing, ..core.capabilities, ..models.config, ..core, ..parsing.deps, typing, ..core.logger, tree_sitter ...
*   **[impact_flow.py](impact_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..models.config, ..parsing, .deps_flow, collections, pathlib, ... @DEP: ..parsing, ..models.config, .deps_flow, subprocess, typing, collections, pathlib
*   **[init_flow.py](init_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.flows, ndoc.models.config @DEP: ndoc.models.config, ndoc.flows
*   **[inject_flow.py](inject_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..core.logger, ..models.config, ..parsing, pathlib, ... @DEP: ..parsing, re, ..models.config, ..core, typing, ..core.logger, pathlib
*   **[lesson_flow.py](lesson_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..models.config, ..parsing, pathlib, typing @DEP: ..parsing, ..models.config, ..core, typing, pathlib
*   **[map_flow.py](map_flow.py#L1)**: ------------------------------------------------------------------------------ @DEP: ..core, ..models.config, ..parsing, concurrent.futures, dataclasses, ... @DEP: ..parsing, ..models.config, ..core, typing, dataclasses, datetime, pathlib, concurrent.futures
*   **[mind_flow.py](mind_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..models.config, ..parsing, collections, pathlib, ... @DEP: ..parsing, ..models.config, ..core, typing, collections, pathlib
*   **[prompt_flow.py](prompt_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..brain, ..brain.vectordb, ..core, ..core.logger, ..models.config, ... @DEP: ..parsing, re, ..models.config, ..core, ..brain.vectordb, typing, ..core.logger, ..brain ...
*   **[quality_flow.py](quality_flow.py#L1)**: Flow: Quality Gates. @DEP: ..core.logger, ndoc.models.config, os, pathlib, shlex, ... @DEP: subprocess, shlex, typing, ..core.logger, ndoc.models.config, pathlib, os
*   **[search_flow.py](search_flow.py#L1)**: Flow: Semantic Search. @DEP: ..brain.vectordb, ..core.logger, ..models.config, pathlib, typing @DEP: ..models.config, ..brain.vectordb, typing, ..core.logger, pathlib
*   **[stats_flow.py](stats_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ., ndoc.models.config, pathlib @DEP: ndoc.models.config, pathlib, .
*   **[status_flow.py](status_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..core.logger, ..models.config, ..parsing, .deps_flow, ... @DEP: ..parsing, re, ..models.config, ..core, .deps_flow, typing, ..core.logger, time ...
*   **[syntax_flow.py](syntax_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ndoc.models.config, pathlib @DEP: ..core, ndoc.models.config, pathlib
*   **[test_map_flow.py](test_map_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ast as py_ast, ndoc.core.fs, ndoc.core.io, ndoc.models.config, ndoc.parsing.ast, ... @DEP: ndoc.core.fs, ndoc.parsing.ast.discovery, typing, ndoc.parsing.ast, ast as py_ast, ndoc.models.config, ndoc.core.io, pathlib
*   **[todo_flow.py](todo_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ., ..models.config, pathlib, typing @DEP: ., pathlib, typing, ..models.config
*   **[update_flow.py](update_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, pathlib, subprocess, sys, typing @DEP: ..core, subprocess, typing, sys, pathlib
*   **[verify_flow.py](verify_flow.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..core.logger, ..parsing, ndoc.models.config, sys @DEP: ..parsing, ..core, ..core.logger, ndoc.models.config, sys
<!-- NIKI_AUTO_Context_END -->
