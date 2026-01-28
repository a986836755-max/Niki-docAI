# PROJECT GLOSSARY (术语表)

> **Context**: 统一项目中的特定术语定义，防止歧义。
> **Tags**: `@DEF` `@LANGUAGE`
<!-- NIKI_VERSION: 0.1.0 -->

## A. Core Concepts (核心概念)
*   **Entity (实体)**: 在 C++ 侧特指 `entt::entity` (uint32_t Handle)。它只是一个 ID，不是对象。
*   **Component (组件)**: 纯数据结构 (Struct)，不包含逻辑。例如 `TransformComponent`, `HealthComponent`。
*   **System (系统)**: 无状态的逻辑处理单元。例如 `PhysicsSystem` 遍历所有 `Position` + `Velocity` 组件进行更新。

## B. Architecture (架构)
*   **Snapshot (快照)**: 一帧或多帧的完整/部分状态数据包 (FlatBuffer)。
*   **Command (指令)**: Client 发送给 Engine 的操作请求 (FlexBuffer/FlatBuffer)。
