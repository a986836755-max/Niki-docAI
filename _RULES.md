# PROJECT RULES (规范总则)

> **Context**: 项目全局通用的开发规范、原则和禁忌。
> **Tags**: `@RULE` `@CONST`
<!-- NIKI_VERSION: 0.1.0 -->

## 1. Core Philosophy (核心哲学)
*   **Data Oriented Design (DOD)**: 数据先行，逻辑跟随。Entity 只是 ID，Component 只是数据 Struct，System 只是函数。
*   **Single Source of Truth**: 状态唯一。UI 只是数据的投影 (Projection)，不是数据本身。
*   **Narrow Interface**: 跨语言边界 (FFI) 必须足够窄。只允许传递序列化数据 (Buffer) 或基础类型 (Primitive)。

## 2. Coding Standards (代码规范)
*   **C++**: C++20 Standard. No Exceptions in Core Loop.
*   **Dart**: Strict Linting. Null Safety.
*   **Naming**: 
    *   Structs/Classes: `PascalCase`
    *   Variables/Functions: `snake_case` (C++), `camelCase` (Dart)
    *   Files: `snake_case`

## 3. Toolchain (工具链)
*   所有文档变更必须通过 `ndoc` 工具链验证。
*   新模块创建必须使用 `ndoc create`。
