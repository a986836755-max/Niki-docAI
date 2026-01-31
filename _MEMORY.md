# PROJECT MEMORY
> @CONTEXT: 决策记录 | 历史 | @TAGS: @MEMORY @ADR

<!-- NIKI_VERSION: 2.0.0 -->

## @TIMELINE

### 2026-01-29: Rebirth & Paradigm Shift

#### ADR-001: Project Rebirth (项目重生)
*   **Context**: 旧版本 (Legacy) 代码基于 OOP，结构耦合度高，难以适应 "Live Context" 的自动化需求。
*   **Decision**: 
    *   执行 **Physical Isolation** (物理隔离)：旧代码移至 `ndoc_legacy`，新代码在 `src/ndoc` 从零构建。
    *   确立 **Data-Driven** (数据驱动) 为核心架构。
*   **Status**: Accepted & Executed.

#### ADR-002: Shift to DOD/FP (范式转移)
*   **Context**: OOP 的封装和状态隐藏导致了上下文的不透明和逻辑的硬编码。
*   **Decision**: 全面转向 **Data-Oriented Design (DOD)** 和 **Functional Programming (FP)**。
    *   **Logic as Data**: 业务逻辑必须提取为数据表/配置，禁止硬编码 `if-else`。
    *   **Pipeline**: 代码结构必须是 `Input -> Transform -> Output` 的纯管道。
    *   **Generic Engine**: 代码仅作为执行数据的通用引擎。
*   **Status**: Accepted & Enforced in `_RULES.md`.

#### ADR-003: Parsing Strategy Evolution (解析进化)
*   **Context**: 基于正则 (`re`) 的代码分析脆弱且无法获取语义信息。
*   **Decision**: 
    *   短期：引入 **Tree-sitter** 进行容错性 AST 解析。
    *   长期：集成 **LSP (Language Server Protocol)** 获取 IDE 级语义数据。
    *   定位：Doxygen 仅作为文档生成的参考，不再作为数据源。
*   **Status**: Executed. Tree-sitter 集成已完成 (Phase 2).

#### ADR-004: Testing Strategy Implementation (测试落地)
*   **Context**: 项目缺乏自动化测试，重构风险高。
*   **Decision**:
    *   采用 `pytest` 作为测试框架。
    *   建立 `tests/` 目录，实施分层测试：
        *   Unit Tests: 针对 `scanner` 和 `ast` 模块。
        *   Smoke Tests: 针对 `entry.py` 进行 Dogfooding 自测。
*   **Status**: Executed.

### 2026-01-31: Semantic Enrichment & LSP Integration

#### ADR-005: Enhanced Semantic Extraction (语义提取增强)
*   **Context**: 之前的注释抓取逻辑过于简单，无法处理多行合并、Python 内部字符串 (Inner Docstrings) 以及特定语言 (Dart ///) 的优化。
*   **Decision**: 
    *   重构 `scanner.py`，引入 `text_utils.py` 解耦文本清洗逻辑。
    *   支持多行行注释合并为单一 Docstring。
    *   增强 Python 语义提取：同时抓取类/函数上方的 `#` 注释和内部的 `"""` 字符串。
*   **Status**: Completed.

#### ADR-006: LSP Reference Counting (LSP 引用计数集成)
*   **Context**: 符号索引 `_SYMBOLS.md` 仅列出定义，缺乏使用热度信息。
*   **Decision**: 
    *   在 `lsp.py` 中实现轻量级全局词频统计 (Global Word Count) 作为引用计数预估。
    *   在 `symbols_flow.py` 中集成 `LSPService`，为每个公共符号自动标注引用次数。
    *   修复了 `Symbol` 对象在缓存重建过程中的路径丢失导致的 CLI 崩溃。
*   **Status**: Completed.

#### ADR-007: Dart Grammar Ambiguity Resolution (Dart 语法冲突处理)
*   **Context**: `tree-sitter-dart` 的 `relational_expression` 可选字段导致语法解析歧义。
*   **Decision**: 
    *   通过调研发现该可选字段在扁平表达式结构中存在固有冲突。
    *   移除 `TODO` 并转为正式文档说明，保持当前稳定的解析路径。
*   **Status**: Resolved by documentation update.
