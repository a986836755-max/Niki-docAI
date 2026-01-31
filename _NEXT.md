# PROJECT ROADMAP
> 最后更新 (Last Updated): 2026-01-31 11:29:48

## @CURRENT (Phase 5: Niki-ALM & Automation)

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

## @HISTORY

#### Archived on 2026-01-30
### 2. Live Context Daemon (Optimization)
*   [x] **File Watcher**: 实现高效的文件变更监听 (Watchdog)。
*   [x] **增量文档更新 (Incremental Update)**:
    *   [x] 实现基于 MD5 的 `FileCache` 原子能力。
    *   [x] 集成 `scanner.scan_file` 到所有核心 Flow，避免重复解析。
    *   [x] 优化 `daemon.py` 以支持局部更新。

### 3. AI-Native Context (The "Insight")
> **Goal**: 最大化 AI 对项目的理解能力，降低 Context Window 消耗，提供"上帝视角"。

*   [x] **依赖图完善 (_DEPS.md)**:
    *   [x] 增强 `deps.py` 的 AST Import 提取，支持子模块识别。
    *   [x] 优化 `deps_flow.py` 的 Mermaid 图生成逻辑。
*   [x] **Symbol Index (_SYMBOLS.md)**:
    *   [x] 扫描全局公有符号（类、函数、常量）。
    *   [x] 生成全局符号索引文档，支持跨文件跳转（IDE支持）。
    *   [x] 集成到 `ndoc all` 和 `ndoc symbols`。
*   [x] **数据注册中心 (_DATA.md)**:
    *   [x] 集中展示所有 `@dataclass`, `TypedDict` 和 `Enum` 定义。
    *   [x] 修复 AST 属性丢失问题 (decorators, bases)。

### 1. Niki-ALM (Project Lifecycle Engine)
> **Goal**: 实现 "Idea -> Plan -> Code -> Done -> Memory" 的自动化闭环管理。

*   [x] **Plan & Split (The Planner)**:
    *   [x] 实现 `ndoc plan "Objective"` 命令，通过 LLM 自动将一句话目标拆解为 `_NEXT.md` 中的结构化任务。
*   [x] **Task Tracking (The Tracker)**:
    *   [x] 实现 `Todo Flow`：自动扫描代码中的 `TODO/FIXME`，聚合到 `_NEXT.md`底部。
    *   [x] #scanner-enhancement: 增强 `Scanner`：识别代码完成状态，自动更新 `_NEXT.md` 中的 Checkbox (关联 Task ID)。
*   [x] **归档与记忆 (_MEMORY.md)**:
    *   [x] 实现 `archive_flow.py`，自动归档已完成的任务。
    *   [x] 遵循交付即更新规则。

### 4. @ARCH: Modular Language Support (Refactoring)
> **Goal**: 将不同语言的 API 抓取配置（SCM 查询与解析规则）从核心引擎中剥离，实现解耦与独立管理。

*   [x] **Standardize Language Definitions**:
    *   定义 `langs/` 目录下的统一接口：`SCM_QUERY`, `EXTENSIONS`, `METADATA`。
*   [x] **Dynamic Registry Implementation**:
    *   在 `ast.py` 中实现动态加载机制，自动扫描并注册 `src/ndoc/atoms/langs/` 下的配置。
*   [x] **Independent SCM Files**:
    *   将复杂的 SCM 查询移至独立的 `.scm` 文件 (或通过 Python 定义实现解耦)。
*   [x] **Rule-based Visibility & Parsing**:
    *   将可见性判定、Docstring 提取、签名格式化逻辑全部下放到各语言定义中，实现彻底的 Logic as Data。

## @PLAN: Niki-docAI Evolution (Phase 6)
> @CONTEXT: Optimization Proposals | @TAGS: @VISION @ARCH @TECH

### Phase 2 & 3: Parsing & Foundation
*   [x] **Testing Strategy**: 建立了 `tests/` 和 `pytest` 体系。
*   [x] **Tree-sitter Integration**: 完成了基于 AST 的代码解析（Class, Function, Decorator, Signature）。
*   [x] **Scanner Migration**: 移除了代码解析的正则依赖，确立了混合解析策略。
*   [x] **Dogfooding**: 通过了项目自测。

## @PLAN (Future)


#### Archived on 2026-01-30

#### Archived on 2026-01-30

#### Archived on 2026-01-30

#### Archived on 2026-01-30

#### Archived on 2026-01-30

#### Archived on 2026-01-30

#### Archived on 2026-01-30