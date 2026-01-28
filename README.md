# Niki-docAI

> **Context Ops & Architecture Guard**  
> **上下文运维与架构守护工具**

**Niki-docAI** is an intelligent toolchain designed to enforce **Architecture Consistency** and maintain "Living Documentation" for any software project. It bridges the gap between Code (Reality) and Documentation (Knowledge), ensuring that architecture constraints are not just written, but verified.

**Niki-docAI** 是一个智能工具链，旨在强制执行 **架构一致性** 并维护软件项目的“活文档”。它架起了代码（现实）与文档（知识）之间的桥梁，确保架构约束不仅停留在纸面上，而是得到实际验证。

---

## Core Philosophy / 核心哲学

*   **Single Source of Truth (单一事实来源)**:  
    Documentation should be generated from or verified against code.  
    文档应由代码生成，或与代码进行一致性验证。

*   **Architecture as Code (架构即代码)**:  
    Project rules (Isolation, FFI barriers) are checked via static analysis.  
    项目规则（如隔离、FFI 边界）通过静态分析进行检查。

*   **Context Aware (上下文感知)**:  
    Auto-detects tech stack, generates dependency graphs, and maps project structure.  
    自动检测技术栈，生成依赖图，并映射项目结构。

---

## Installation / 安装

```bash
# Install in editable mode / 以编辑模式安装
pip install -e packages/nk_doc_ai
```

---

## Usage / 使用说明

### 1. Initialization (项目初始化)

Start by initializing the documentation meta-files (`_RULES.md`, `_TECH.md`, etc.).  
首先初始化文档元文件（如 `_RULES.md`, `_TECH.md` 等）。

```bash
ndoc init               # Initialize meta files if missing / 初始化缺失的元文件
ndoc init --reset-meta  # Force reset global meta files / 强制重置全局元文件
ndoc init --reset-all   # Force reset all meta and _AI.md files recursively / 强制递归重置所有元文件和 _AI.md
ndoc init --reset-path <path> # Reset _AI.md in specific path / 重置指定路径下的 _AI.md
```

### 2. Context Management (上下文管理)

Keep your project's high-level context up to date.  
保持项目的高层上下文处于最新状态。

```bash
ndoc tech update        # Scan dependencies and update _TECH.md / 扫描依赖并更新 _TECH.md
ndoc map update         # Scan directory structure and update _MAP.md / 扫描目录结构并更新 _MAP.md
ndoc log "Title" words  # Append a decision record to _MEMORY.md / 向 _MEMORY.md 追加决策记录
```

### 3. Documentation Automation (文档自动化)

Tools to maintain living documentation.  
用于维护“活文档”的工具。

```bash
ndoc docs init <path>   # Create _AI.md in a specific directory / 在指定目录创建 _AI.md
ndoc docs init --all    # Recursively create _AI.md in all subdirectories / 递归在所有子目录创建 _AI.md
ndoc docs audit         # Check if _AI.md files are out of sync with code / 检查 _AI.md 文件是否与代码不同步
ndoc docs audit --hook <files> # Run as pre-commit hook / 作为 pre-commit 钩子运行
ndoc docs update        # Update _AI.md files with latest code summaries / 用最新的代码摘要更新 _AI.md 文件
ndoc link               # Auto-link glossary terms in markdown files / 自动链接 Markdown 文件中的术语
ndoc fix                # Attempt to auto-fix missing documentation or bad links / 尝试自动修复缺失的文档或错误链接
```

### 4. Architecture Guard (架构守护)

Ensure the project adheres to defined rules.  
确保项目遵守已定义的规则。

```bash
ndoc verify             # Run static analysis to verify architecture rules / 运行静态分析以验证架构规则
ndoc graph              # Generate and display module dependency graph (Mermaid) / 生成并显示模块依赖图 (Mermaid)
ndoc doctor             # Check toolchain health and environment / 检查工具链健康状况和环境
```

### 5. Development Helpers (开发辅助)

Helpers for common development tasks.  
常用开发任务的辅助工具。

```bash
ndoc module create <name> # Scaffold a new engine module (Standard Structure) / 创建新的引擎模块脚手架（标准结构）
ndoc build                # Trigger project build (via CMake/Script) / 触发项目构建（通过 CMake/脚本）
ndoc test                 # Run tests and update documentation with results / 运行测试并用结果更新文档
```
