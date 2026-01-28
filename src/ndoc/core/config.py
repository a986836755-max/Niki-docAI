# Core Configuration for Niki Context Ops
# This file defines the default configuration for the Niki toolchain.
# Projects can override these values in a local configuration file (e.g. niki_config.py).

import os
import re
from pathlib import Path

# --- Version Info ---
TOOLCHAIN_VERSION = "0.1.0"
VERSION_MARKER_TEMPLATE = "<!-- NIKI_VERSION: {version} -->"
VERSION_MARKER_REGEX = re.compile(r"<!-- NIKI_VERSION: ([\d\.]+) -->")

# --- Project Structure ---
# Directories to ignore during scanning
IGNORE_DIRS = {'.git', '.vs', '.vscode', 'build', 'out', '__pycache__', '.dart_tool', '.idea'}

# File extensions to consider as "Code" for audit
CODE_EXTENSIONS = {'.cpp', '.h', '.hpp', '.c', '.cc', '.dart', '.py'}

# --- Markdown Markers ---
# Tags required in _AI.md files
REQUIRED_TAGS = ['@DOMAIN', '!RULE']

# Tag used to ignore paths in _AI.md
IGNORE_TAG = '@CHECK_IGNORE'

# Pattern for the MAP section in markdown files
MAP_HEADER_PATTERN = re.compile(r'^##\s+\d*\.?\s*MAP')
NEXT_HEADER_PATTERN = re.compile(r'^##\s+')

# Markers for Auto-Generated Content
MARKER_START = "<!-- NIKI_AUTO_DOC_START -->"
MARKER_END = "<!-- NIKI_AUTO_DOC_END -->"

# --- Status Badges ---
BADGE_TEMPLATE = "![Status](https://img.shields.io/badge/Status-Verified-green)"
BADGE_REGEX = re.compile(r"!\[Status\]\(https://img\.shields\.io/badge/Status-[^\)]+\)")
VERIFIED_TEMPLATE = "**Last Verified**: {date}"
VERIFIED_REGEX = re.compile(r"\*\*Last Verified\*\*: \d{4}-\d{2}-\d{2}")

# --- Doxygen Integration ---
# Default Doxygen configuration file path relative to project root
DOXYFILE_PATH = "tools/Doxyfile.niki"
# Directory where Doxygen XML output is generated relative to project root
XML_OUTPUT_DIR = Path("build/docs/xml")

# --- Templates ---
AI_TEMPLATE = """# {module_name} Module AI Context

@DOMAIN: {domain_tag}
@STATUS: Experimental

## 1. Overview
(Describe the core responsibility of this module. Why does it exist?)

## 2. Architecture
### Components
- [ExampleComponent](components/example_component.h): Description.

### Systems
- [ExampleSystem](systems/example_system.h): Description.

## 3. Constraints (!RULE)
- !RULE: Logic must be data-driven.
- !RULE: No direct dependencies on UI.

## 4. Map
- [README.md](README.md)

## 5. Tool Config
<!-- Files/Folders exempted from document synchronization audit -->
<!-- @CHECK_IGNORE: generated/ -->
"""

README_TEMPLATE = """# {module_name} Module

## Vision
(High level vision and human-readable description)

## Usage
```cpp
// Example usage
```
"""

COMPONENT_TEMPLATE = """#pragma once
#include <entt/entt.hpp>

namespace niki::{module_name} {{

struct ExampleComponent {{
    float value;
}};

}} // namespace niki::{module_name}
"""

SYSTEM_H_TEMPLATE = """#pragma once
#include <entt/entt.hpp>

namespace niki::{module_name} {{

class ExampleSystem {{
public:
    static void update(entt::registry& registry);
}};

}} // namespace niki::{module_name}
"""

SYSTEM_CPP_TEMPLATE = """#include "example_system.h"
#include "../components/example_component.h"

namespace niki::{module_name} {{

void ExampleSystem::update(entt::registry& registry) {{
    auto view = registry.view<ExampleComponent>();
    for (auto entity : view) {{
        auto& comp = view.get<ExampleComponent>(entity);
        // Logic here
    }}
}}

}} // namespace niki::{module_name}
"""

