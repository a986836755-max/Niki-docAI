# Niki-docAI 2.0 (Rebirth)

> **Context Ops & Architecture Guard for AI-Assisted Development**  
> **面向 AI 辅助开发的上下文运维与架构守护工具**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)]()

---

## 1. What is Niki-docAI? (它是什么?)

**Niki-docAI** is an intelligent toolchain designed to bridge the gap between **Human Engineers** and **AI Coding Assistants** (like Copilot, Cursor, Trae).

It treats documentation not as static text, but as a **"Context Database"** that is:
1.  **Auto-generated** from code (Single Source of Truth).
2.  **Structurally Optimized** for AI context windows (Token efficient).
3.  **Strictly Verified** against architectural rules (Hallucination reduction).

**Niki-docAI** 是一个智能工具链，旨在架起 **人类工程师** 与 **AI 编程助手** 之间的桥梁。它将文档视为一个 **“上下文数据库”**，具备以下特性：
1.  **自动化生成**：源自代码，确保是“单一事实来源” (Single Source of Truth)。
2.  **结构化优化**：专为 AI 上下文窗口优化（节省 Token）。
3.  **严格验证**：基于架构规则进行验证（减少幻觉）。

---

## 2. The Problem (解决什么问题?)

In the era of AI-assisted coding, we face three major pain points:

*   **Context Loss (上下文缺失)**:
    AI assistants often fail to understand the "Big Picture" of a large codebase because they can only see a few open files.
    AI 助手往往因为只能看到少数打开的文件，而无法理解大型代码库的“全局全貌”。

*   **Hallucination (幻觉)**:
    When documentation is outdated, AI generates code based on wrong assumptions.
    当文档过期时，AI 会基于错误的假设生成代码。

*   **Maintenance Burden (维护负担)**:
    Humans hate writing docs. Keeping architecture diagrams and dependency lists up-to-date manually is painful and error-prone.
    人类讨厌写文档。手动维护架构图和依赖列表既痛苦又容易出错。

---

## 3. The Solution (解决方案)

Niki-docAI provides a suite of tools to automate "Context Ops":

### Core Features (核心特性)

*   **Automated Context Map (`_MAP.md`)**:
    Automatically generates a navigational map of your project structure with **Precise Line References** (e.g., `file.py#L1`), helping AI find the right files instantly.
    自动生成项目结构的导航地图，并包含**精确的行号引用**，帮助 AI 瞬间定位文件。

*   **Architecture Guard (`ndoc check`)**:
    **[NEW in 2.0]** Enforce architecture rules (e.g., Layering) defined in `_RULES.md` using `!RULE`. Prevents "Architecture Drift" before it happens.
    **[2.0 新功能]** 基于 `!RULE` 强制执行架构规则（如分层约束）。防止架构腐化。

*   **Circular Dependency Detection (`ndoc deps`)**:
    **[NEW in 2.0]** Detects and reports circular dependencies in your codebase using Tarjan's algorithm.
    **[2.0 新功能]** 自动检测并报告代码库中的循环依赖。

*   **Intelligent Retrieval (`ndoc prompt --focus`)**:
    **[NEW in 2.0]** Uses **Vector Database (ChromaDB)** to semantic search related context, enabling AI to "recall" relevant code even if it's not open.
    **[2.0 新功能]** 利用向量数据库进行语义检索，让 AI 能“回忆”起未打开的相关代码。

*   **Impact Analysis (`ndoc impact`)**:
    **[NEW in 2.0]** Analyzes Git changes to predict which modules and tests are affected.
    **[2.0 新功能]** 分析 Git 变更，智能预测受影响的模块和测试用例。

*   **Semantic Skeleton (`ndoc skeleton`)**:
    **[NEW in 2.0]** Generates high-density code skeletons (interfaces only), reducing token usage by 70%.
    **[2.0 新功能]** 生成高密度的代码骨架（仅接口），降低 70% 的 Token 消耗。

---

## 4. Installation & Quick Start (安装与快速开始)

### Installation (安装)

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/your-org/nk_doc_ai.git
cd nk_doc_ai

# Install / 安装
pip install .
```

### Quick Start (快速开始)

**1. Initialize (初始化)**

```bash
# Initialize Niki-docAI (Create _RULES.md, _SYNTAX.md)
# 初始化项目（生成配置和语法手册）
ndoc init
```

**2. Generate Context (生成上下文)**

```bash
# Generate/Update ALL documentation (Arch + Context + Status + Deps)
# 一键生成所有文档
ndoc all
```

**3. AI Assistance (AI 辅助)**

```bash
# Generate context prompt for a specific file (Smart Retrieval)
# 为特定文件生成 AI 提示词（智能检索模式）
ndoc prompt src/main.py --focus

# View high-density skeleton of a file
# 查看文件的高密度骨架
ndoc skeleton src/utils.py
```

**4. Architecture Governance (架构治理)**

```bash
# Check for architecture violations
# 检查架构违规
ndoc check

# Detect circular dependencies
# 检测循环依赖
ndoc deps

# Analyze impact of current changes
# 分析当前变更的影响范围
ndoc impact
```

---

## 5. Configuration (配置)

Configure your project via `_RULES.md`:

```markdown
## Scanning Rules
- `!IGNORE`: node_modules, dist, build, .git

## Architecture Rules
- `!RULE`: @LAYER(core) CANNOT_IMPORT @LAYER(ui)
- `!RULE`: @FORBID(hardcoded_paths)
```

---

## 6. Supported Languages (支持的语言)

Built-in Tree-sitter integration for polyglot codebases:
*   **Python** (`.py`)
*   **JavaScript/TypeScript** (`.js`, `.ts`, `.jsx`, `.tsx`)
*   **Java** (`.java`)
*   **Go** (`.go`)
*   **C/C++** (`.cpp`, `.h`)
*   **C#** (`.cs`)
*   **Rust** (`.rs`)
*   **Dart** (`.dart`)

---

*Powered by Niki-docAI Team*
