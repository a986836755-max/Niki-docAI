# PROJECT MEMORY (关键决策记录)

> **Context**: 记录项目历史上的关键决策、教训和路径选择 (ADR - Architecture Decision Records)。
> **Tags**: `@MEMORY` `@HISTORY`
<!-- NIKI_VERSION: 0.1.0 -->

## 1. Active Decisions (生效决策)
*   [ADR-001] (Title)
    *   **Context**: (Why we made this decision?)
    *   **Decision**: (What we decided?)
    *   **Consequences**: (What are the trade-offs?)

## 2. Deprecated Paths (已废弃路径)
*   (None)

## 2026-01-29
*   **[Plan] Refactor Plan: Unified Configuration**: Plan to refactor codebase to eliminate hardcoding. 1. Unify config loading in core/config.py. 2. Remove hardcoded paths in tech.py and verify.py. 3. Ensure all features respect ndoc.toml settings (IGNORE_DIRS, scan paths).
*   **[Philosophy] Core Philosophy: AI-Centric & User Control**: Recorded the core design philosophy: 1. Solve AI pain points (Context Window, Hallucination) via compressed indexes (_MAP, _ARCH) and deterministic constraints (!RULE). 2. Empower users via Configurable (ndoc.toml), Persistent (no overwrite), and Automated workflows.
