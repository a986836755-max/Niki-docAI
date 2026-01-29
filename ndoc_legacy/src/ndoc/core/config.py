# Core Configuration for Niki Context Ops
# This file defines the default configuration for the Niki toolchain.
# Projects can override these values in a local configuration file (e.g. niki_config.py).

import os
import re
import tomli
from pathlib import Path
from ndoc.base import console

# --- Version Info ---
TOOLCHAIN_VERSION = "0.1.0"
VERSION_MARKER_TEMPLATE = "<!-- NIKI_VERSION: {version} -->"
VERSION_MARKER_REGEX = re.compile(r"<!-- NIKI_VERSION: ([\d\.]+) -->")

# --- Default Configuration ---
# These can be overridden by ndoc.toml

# Directories to ignore during scanning
DEFAULT_IGNORE_DIRS = {'.git', '.vs', '.vscode', 'build', 'out', '__pycache__', '.dart_tool', '.idea', 'venv', 'env', 'node_modules'}

# Common Directory Patterns for Smart Inference
DEFAULT_DIR_PATTERNS = {
    'src': 'Source Code Root (源代码根目录)',
    'lib': 'Library Root (库文件根目录)',
    'include': 'Public Headers (公共头文件)',
    'bin': 'Binary Executables (可执行文件)',
    'tests': 'Test Suites (测试套件)',
    'test': 'Test Suites (测试套件)',
    'docs': 'Project Documentation (项目文档)',
    'doc': 'Project Documentation (项目文档)',
    'tools': 'Dev Tools & Scripts (开发工具与脚本)',
    'scripts': 'Dev Tools & Scripts (开发工具与脚本)',
    'utils': 'Shared Utilities (通用工具)',
    'common': 'Shared Utilities (通用工具)',
    'core': 'Core Logic (核心逻辑)',
    'features': 'Feature Modules (功能模块)',
    'api': 'Public API Definitions (接口定义)',
    'assets': 'Static Assets (静态资源)',
    'config': 'Configuration Files (配置文件)',
    'examples': 'Usage Examples (示例代码)',
    'generated': 'Auto-generated Code (自动生成代码)',
}

# Global Config State
IGNORE_DIRS = set(DEFAULT_IGNORE_DIRS)
COMMON_DIR_PATTERNS = dict(DEFAULT_DIR_PATTERNS)
PROJECT_RULES = {}
PROJECT_LAYERS = []

# !RULE: Configuration must be loaded from ndoc.toml, not hardcoded.
def load_config(root: Path):
    """
    Loads configuration from ndoc.toml in the project root.
    Updates global config variables.
    """
    global IGNORE_DIRS, COMMON_DIR_PATTERNS, PROJECT_RULES, PROJECT_LAYERS
    
    config_path = root / "ndoc.toml"
    if not config_path.exists():
        return

    try:
        with open(config_path, "rb") as f:
            data = tomli.load(f)

        # 1. Load Ignore Dirs
        # [project]
        # ignore = ["dist", "tmp"]
        if "project" in data and "ignore" in data["project"]:
            user_ignores = set(data["project"]["ignore"])
            IGNORE_DIRS.update(user_ignores)

        # 2. Load Directory Patterns (Contexts)
        # [context]
        # "my_folder" = "My Custom Folder"
        if "context" in data:
            COMMON_DIR_PATTERNS.update(data["context"])
            
        # 3. Load Rules
        # [rules]
        if "rules" in data:
            PROJECT_RULES = data["rules"]

        # 4. Load Layers
        # [layers]
        if "layers" in data:
            PROJECT_LAYERS = data["layers"]

    except Exception as e:
        console.warning(f"Failed to load ndoc.toml: {e}")


# File extensions to consider as "Code" for audit
CODE_EXTENSIONS = {'.cpp', '.h', '.hpp', '.c', '.cc', '.dart', '.py'}

# --- Markdown Markers ---
# Tags required in _AI.md files
REQUIRED_TAGS = ['@CONTEXT', '!RULE']

# Tag used to ignore paths in _AI.md
IGNORE_TAG = '@CHECK_IGNORE'

# Tag used to aggregate subdirectories
AGGREGATE_TAG = '@AGGREGATE'

# Pattern for the MAP section in markdown files
MAP_HEADER_PATTERN = re.compile(r'^\s*<!-- NIKI_MAP_START -->')
NEXT_HEADER_PATTERN = re.compile(r'^\s*<!-- NIKI_MAP_END -->')

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
AI_TEMPLATE = """# {module_name}
> @CONTEXT: {domain_tag} | @TAGS: @OVERVIEW @ARCH
<!-- NIKI_VERSION: {version} -->

## @OVERVIEW

## @ARCH
<!-- NIKI_AUTO_DOC_START -->
<!-- (File list merged into @MAP section) -->
<!-- NIKI_AUTO_DOC_END -->

## !RULE
- !RULE: 

## @MAP
<!-- NIKI_MAP_START -->
- [README.md](README.md)
<!-- NIKI_MAP_END -->

## @CONFIG
<!-- @CHECK_IGNORE: generated/ -->
"""

