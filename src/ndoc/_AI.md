# Context: ndoc
> @CONTEXT: Local | ndoc | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:28:01

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Proactive Capability Check**: `entry.py` serves as the primary gatekeeper. It must invoke `capability_flow` to ...ensure all necessary language parsers are installed *before* executing documentation generation flows (`map`, `context`, `all`).
*   **Dynamic Watchdog**: `daemon.py` monitors file system events. When a new file type is detected (e.g., a `.rs` file added to a python project), it must trigger a capability check to auto-provision the parser on the fly, ensuring zero-configuration support for polyglot projects.
*   **CLI Robustness**: All CLI commands (including `lsp`) must handle missing capabilities gracefully, either by attempting auto-installation or falling back to regex-based scanning without crashing.
*   **LSP Protocol Integrity**: `entry.py`'s `server` command MUST NOT print anything to `stdout` other than JSON-RPC messages. All logs must go to `stderr`.
*   **Context Awareness**: `lsp_server.py` implements "Thinking Context" via `textDocument/hover`, aggregating rules and memories from `_AI.md` hierarchy.
*   **LSP Command Contract**: `lsp_server.py` 必须通过 `workspace/executeCommand` 暴露 `ndoc.getThinkingContext`，返回目标文件的层级规则上下文。
*   **IDE Quick Entry**: `lsp_server.py` 应提供 `textDocument/codeLens` 入口，触发 `ndoc.showContext` 以快速展示上下文。
*   **Hover Structure**: Hover 内容应按 Symbol / Rules / Vector 分区输出，保证可读性与可复制性。
*   **Diagnostics Precision**: LSP 诊断必须使用 `checker.Violation` 的行列信息进行精准标注。
*   **Unified API Surface**: `ndoc.api.NdocAPI` exposes high-level capabilities (Search, Context, Check) for external agents (MCP Servers, CI Scripts), decoupling them from internal CLI arguments.
*   **Quality Gate CLI**: `entry.py` exposes `lint` and `typecheck` commands driven by `_RULES.md` without hardcoding toolchains.
*   **CLI Deprecation Redirect**: `todo` and `stats` commands must route through `status` and shared status logic.
*   **@USAGE**: CLI 层仅保留 `status` 作为聚合入口，`todo`/`stats` 为兼容转发。
*   **@ANALYSIS**: Pitfall - 直接调用旧入口会触发重复扫描与文件写入，需统一走 status。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[atoms/](atoms/_AI.md#L1)**
*   **[brain/](brain/_AI.md#L1)**
*   **[core/](core/_AI.md#L1)**
*   **[flows/](flows/_AI.md#L1)**
*   **[interfaces/](interfaces/_AI.md#L1)**
*   **[models/](models/_AI.md#L1)**
*   **[parsing/](parsing/_AI.md#L1)**
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START>
*   **[api.py](api.py#L1)**: Public API: High-level interfaces for Agents and MCP Servers. @DEP: .flows, .models.config, pathlib, typing @DEP: .models.config, pathlib, typing, .flows
*   **[daemon.py](daemon.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ndoc.brain.hippocampus, ndoc.core.logger, ndoc.flows, ndoc.models.config, pathlib, ... @DEP: threading, ndoc.core.logger, ndoc.flows, watchdog.events, traceback, ndoc.brain.hippocampus, watchdog.observers, typing ...
*   **[demo_violation.py](demo_violation.py#L1)**: @author Niki
*   **[entry.py](entry.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: argparse, logging, ndoc, ndoc.atoms, ndoc.core, ... @DEP: ndoc.core.logger, ndoc.flows, argparse, ndoc.atoms, ndoc, ndoc.daemon, ndoc.models.config, ndoc.core ...
*   **[lsp_server.py](lsp_server.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: logging, lsprotocol.types, ndoc.brain, ndoc.brain.vectordb, ndoc.core, ... @DEP: ndoc.interfaces.lsp, ndoc.flows, lsprotocol.types, typing, ndoc.models.context, ndoc.brain, ndoc.core, ndoc.brain.vectordb ...
<!-- NIKI_AUTO_Context_END -->
