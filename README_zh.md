# Niki-docAI 2.0 (重生版)

> **面向 AI 辅助开发的上下文运维与架构守护工具**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)]()

[**中文文档**](README_zh.md) | [**English**](README.md)

---

## 1. 什么是 Niki-docAI?

**Niki-docAI** 是一个智能工具链，旨在架起 **人类工程师** 与 **AI 编程助手**（如 Copilot, Cursor, Trae）之间的桥梁。

它将文档视为一个 **“上下文数据库”**，具备以下特性：
1.  **自动化生成**：源自代码，确保是“单一事实来源” (Single Source of Truth)。
2.  **结构化优化**：专为 AI 上下文窗口优化（节省 Token）。
3.  **严格验证**：基于架构规则进行验证（减少幻觉）。

---

## 2. 解决什么问题?

在 AI 辅助编程时代，我们面临三大痛点：

*   **上下文缺失 (Context Loss)**:
    AI 助手往往因为只能看到少数打开的文件，而无法理解大型代码库的“全局全貌”。

*   **幻觉 (Hallucination)**:
    当文档过期时，AI 会基于错误的假设生成代码。

*   **维护负担 (Maintenance Burden)**:
    人类讨厌写文档。手动维护架构图和依赖列表既痛苦又容易出错。

---

## 3. 解决方案

Niki-docAI 提供了一套工具来自动化“上下文运维”：

### 核心特性

*   **自动化上下文地图 (`_MAP.md`)**:
    自动生成项目结构的导航地图，并包含**精确的行号引用**（如 `file.py#L1`），帮助 AI 瞬间定位文件。

*   **架构守护 (`ndoc check`)**:
    **[2.0 新功能]** 基于 `_RULES.md` 中的 `!RULE` 强制执行架构规则（如分层约束）。防止“架构漂移”。

*   **循环依赖检测 (`ndoc deps`)**:
    **[2.0 新功能]** 利用 Tarjan 算法自动检测并报告代码库中的循环依赖。

*   **智能检索 (`ndoc prompt --focus`)**:
    **[2.0 新功能]** 利用 **向量数据库 (ChromaDB)** 进行语义检索，让 AI 能“回忆”起未打开的相关代码。

*   **全链路影响分析 (`ndoc impact`)**:
    **[2.0 新功能]** 分析 Git 变更，智能预测受影响的模块和测试用例。

*   **语义骨架 (`ndoc skeleton`)**:
    **[2.0 新功能]** 生成高密度的代码骨架（仅接口），降低 70% 的 Token 消耗。

*   **数据注册表 (`ndoc data`)**:
    **[2.0 新功能]** 自动提取 `dataclass`, `TypedDict`, `Enum`, `struct`, 和 `model` 定义到 `_DATA.md`，建立统一数据字典。

*   **质量门禁 (`ndoc lint` / `ndoc typecheck`)**:
    **[2.0 新功能]** 集成 `_RULES.md` 中定义的质量检查命令，提供统一的调用接口。

*   **经验固化 (`ndoc lesson`)**:
    **[2.0 新功能]** 从代码注释中提取 `@LESSON` 标签到 `_LESSONS.md`，形成项目知识库，避免重复犯错。

*   **系统诊断 (`ndoc doctor`)**:
    **[2.0 新功能]** 全面的环境检查，包括 OS、Python 版本、依赖项、Tree-sitter 语言绑定和项目配置健康状况。

---

## 4. 🚀 一键安装指南

### Windows (PowerShell)
```powershell
.\install.ps1
```

### Linux / macOS
```bash
chmod +x install.sh
./install.sh
```

此脚本会自动执行以下操作：
1.  检测并使用合适的 Python 版本。
2.  安装 `ndoc` 核心工具。
3.  检测 VS Code 并自动安装 Niki-docAI 插件。

---

## 5. 快速开始

### 初始化项目

1.  在 VS Code 中打开你的目标项目。
2.  打开终端运行：
    ```bash
    ndoc init
    ```
    这将创建 `.ndoc` 配置目录和必要文件：
    *   `_RULES.md`: 架构规则与 Lint 命令。
    *   `_SYNTAX.md`: 文档语法指南。

### 生成上下文

运行全量生成命令来索引你的代码库：

```bash
ndoc all
```

你将在项目根目录看到生成的文件：
*   `_MAP.md`: 项目结构地图。
*   `_ARCH.md`: 架构概览。
*   `_DEPS.md`: 依赖关系图。
*   `_AI.md`: 各目录的递归上下文文件。

### 配置规则 (可选)

编辑 `_RULES.md` 定义你的项目特定约束：

```markdown
## !RULE
<!-- 示例：强制分层 -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
```

然后运行 `ndoc check` 来验证代码是否符合规则。

---

## 6. 开发 (吃狗粮)

要开发 Niki-docAI 本身：

1.  在 VS Code 中打开本仓库。
2.  运行 `ndoc init` (我们吃自己的狗粮！)。
3.  使用 "Launch Extension" 调试配置来测试 VS Code 插件。

---

## License

MIT