README_TEMPLATE = """# {module_name}

## @VISION

## @USAGE
```
// Example
```
"""

COMPONENT_TEMPLATE = """// Component
// namespace {module_name}
// struct ExampleComponent {{ ... }}
"""

SYSTEM_H_TEMPLATE = """// System Header
// namespace {module_name}
// class ExampleSystem {{ ... }}
"""

SYSTEM_CPP_TEMPLATE = """// System Impl
// namespace {module_name}
// void ExampleSystem::update() {{ ... }}
"""

# Syntax Template
SYNTAX_TEMPLATE = """# PROJECT SYNTAX
> @CONTEXT: DSL Definition | @TAGS: @SYNTAX @OP
<!-- NIKI_VERSION: {version} -->

## @OP
| Op | Meaning |
| :--- | :--- |
| `->` | **Flow**: Logic -> Comp |
| `<-` | **Read**: Sys <- Comp |
| `=>` | **Map**: ID => Sprite |
| `>>` | **Move**: Ptr >> Sys |
| `?` | **Check**: Dirty? |
| `+` | **Mix**: Pos + Vel |
| `!` | **Ban**: !Draw |

## @TAGS
> Global Tag Definitions. AI MUST follow these semantics.

### Structural
- `@DOMAIN`: **Scope**. Boundary/Domain.
- `@MODULE`: **Module**. Independent unit.
- `@API`: **Public**. Public Interface.
- `@AGGREGATE`: **Recursive**. Include subdirs.
- `@ARCH`: **Architecture**. File list/Graph.
- `@MAP`: **Navigation**. Links/Structure.
- `@TREE`: **Directory Tree**. Project hierarchy.
- `@GRAPH`: **Dependency Graph**. Visual relationships.
- `@INDEX`: **Index**. Cross-reference.

### Constraint
- `!RULE`: **Constraint**. Mandatory rule.
- `!CONST`: **Invariant**. Immutable fact.

### Semantic
- `@OVERVIEW`: **Summary**. Core responsibility/Why it exists.
- `@VISION`: **Vision**. Long-term goal.
- `@USAGE`: **Usage**. Examples/How-to.
- `@FLOW`: **Process**. Sequence/Data flow.
- `@STATE`: **State**. State machine/Variables.
- `@EVENT`: **Event**. Emitted/Handled events.
- `@DEF`: **Term**. Definition/Concept.
- `@TERM`: **Glossary**. Term definition.
- `@TECH`: **Technology**. Stack info.
- `@STACK`: **Stack**. Dependencies/Versions.
- `@ANALYSIS`: **Analysis**. Insights/Metrics.

### Evolutionary
- `!TODO`: **Debt**. Known issue.
- `@PLAN`: **Roadmap**. Future plan.
- `@BACKLOG`: **Backlog**. Future tasks.
- `@MEMORY`: **ADR**. Decision record.
- `@ADR`: **Decision**. Record of decisions.
- `@DEPRECATED`: **No**. Do not use.
- `@EXPERIMENTAL`: **WIP**. Unstable.
- `@LEGACY`: **Legacy**. Old code.

### Meta
- `@META`: **Metadata**. File attributes.
- `@CONFIG`: **Configuration**. Settings/Rules.
- `@CHECK_IGNORE`: **Audit Ignore**.
- `@CONTEXT`: **Context**. Scope definition.
- `@TAGS`: **Tag Def**. Tag dictionary.
- `@SYNTAX`: **Syntax**. DSL rules.
- `@OP`: **Operator**. DSL operators.
- `@TOOL`: **Tooling**. CLI instructions.

### @DISCOVERED
> Auto-discovered tags from file headers.
- `@UNKNOWN`: **Unknown**. Placeholder.
"""

# --- Meta File Templates ---

NDOC_TOML_TEMPLATE = """# Niki Doc AI Configuration
# Generated by ndoc init

# [rules]
# [[rules.python]]
# id = "!RULE:EXAMPLE"
# pattern = 'forbidden_pattern'
# message = "Don't use forbidden pattern."

# [layers]
# [[layers]]
# name = "core"
# path = "src/core"
# deny = ["features"]
"""

RULES_TEMPLATE = """# PROJECT RULES
> @CONTEXT: Dev Standards | @TAGS: !RULE !CONST
<!-- NIKI_VERSION: {version} -->

## !RULE
*   **Single Source of Truth**: Document matches Code.
*   (Add rules...)

## @TOOL
*   Use `ndoc` for verification.
"""

# Glossary Template
GLOSSARY_TEMPLATE = """# PROJECT GLOSSARY
> @CONTEXT: Terms | @TAGS: @DEF @TERM
<!-- NIKI_VERSION: {version} -->

## @DEF
*   (Add terms...)
"""



