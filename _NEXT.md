# PROJECT ROADMAP
> 最后更新 (Last Updated): 2026-01-30 19:04:13

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

### 3. AI-Native Context (The "Insight")
> **Goal**: 最大化 AI 对项目的理解能力，降低 Context Window 消耗，提供"上帝视角"。

*   [ ] **Dependency Graph (_DEPS.md)**:
    *   [x] 实现 `deps.py` 的 AST Import 提取。
    *   [x] 生成模块依赖关系图 (Module Dependency Graph)，帮助 AI 理解修改的影响范围。
*   [ ] **Symbol Index (_SYMBOLS.md)**:
    *   [ ] 生成全项目符号表 (Classes/Functions/Signatures)，提供 API 速查手册。
    *   [ ] 提取 Docstring Summary，建立语义索引。
*   [ ] **Data Registry (_DATA.md)**:
    *   [ ] 集中展示所有 `@dataclass`, `TypedDict` 和 `Enum` 定义。
    *   [ ] 强化 "Logic as Data" 原则的可视化。

## @PLAN: Niki-docAI Evolution (Phase 6)
> @CONTEXT: Optimization Proposals | @TAGS: @VISION @ARCH @TECH

### 1. @TECH: Deep Semantic Analysis (LSP)
> **Goal**: `Regex` -> `LSP` => **Deep Context**
- **Ref**: `Regex` (Current) -> `Symbol Name` (Shallow)
- **New**: `LSP Server` -> `Signature` + `DocString` + `CallGraph`
- **Flow**: `Source` -> `LSP` >> `_AI.md` (`@API` Detail)
- **Value**: `@API` now contains `FUN Name(Args) -> Ret`, minimizing `Context Loss`.

### 2. @ARCH: Architecture Guard (Linter)
> **Goal**: `Passive Recorder` -> `Active Police`
- **Ref**: `_DEPS.md` (Current) -> `Visual Graph` (Passive)
- **New**: `_RULES.md` defines `!RULE` (Constraints)
- **Syntax**: `Client` !-> `Engine::Core` (Ban Dependency)
- **Op**: `ndoc verify` ? `Violation` => `[ARCH_ERROR]` Alert


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
*   🔵 **TODO** [src/ndoc/flows/verify_flow.py:38](src/ndoc/flows/verify_flow.py#L38): Implement deeper rule verification
*   🔵 **TODO** [vendors/tree-sitter-dart/grammar.js:42](vendors/tree-sitter-dart/grammar.js#L42): general things to add
*   🔵 **TODO** [vendors/tree-sitter-dart/grammar.js:858](vendors/tree-sitter-dart/grammar.js#L858): The spec says optional but it breaks tests, and I'm not sure in a good way.
*   🔵 **TODO** [vendors/tree-sitter-dart/grammar.js:1218](vendors/tree-sitter-dart/grammar.js#L1218): add rethrow statement.
*   🔵 **TODO** [vendors/tree-sitter-dart/grammar.js:1923](vendors/tree-sitter-dart/grammar.js#L1923): This should only work with native?
*   🔵 **TODO** [vendors/tree-sitter-dart/grammar.js:2007](vendors/tree-sitter-dart/grammar.js#L2007): add in the 'late' keyword from the informal draft spec:
*   🔵 **TODO** [vendors/tree-sitter-dart/grammar.js:2833](vendors/tree-sitter-dart/grammar.js#L2833): add support for triple-slash comments as a special category.
*   🔵 **TODO** [vendors/tree-sitter-dart/test/corpus/flutter.txt:53](vendors/tree-sitter-dart/test/corpus/flutter.txt#L53): implement build
<!-- NIKI_TODO_END -->
