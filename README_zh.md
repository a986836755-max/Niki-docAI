# Niki-docAI 2.0 (重生版)

> **面向 AI 辅助开发的上下文运维与架构守护工具**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
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

---

## 4. 安装与快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-org/nk_doc_ai.git
cd nk_doc_ai

# 安装（推荐）
python -m pip install .
```

首次运行会自动在 `~/.ndoc/bin` 生成 shim 并尝试写入 PATH。

如果安装后找不到 `ndoc`，可以使用模块入口：

```bash
python -m ndoc all
```

### 自包含发行包

```bash
tools/packaging/build.sh
```

输出：

- `dist/ndoc` (macOS/Linux)
- `dist/ndoc.exe` (Windows)

### 快速开始

**1. 初始化 (Initialize)**

```bash
# 初始化项目（生成配置和语法手册）
ndoc init
```

**2. 生成上下文 (Generate Context)**

```bash
# 一键生成/更新所有文档 (架构 + 上下文 + 状态 + 依赖)
ndoc all
```

**3. AI 辅助 (AI Assistance)**

```bash
# 为特定文件生成 AI 提示词（智能检索模式）
ndoc prompt src/main.py --focus

# 查看文件的高密度骨架
ndoc skeleton src/utils.py
```

**4. 架构治理 (Architecture Governance)**

```bash
# 检查架构违规
ndoc check

# 检测循环依赖
ndoc deps
# 查看特定模块的局部依赖
ndoc deps src/core

# 分析当前变更的影响范围
ndoc impact
```

---

## 5. 配置 (Configuration)

通过 `_RULES.md` 配置你的项目：

```markdown
## 扫描规则 (Scanning Rules)
- `!IGNORE`: node_modules, dist, build, .git

## 架构规则 (Architecture Rules)
- `!RULE`: @LAYER(core) CANNOT_IMPORT @LAYER(ui)
- `!RULE`: @FORBID(hardcoded_paths)
```

---

## 6. 支持的语言

内置 Tree-sitter 解析器，支持多语言混合项目：
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
