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
    Automatically generates a navigational map of your project structure, helping AI find the right files instantly.
    自动生成项目结构的导航地图，帮助 AI 瞬间找到正确的文件。

*   **Living Architecture (`_ARCH.md`)**:
    Scans your code to generate real-time dependency graphs (Mermaid), ensuring the architecture view is always synced with reality.
    扫描代码生成实时的依赖关系图，确保架构视图永远与现实同步。

*   **Defensive Documentation (防御性文档)**:
    Users' manual insights are preserved, while the tool automates the tedious parts (file lists, tech stacks).
    保留用户的手动洞察，同时工具自动化处理繁琐的部分（文件列表、技术栈）。

### Key Features (关键特性)
1. **Configurability (可配置化)**: Unified config via `ndoc.toml`. (通过 `ndoc.toml` 进行统一配置)
2. **Persistence (持久性)**: Respects user edits; never overwrites creative content. (尊重用户修改，绝不覆盖创作内容)
3. **Automation (自动化)**: One-command maintenance (`ndoc map`, `ndoc graph`, `ndoc tech`). (一键维护)

---

## 4. Vision (未来愿景)

We believe that **Documentation is the API for AI Agents**.

Niki-docAI aims to become the standard **Protocol** for how projects expose their internal structure to AI. In the future, we plan to support:

*   **Semantic Search Indexing**: Pre-computed vector embeddings for the codebase.
*   **Active Architectural Linter**: Preventing "Architecture Drift" before code is committed.
*   **Universal Language Support**: Expanding beyond Python/C++ to any language via LSP integration.

我们相信 **文档是 AI Agent 的 API**。Niki-docAI 旨在成为项目向 AI 暴露其内部结构的标准 **协议**。在未来，我们计划支持：

*   **语义搜索索引**：为代码库预计算向量嵌入 (Vector Embeddings)。
*   **主动架构 Linter**：在代码提交前防止“架构漂移” (Architecture Drift)。
*   **通用语言支持**：通过 LSP 集成，将支持扩展到 Python/C++ 以外的任何语言。

---

## 5. Installation & Quick Start (安装与快速开始)

```bash
# Install in editable mode / 以编辑模式安装
pip install -e packages/nk_doc_ai
```

### Quick Start
```bash
ndoc all                # Run all update flows (执行所有更新流程)
ndoc watch              # Start daemon to auto-update on file changes (启动守护进程自动更新)
```

For detailed usage, check the [Detailed Usage](#6-detailed-usage--详细使用说明) section below.

---

## 6. Detailed Usage (详细使用说明)

### 1. Core Commands (核心命令)

Manually trigger updates for specific context files.
手动触发特定上下文文件的更新。

```bash
ndoc map      # Scan directory structure and update _MAP.md / 扫描目录结构并更新 _MAP.md
ndoc tech     # Scan dependencies and update _TECH.md / 扫描依赖并更新 _TECH.md
ndoc context  # Update _AI.md and other context files / 更新 _AI.md 等上下文文件
ndoc todo     # Scan code TODOs and update _NEXT.md / 扫描代码 TODO 并更新 _NEXT.md
ndoc all      # Run all of the above / 执行以上所有命令
```

### 2. Automation (自动化)

```bash
ndoc watch    # Monitor file changes and auto-update relevant docs / 监听文件变更并自动更新相关文档
```

### 3. Planned Commands (计划中命令)

*   `ndoc init`: Initialize project structure (初始化项目结构)
*   `ndoc verify`: Architecture verification (架构验证)
*   `ndoc graph`: Dependency visualization (依赖可视化)

---

## CI/CD Integration / 持续集成

Run `ndoc verify` in your pipeline with standard formats.
在流水线中以标准格式运行 `ndoc verify`。

```bash
# JSON output for dashboards / 输出 JSON 供仪表盘使用
ndoc verify --format=json

# JUnit output for Jenkins/GitLab / 输出 JUnit 格式供 CI 使用
ndoc verify --format=junit > report.xml
```

## Docker Usage / Docker 使用

Run without installation via Docker.
通过 Docker 直接运行。

```bash
# Build image / 构建镜像
docker build -t ndoc .

# Run verification / 运行验证
docker run --rm -v $(pwd):/app ndoc verify
```
