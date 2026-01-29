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