# Tech Stack Knowledge Base (for dynamic generation)
TECH_KNOWLEDGE_BASE = {
    # Languages
    "c++": {"name": "C++", "category": "Core Languages", "desc": "System Programming"},
    "c": {"name": "C", "category": "Core Languages", "desc": "System Programming"},
    "dart": {"name": "Dart", "category": "Core Languages", "desc": "Client/UI"},
    "python": {"name": "Python", "category": "Core Languages", "desc": "Scripting"},
    "rust": {"name": "Rust", "category": "Core Languages", "desc": "Systems"},
    "lua": {"name": "Lua", "category": "Core Languages", "desc": "Scripting"},
    "javascript": {"name": "JavaScript", "category": "Core Languages", "desc": "Web"},
    "typescript": {"name": "TypeScript", "category": "Core Languages", "desc": "Web"},
    "go": {"name": "Go", "category": "Core Languages", "desc": "Cloud"},
    "java": {"name": "Java", "category": "Core Languages", "desc": "Enterprise"},
    "kotlin": {"name": "Kotlin", "category": "Core Languages", "desc": "Android"},
    "swift": {"name": "Swift", "category": "Core Languages", "desc": "iOS"},

    # Common Libs (Examples)
    "entt": {"name": "EnTT", "category": "Core Libraries", "desc": "ECS"},
    "flatbuffers": {"name": "FlatBuffers", "category": "Core Libraries", "desc": "Serialization"},
    "spdlog": {"name": "spdlog", "category": "Core Libraries", "desc": "Logging"},
    "catch2": {"name": "Catch2", "category": "Core Libraries", "desc": "Testing"},
    "fmt": {"name": "fmt", "category": "Core Libraries", "desc": "Formatting"},
    
    # Frameworks
    "flutter": {"name": "Flutter", "category": "Frameworks", "desc": "UI"},
    "react": {"name": "React", "category": "Frameworks", "desc": "Web UI"},
    "vue": {"name": "Vue", "category": "Frameworks", "desc": "Web UI"},
    "django": {"name": "Django", "category": "Frameworks", "desc": "Web Framework"},
    "flask": {"name": "Flask", "category": "Frameworks", "desc": "Micro Web"},
    
    # Tools
    "cmake": {"name": "CMake", "category": "Build Tools", "desc": "Build System"},
    "gradle": {"name": "Gradle", "category": "Build Tools", "desc": "Build Automation"},
    "maven": {"name": "Maven", "category": "Build Tools", "desc": "Build Automation"},
    "cargo": {"name": "Cargo", "category": "Build Tools", "desc": "Rust Pkg Mgr"},
    "ninja": {"name": "Ninja", "category": "Build Tools", "desc": "Build System"},
    "make": {"name": "Make", "category": "Build Tools", "desc": "Build Automation"},
}

TECH_HEADER_TEMPLATE = """# PROJECT STACK
> @CONTEXT: Locked Versions | @TAGS: @TECH @STACK
<!-- NIKI_VERSION: {version} -->

"""

# Memory Template
MEMORY_TEMPLATE = """# PROJECT MEMORY
> @CONTEXT: ADR/History | @TAGS: @MEMORY @ADR
<!-- NIKI_VERSION: {version} -->

## @ADR
*   [ADR-001] (Title)
    *   **Context**: ...
    *   **Decision**: ...
    *   **Result**: ...

## @DEPRECATED
*   (None)
"""

# Map Template
MAP_TEMPLATE = """# PROJECT MAP
> @CONTEXT: Navigation | @TAGS: @MAP @INDEX
<!-- NIKI_VERSION: {version} -->

## @META
- [_SYNTAX.md](_SYNTAX.md)
- [_RULES.md](_RULES.md)
- [_GLOSSARY.md](_GLOSSARY.md)
- [_TECH.md](_TECH.md)
- [_MEMORY.md](_MEMORY.md)
- [_ARCH.md](_ARCH.md)
- [_NEXT.md](_NEXT.md)

## @TREE
<!-- NIKI_MAP_START -->
<!-- NIKI_MAP_END -->
"""

# Arch Template (New)
ARCH_TEMPLATE = """# PROJECT ARCHITECTURE
> @CONTEXT: Dependency Graph | @TAGS: @ARCH @GRAPH
<!-- NIKI_VERSION: {version} -->

## @GRAPH
> Generated by `ndoc graph`.

<!-- NIKI_AUTO_DOC_START -->
```mermaid
{mermaid_graph}
```
<!-- NIKI_AUTO_DOC_END -->

## @ANALYSIS
*   **Nodes**: Modules.
*   **Edges**: Dependencies (`A --> B`).
"""

# Next Steps Template
NEXT_STEP_TEMPLATE = """# PROJECT ROADMAP
> @CONTEXT: Evolution | @TAGS: @PLAN @TODO
<!-- NIKI_VERSION: {version} -->

## @PLAN
*   (High Priority...)

## @BACKLOG
*   (Todo...)
"""
