# ARCHITECTURAL RULES (架构守则)

> **Context**: 项目全局通用的开发规范、原则和禁忌。
> **Tags**: `@RULE` `@CONST`
<!-- NIKI_VERSION: 0.1.0 -->

## 1. Core Philosophy (核心哲学)
*   **Single Source of Truth**: 确保文档与代码的一致性。
*   **Configuration First (配置优先)**: 所有硬编码逻辑必须移至 `ndoc.toml`，确保用户可控。
*   **Defense Against Overwrite (防御性写入)**: 工具生成的文档必须尊重用户的修改。如果文件已存在且包含用户内容，工具应采用增量更新或跳过，绝不强制覆盖（除非用户显式要求重置）。
*   **AI-Centric (AI 为中心)**: 架构设计应优先考虑 AI 的理解效率（如上下文压缩、确定性规则）。

## 2. Coding Standards (代码规范)
*   (Add your coding standards here...)

## 3. Toolchain (工具链)
*   所有文档变更建议通过 `ndoc` 工具链验证。