# Syntax Template
SYNTAX_TEMPLATE = """# NIKI_DOC_SYNTAX
> **Context**: Definition of Documentation Syntax, Operators, and Tags.
> **Tags**: `@SYNTAX`
<!-- NIKI_VERSION: {version} -->

## 1. Operators (逻辑操作符)
| Op | Meaning |
| :--- | :--- |
| `->` | **Flow/Write**: Data flow or write. `Logic -> Comp` (Logic writes Comp). |
| `<-` | **Read**: Read access. `Sys <- Comp` (System reads Comp). |
| `=>` | **Map/Transform**: Mapping or transformation. `TypeID => Sprite` (Map ID to Sprite). |
| `>>` | **Move/Transfer**: Strong ownership transfer. `UniquePtr >> System`. |
| `?` | **Optional/Check**: Optional or conditional check. `Dirty?` (If Dirty). |
| `+` | **Combine**: Combination or dependency. `Pos + Vel`. |
| `!` | **Ban**: Prohibition. `!DrawCall`. |

## 2. Tags (标签)
- `@DOMAIN`: Scope/Domain definition.
- `!RULE`: Constraint definition.
- `@CHECK_IGNORE`: Ignore path for audit.
"""

# Rules Template
RULES_TEMPLATE = """# PROJECT RULES (规范总则)

> **Context**: 项目全局通用的开发规范、原则和禁忌。
> **Tags**: `@RULE` `@CONST`
<!-- NIKI_VERSION: {version} -->

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
"""

# Glossary Template
GLOSSARY_TEMPLATE = """# PROJECT GLOSSARY (术语表)

> **Context**: 统一项目中的特定术语定义，防止歧义。
> **Tags**: `@DEF` `@LANGUAGE`
<!-- NIKI_VERSION: {version} -->

## A. Core Concepts (核心概念)
*   **Entity (实体)**: 在 C++ 侧特指 `entt::entity` (uint32_t Handle)。它只是一个 ID，不是对象。
*   **Component (组件)**: 纯数据结构 (Struct)，不包含逻辑。例如 `TransformComponent`, `HealthComponent`。
*   **System (系统)**: 无状态的逻辑处理单元。例如 `PhysicsSystem` 遍历所有 `Position` + `Velocity` 组件进行更新。

## B. Architecture (架构)
*   **Snapshot (快照)**: 一帧或多帧的完整/部分状态数据包 (FlatBuffer)。
*   **Command (指令)**: Client 发送给 Engine 的操作请求 (FlexBuffer/FlatBuffer)。
"""

