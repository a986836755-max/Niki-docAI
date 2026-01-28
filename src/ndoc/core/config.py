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
- [ExampleComponent](components/example_component.ext): Description.

### Systems
- [ExampleSystem](systems/example_system.ext): Description.

## 3. Constraints (!RULE)
- !RULE: (Add constraint here)

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
```
// Example usage
```
"""

COMPONENT_TEMPLATE = """// Template for component
// namespace {module_name}
// struct ExampleComponent {{ ... }}
"""

SYSTEM_H_TEMPLATE = """// Template for system header
// namespace {module_name}
// class ExampleSystem {{ ... }}
"""

SYSTEM_CPP_TEMPLATE = """// Template for system implementation
// namespace {module_name}
// void ExampleSystem::update() {{ ... }}
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
*   **Single Source of Truth**: 确保文档与代码的一致性。
*   (Add your core philosophy here...)

## 2. Coding Standards (代码规范)
*   (Add your coding standards here...)

## 3. Toolchain (工具链)
*   所有文档变更建议通过 `ndoc` 工具链验证。
"""

# Glossary Template
GLOSSARY_TEMPLATE = """# PROJECT GLOSSARY (术语表)

> **Context**: 统一项目中的特定术语定义，防止歧义。
> **Tags**: `@DEF` `@LANGUAGE`
<!-- NIKI_VERSION: {version} -->

## A. Core Concepts (核心概念)
*   (Add your core concepts here...)

## B. Architecture (架构)
*   (Add your architecture terms here...)
"""

# Tech Stack Knowledge Base (for dynamic generation)
TECH_KNOWLEDGE_BASE = {
    # Languages
    "c++": {"name": "C++", "category": "1. Core Languages", "desc": "System Programming Language"},
    "c": {"name": "C", "category": "1. Core Languages", "desc": "System Programming Language"},
    "dart": {"name": "Dart", "category": "1. Core Languages", "desc": "Client/UI Language"},
    "python": {"name": "Python", "category": "1. Core Languages", "desc": "Scripting Language"},
    "rust": {"name": "Rust", "category": "1. Core Languages", "desc": "Systems Programming"},
    "lua": {"name": "Lua", "category": "1. Core Languages", "desc": "Scripting"},
    "javascript": {"name": "JavaScript", "category": "1. Core Languages", "desc": "Web/Scripting"},
    "typescript": {"name": "TypeScript", "category": "1. Core Languages", "desc": "Web/Scripting"},
    "go": {"name": "Go", "category": "1. Core Languages", "desc": "Cloud/System Language"},
    "java": {"name": "Java", "category": "1. Core Languages", "desc": "Enterprise/Android Language"},
    "kotlin": {"name": "Kotlin", "category": "1. Core Languages", "desc": "Android/JVM Language"},
    "swift": {"name": "Swift", "category": "1. Core Languages", "desc": "iOS/macOS Language"},

    # Common Libs (Examples)
    "entt": {"name": "EnTT", "category": "2. Core Libraries", "desc": "ECS Framework"},
    "flatbuffers": {"name": "FlatBuffers", "category": "2. Core Libraries", "desc": "Serialization"},
    "spdlog": {"name": "spdlog", "category": "2. Core Libraries", "desc": "Logging"},
    "catch2": {"name": "Catch2", "category": "2. Core Libraries", "desc": "Unit Testing"},
    "fmt": {"name": "fmt", "category": "2. Core Libraries", "desc": "Formatting"},
    
    # Frameworks
    "flutter": {"name": "Flutter", "category": "3. Frameworks", "desc": "UI Toolkit"},
    "react": {"name": "React", "category": "3. Frameworks", "desc": "Web UI Library"},
    "vue": {"name": "Vue", "category": "3. Frameworks", "desc": "Web UI Framework"},
    "django": {"name": "Django", "category": "3. Frameworks", "desc": "Web Framework"},
    "flask": {"name": "Flask", "category": "3. Frameworks", "desc": "Micro Web Framework"},
    
    # Tools
    "cmake": {"name": "CMake", "category": "4. Build Tools", "desc": "Build System Generator"},
    "gradle": {"name": "Gradle", "category": "4. Build Tools", "desc": "Build Automation"},
    "maven": {"name": "Maven", "category": "4. Build Tools", "desc": "Build Automation"},
    "cargo": {"name": "Cargo", "category": "4. Build Tools", "desc": "Rust Package Manager"},
    "ninja": {"name": "Ninja", "category": "4. Build Tools", "desc": "Build System"},
    "make": {"name": "Make", "category": "4. Build Tools", "desc": "Build Automation"},
}

TECH_HEADER_TEMPLATE = """# TECHNOLOGY STACK (技术栈版本锁定)

> **Context**: 明确锁定的技术版本清单，防止兼容性问题。
> **Tags**: `@TECH` `@VERSION`
<!-- NIKI_VERSION: {version} -->

"""

# Memory Template
MEMORY_TEMPLATE = """# PROJECT MEMORY (关键决策记录)

> **Context**: 记录项目历史上的关键决策、教训和路径选择 (ADR - Architecture Decision Records)。
> **Tags**: `@MEMORY` `@HISTORY`
<!-- NIKI_VERSION: {version} -->

## 1. Active Decisions (生效决策)
*   [ADR-001] (Title)
    *   **Context**: (Why we made this decision?)
    *   **Decision**: (What we decided?)
    *   **Consequences**: (What are the trade-offs?)

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

## 1. Module Dependency Graph
> Generated by `ndoc graph` based on analysis.

```mermaid
{mermaid_graph}
```

## 2. Analysis
*   **Nodes**: Modules found in source directories.
*   **Edges**: `A --> B` means A depends on B.
"""

# Next Steps Template
NEXT_STEP_TEMPLATE = """# PROJECT NEXT STEPS (规划与待办)

> **Context**: 项目的下一步计划、待办事项和路线图。
> **Tags**: `@PLAN` `@TODO`
<!-- NIKI_VERSION: {version} -->

## 1. High Priority (高优先级)
*   (Add high priority tasks here...)

## 2. Backlog (待办池)
*   (Add backlog items here...)
"""
