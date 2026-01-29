# PROJECT ROADMAP

## @CURRENT (Phase 5: Niki-ALM & Automation)

### 1. Niki-ALM (Project Lifecycle Engine)
> **Goal**: 实现 "Idea -> Plan -> Code -> Done -> Memory" 的自动化闭环管理。

*   [ ] **Plan & Split (The Planner)**:
    *   [ ] 实现 `ndoc plan "Objective"` 命令，通过 LLM 自动将一句话目标拆解为 `_NEXT.md` 中的结构化任务。
*   [ ] **Task Tracking (The Tracker)**:
    *   [ ] 实现 `Todo Flow`：自动扫描代码中的 `TODO/FIXME`，聚合到 `_NEXT.md` 底部。
    *   [ ] 增强 `Scanner`：识别代码完成状态，自动更新 `_NEXT.md` 中的 Checkbox (关联 Task ID)。
*   [ ] **Archive & Memory (The Archivist)**:
    *   [ ] 实现自动归档：当 Section 下任务全完成时，自动移入 `@HISTORY`。
    *   [ ] 实现记忆提取：分析完成的任务，提取关键决策点并更新 `_MEMORY.md`。

### 2. Live Context Daemon (Optimization)
*   [x] **File Watcher**: 实现高效的文件变更监听 (Watchdog)。
*   [ ] **Incremental Update**: 实现基于变更文件的增量文档更新，而非全量扫描。

## @HISTORY (Completed)

### Phase 2 & 3: Parsing & Foundation
*   [x] **Testing Strategy**: 建立了 `tests/` 和 `pytest` 体系。
*   [x] **Tree-sitter Integration**: 完成了基于 AST 的代码解析（Class, Function, Decorator, Signature）。
*   [x] **Scanner Migration**: 移除了代码解析的正则依赖，确立了混合解析策略。
*   [x] **Dogfooding**: 通过了项目自测。

## @PLAN (Future)

### Phase 3: Parsing Evolution (The "Eyes")
*   **Tree-sitter Integration**: 引入 Tree-sitter (Python binding) 替代正则解析，实现稳健的增量 AST 解析。
    *   Goal: 容错性解析，结构化数据获取 (CST)。
*   **LSP Integration**: 探索与 Language Server Protocol 的对接。
    *   Goal: 获取 IDE 级别的语义数据 (Symbols, References, Hovers)。

### Phase 4: IDE Plugin (The "Brain")
*   **VS Code Extension**: 开发原生插件，实时消费 LSP 数据并更新 Live Context。

## @CODE_TODOS
> Auto-generated from source code. Do not edit manually.

<!-- NIKI_TODO_START -->
<!-- NIKI_TODO_END -->
