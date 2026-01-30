# Niki-docAI

> **Context Ops & Architecture Guard for AI-Assisted Development**
> **面向 AI 辅助开发的上下文运维与架构守护工具**

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

*   **Automated Context Map (`_MAP.md`)**:
    Automatically generates a navigational map of your project structure with **Precise Line References** (e.g., `file.py#L1`), helping AI find the right files instantly.
    自动生成项目结构的导航地图，并包含**精确的行号引用**，帮助 AI 瞬间定位文件。

*   **Dependency Graph (`_DEPS.md`)**:
    Scans your code to generate real-time dependency graphs (Mermaid), ensuring the architecture view is always synced with reality.
    扫描代码生成实时的依赖关系图，确保架构视图永远与现实同步。

*   **Project Statistics (`_STATS.md`)**:
    Provides insights into project scale, doc/code ratio, and AI context coverage.
    提供项目规模、文档/代码比率及 AI 上下文覆盖率的统计洞察。

*   **Task Tracking (`_NEXT.md`)**:
    Aggregates TODOs and FIXMEs from source code into a prioritized roadmap.
    自动聚合源码中的 TODO/FIXME，形成优先级明确的开发路线图。

*   **Recursive Context (`_AI.md`)**:
    Generates local context summaries in every directory, creating a fractal knowledge base.
    在每个目录下生成局部上下文摘要，构建分形的知识库。

### Key Features (关键特性)
1. **Configurability (可配置化)**:
    Unified config via `_RULES.md` (Documentation as Configuration).
    通过 `_RULES.md` 进行统一配置（文档即配置）。
    - *Reference `_RULES.md` for `!IGNORE`, `!INCLUDE`, and special keywords like `@AGGREGATE` and `@CHECK_IGNORE`.*
    - *参阅 `_RULES.md` 了解 `!IGNORE`, `!INCLUDE` 以及 `@AGGREGATE`, `@CHECK_IGNORE` 等特殊关键字。*

2. **Priority Weighting (优先级加权)**:
    Use `@CORE` in file headers or docstrings to elevate importance for AI focus.
    在文件头或文档注释中使用 `@CORE` 提升关键文件的 AI 关注度优先级。

3. **Visibility Awareness (可见性感知)**:
    Automatically captures `public`/`private`/`protected` modifiers and naming conventions (`_`, `#`, Go Uppercase) to distinguish API boundaries.
    自动捕捉 `public`/`private`/`protected` 修饰符及命名规范（`_`, `#`, Go 大写），清晰界定 API 边界。

4. **Persistence (持久性)**:
    Respects user edits; never overwrites creative content.
    尊重用户修改；绝不覆盖用户的创作内容。

5. **Automation (自动化)**:
    One-command maintenance (`ndoc all`).
    一键自动化维护 (`ndoc all`)。

6. **Recursive Deep Scan (递归深度扫描)**:
    Deep dependency analysis across multi-language manifests and source code.
    跨多语言配置清单与源码的深度依赖分析。

7. **Multi-Language Support (多语言支持)**:
    Built-in Tree-sitter integration for polyglot codebases.
    内置 Tree-sitter 集成，支持多语言混合代码库。

### Supported Languages (支持的语言)
*   **Python** (`.py`) - AST, Imports & Visibility
*   **Java** (`.java`) - AST, Packages & Visibility (New!)
*   **C/C++** (`.cpp`, `.c`, `.h`, `.hpp`) - AST & Includes
*   **JavaScript/TypeScript** (`.js`, `.ts`, `.jsx`, `.tsx`) - AST, Imports & Private Fields (#)
*   **Go** (`.go`) - AST, Imports & Exported Symbols
*   **Rust** (`.rs`) - AST, Imports & Visibility
*   **Dart** (`.dart`) - AST & Imports (pubspec.yaml)
*   **C#** (`.cs`, `.csproj`) - AST & Usings (PackageReference)
*   **CMake** (`.cmake`, `CMakeLists.txt`) - FetchContent & find_package
*   **Manifests**: `requirements.txt`, `pyproject.toml`, `package.json`, `pubspec.yaml`, `CMakeLists.txt`, `.csproj`

---

## 4. Vision (未来愿景)

We believe that **Documentation is the API for AI Agents**.

Niki-docAI aims to become the standard **Protocol** for how projects expose their internal structure to AI. In the future, we plan to support:

*   **Semantic Search Indexing**: Pre-computed vector embeddings for the codebase.
*   **Active Architectural Linter**: Preventing "Architecture Drift" before code is committed.
*   **Deeper Semantic Analysis**: LSP Integration for cross-file references and precise call graphs.

我们相信 **文档是 AI Agent 的 API**。Niki-docAI 旨在成为项目向 AI 暴露其内部结构的标准 **协议**。在未来，我们计划支持：

*   **语义搜索索引**：为代码库预计算向量嵌入 (Vector Embeddings)。
*   **主动架构 Linter**：在代码提交前防止“架构漂移” (Architecture Drift)。
*   **深度语义分析**：通过 LSP 集成，实现跨文件引用分析和精准调用图。

---

## 5. Installation & Quick Start (安装与快速开始)

### Installation (安装)

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/your-org/nk_doc_ai.git
cd nk_doc_ai

# Install / 安装
pip install .

# For development (Editable mode) / 开发模式安装
pip install -e .
```

### Quick Start (快速开始)

**1. Basic Usage (基础用法)**

```bash
# Initialize Niki-docAI (Create _RULES.md, _SYNTAX.md)
# 初始化项目（生成配置和语法手册）
ndoc init

# Generate/Update ALL documentation (Map, Context, Tech, Todo, Deps)
# 生成/更新所有文档
ndoc all

# Start Watch Mode (Auto-update on file change)
# 启动守护进程（文件变更时自动更新）
ndoc watch
```

**2. Maintenance & Diagnostics (维护与诊断)**

```bash
# Update Niki-docAI to the latest version
# 更新 Niki-docAI 到最新版本
ndoc update

# View Project Statistics (File count, Token usage, Context coverage)
# 查看项目统计（文件数、Token 估算、上下文覆盖率）
ndoc stats

# Verify documentation artifacts and rules
# 验证文档完整性与规则合规性
ndoc verify

# Diagnose environment and configuration health
# 诊断环境与配置健康度
ndoc doctor
```

**⚠️ Safety Operations (安全操作与警告)**

```bash
# Clean/Reset generated documentation artifacts
# 清理/重置生成的文档
# ⚠️ WARNING: Deletes ALL _AI.md, _MAP.md, etc. recursively!
# ⚠️ 警告：这将递归删除所有的 _AI.md, _MAP.md 等生成文件！
ndoc clean
# Use with target to limit scope:
# ndoc clean src/

# Force Initialize
# 强制初始化
# ⚠️ WARNING: Overwrites _RULES.md and _SYNTAX.md!
# ⚠️ 警告：这将覆盖现有的 _RULES.md 和 _SYNTAX.md 配置！
ndoc init --force
```

**3. Advanced: Granular Updates (高级：单独更新)**

```bash
ndoc map      # Update Project Map (_MAP.md)
ndoc context  # Update Recursive Context (_AI.md)
ndoc todo     # Scan Todos (_NEXT.md)
ndoc deps     # Update Dependency Graph (_DEPS.md)
ndoc tech     # Update Tech Stack (_TECH.md)
```