# Tech Stack Knowledge Base (for dynamic generation)
TECH_KNOWLEDGE_BASE = {
    # Languages
    "c++": {"name": "C++", "category": "1. Core Languages", "desc": "Standard: C++20 (Required features: `std::span`, `std::format`, `std::source_location`)"},
    "c": {"name": "C", "category": "1. Core Languages", "desc": "Legacy/Interop"},
    "dart": {"name": "Dart", "category": "1. Core Languages", "desc": "Null Safety enabled"},
    "python": {"name": "Python", "category": "1. Core Languages", "desc": "Scripts/Tools"},
    "rust": {"name": "Rust", "category": "1. Core Languages", "desc": "Systems Programming"},
    "lua": {"name": "Lua", "category": "1. Core Languages", "desc": "Scripting"},
    "javascript": {"name": "JavaScript", "category": "1. Core Languages", "desc": "Web/Scripting"},
    "typescript": {"name": "TypeScript", "category": "1. Core Languages", "desc": "Web/Scripting"},

    # Engine Libs (C++)
    "entt": {"name": "EnTT", "category": "2. Core Libraries (Engine)", "desc": "ECS Framework (Strict)"},
    "flatbuffers": {"name": "FlatBuffers", "category": "2. Core Libraries (Engine)", "desc": "Serialization"},
    "spdlog": {"name": "spdlog", "category": "2. Core Libraries (Engine)", "desc": "Logging"},
    "catch2": {"name": "Catch2", "category": "2. Core Libraries (Engine)", "desc": "Unit Testing"},
    "glm": {"name": "GLM", "category": "2. Core Libraries (Engine)", "desc": "Mathematics"},
    "fmt": {"name": "fmt", "category": "2. Core Libraries (Engine)", "desc": "Formatting"},
    
    # Client Libs (Dart/Flutter)
    "flutter": {"name": "Flutter", "category": "3. Frameworks (Client)", "desc": "UI Toolkit"},
    "ffi": {"name": "FFI", "category": "3. Frameworks (Client)", "desc": "Foreign Function Interface"},
    "dart_sdk": {"name": "Dart SDK", "category": "3. Frameworks (Client)", "desc": "Language SDK"},
    "vector_math": {"name": "Vector Math", "category": "3. Frameworks (Client)", "desc": "Mathematics"},
    "flat_buffers": {"name": "FlatBuffers (Dart)", "category": "3. Frameworks (Client)", "desc": "Serialization"},
    "cupertino_icons": {"name": "Cupertino Icons", "category": "3. Frameworks (Client)", "desc": "UI Assets"},
    
    # Tools
    "cmake": {"name": "CMake", "category": "4. Build Tools", "desc": "Build System Generator"},
    "gradle": {"name": "Gradle", "category": "4. Build Tools", "desc": "Android Build Tool"},
    "cargo": {"name": "Cargo", "category": "4. Build Tools", "desc": "Rust Package Manager"},
    "ninja": {"name": "Ninja", "category": "4. Build Tools", "desc": "Build System"},
}

TECH_HEADER_TEMPLATE = """# TECHNOLOGY STACK (技术栈版本锁定)

> **Context**: 明确锁定的技术版本清单，防止兼容性问题。
> **Tags**: `@TECH` `@VERSION`
<!-- NIKI_VERSION: {toolchain} -->

"""

# Memory Template
MEMORY_TEMPLATE = """# PROJECT MEMORY (关键决策记录)

> **Context**: 记录项目历史上的关键决策、教训和路径选择 (ADR - Architecture Decision Records)。
> **Tags**: `@MEMORY` `@HISTORY`
<!-- NIKI_VERSION: {version} -->

## 1. Active Decisions (生效决策)
*   [ADR-001] Adopt EnTT as ECS Framework.
*   [ADR-002] Use FlatBuffers for FFI boundary.
*   [ADR-003] Separate Logic/Render Loops.

## 2. Deprecated Paths (已废弃路径)
*   (None)
"""

# Map Template
MAP_TEMPLATE = """# PROJECT MAP (物理结构索引)

> **Context**: 项目文件系统的物理导航图。由 `ndoc map` 自动维护。
> **Tags**: `@MAP` `@INDEX`
<!-- NIKI_VERSION: {version} -->

## 1. Meta Files (元文件)
- [_SYNTAX.md](_SYNTAX.md): Documentation Syntax & Operators.
- [_RULES.md](_RULES.md): Global Rules & Philosophy.
- [_GLOSSARY.md](_GLOSSARY.md): Terminology.
- [_TECH.md](_TECH.md): Technology Stack & Versions.
- [_MEMORY.md](_MEMORY.md): Key Decisions (ADR).
- [_ARCH.md](_ARCH.md): Architecture Graph (Auto-generated).

## 2. Directory Structure
<!-- NIKI_MAP_START -->
<!-- NIKI_MAP_END -->
"""

# Arch Template (New)
ARCH_TEMPLATE = """# PROJECT ARCHITECTURE (架构视图)

> **Context**: 自动生成的项目依赖关系图。
> **Tags**: `@ARCH` `@GRAPH`
<!-- NIKI_VERSION: {version} -->

## 1. Engine Module Dependency Graph (C++)
> Generated by `ndoc graph` based on `#include` analysis.

```mermaid
{mermaid_graph}
```

## 2. Analysis
*   **Nodes**: Modules found in `engine/modules/`.
*   **Edges**: `A --> B` means A includes headers from B.
"""
