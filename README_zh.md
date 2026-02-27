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

## 3. 解决方案 (五大核心领域)

Niki-docAI 将其能力划分为五个战略领域，以实现自动化的“上下文运维”：

### 3.1 🗺️ 全景导航 (Panoramic Navigation)
*在不挤爆上下文窗口的前提下，给 AI 一张项目的完整地图。*

*   **上下文地图 (`ndoc map`)**:
    生成项目结构的高层导航地图，包含**精确的行号引用**（如 `file.py#L1`），帮助 AI 瞬间定位文件。
*   **AI 上下文 (`ndoc context`)**:
    生成代码库的递归式、Token 优化的摘要，包含文件描述、符号定义和关系。
*   **骨架提取 (`ndoc skeleton`)**:
    从源文件中提取高密度的代码骨架（仅接口/签名），在保留结构信息的同时减少高达 70% 的 Token 消耗。
*   **LSP 查询 (`ndoc lsp`)**:
    提供命令行接口查询语言服务器协议（LSP）的符号和定义，实现精确的代码导航。

### 3.2 🏗️ 架构治理 (Architecture Governance)
*确保项目结构保持整洁并遵守既定规则。*

*   **架构视图 (`ndoc arch`)**:
    可视化高层架构、技术栈和模块边界。
*   **依赖分析 (`ndoc deps`)**:
    使用 Tarjan 算法检测并报告循环依赖，并生成 Mermaid 图表进行可视化。
*   **约束检查 (`ndoc check`)**:
    基于 `_RULES.md` 中的 `!RULE` 语法强制执行架构规则（如分层约束），防止“架构漂移”。
*   **影响分析 (`ndoc impact`)**:
    分析 Git 变更，智能预测当前修改可能影响的下游模块和测试用例。
*   **质量门禁 (`ndoc lint`)**:
    集成项目特定的 Lint 命令封装，确保在提交前符合代码质量标准。

### 3.3 🧠 知识管理 (Knowledge Management)
*捕获并召回项目知识、决策和经验教训。*

*   **记忆归档 (`ndoc archive`)**:
    使用向量数据库 Embedding 存储和检索长期的项目记忆。
*   **短期记忆 (Hippocampus)**:
    管理活跃的上下文和最近的交互，以在编码会话期间保持连续性。
*   **架构决策记录 (`ndoc adr`)**:
    自动从注释中提取 `@DECISION` 标签到 `_ADR.md`，创建架构选择的活历史。
*   **数据字典 (`ndoc data`)**:
    自动提取数据模式（`dataclass`, `TypedDict`, `Enum`）到 `_DATA.md`，建立集中的数据注册表。
*   **项目统计 (`ndoc stats`)**:
    追踪代码指标（行数、复杂度）并扫描 `TODO` 项以监控项目健康状况。
*   **智能提示 (`ndoc prompt`)**:
    为 AI 生成优化后的 Prompt，结合了规则、上下文摘要和相关的 API 参考。

### 3.4 ⚡ 环境效能 (Environment & Efficiency)
*保持开发环境健康，工具随时待命。*

*   **系统诊断 (`ndoc doctor`)**:
    全面的环境检查，包括操作系统、Python 版本、依赖项和 Tree-sitter 语言绑定。
*   **项目初始化 (`ndoc init`)**:
    使用标准配置文件（`_RULES.md`, `.ndoc.toml`）初始化新的 Niki-docAI 项目。
*   **上下文注入 (`ndoc inject`)**:
    向源文件注入上下文标记和头部信息，辅助 AI 理解。
*   **能力检查 (`ndoc caps`)**:
    验证已安装的能力和动态语言支持（例如，检查 Rust 解析器是否已加载）。
*   **清理维护 (`ndoc clean`)**:
    移除生成的临时文件和缓存，保持工作区整洁。

### 3.5 🚀 高级扩展 (Advanced Extensions)
*通过强大的集成和自动化扩展 Niki-docAI。*

*   **监听模式 (`ndoc watch`)**:
    一个守护进程，监控文件变更并实时自动更新文档和索引。
*   **IDE 服务 (`ndoc server`)**:
    语言服务器协议 (LSP) 实现，为 IDE 扩展提供 Niki-docAI 能力支持。
*   **插件 SDK**:
    健壮的 SDK (`ndoc.sdk.interfaces`)，允许开发者为特定语言或框架创建自定义插件。
*   **全量领航 (`ndoc all` / `ndoc pilot`)**:
    运行完整的分析流水线，一次性生成所有文档和报告。

---

## 4. 使用指南 (命令行接口)

Niki-docAI 提供了丰富的命令集。以下是最常用的操作：

### 🚀 核心工作流
```bash
# 初始化新项目
ndoc init

# 运行全量分析 (生成所有文档)
ndoc all
# 别名: ndoc pilot

# 启动监听模式 (文件变更自动更新)
ndoc watch
```

### 🗺️ 导航与上下文
```bash
# 仅更新结构地图 (_MAP.md)
ndoc map

# 更新详细的 AI 上下文 (_AI.md)
ndoc context

# 为特定文件生成骨架 (用于粘贴给 AI)
ndoc skeleton src/main.py

# 查询 LSP 符号定义
ndoc lsp MyClass
```

### 🏗️ 架构与质量
```bash
# 检查架构规则违规 (!RULE)
ndoc check

# 可视化依赖并检测循环
ndoc deps

# 生成高层架构视图
ndoc arch

# 分析当前 Git 变更的影响
ndoc impact
```

### 🧠 知识与提示
```bash
# 为特定文件生成优化后的 Prompt
ndoc prompt src/core/logic.py --focus

# 语义搜索代码库 (需要向量数据库)
ndoc search "how does authentication work?"

# 更新项目统计和 TODO 追踪
ndoc stats
```

### ⚡ 维护
```bash
# 检查环境健康状况
ndoc doctor

# 清理生成的制品
ndoc clean

# 自我更新 (git pull)
ndoc update
```

---

## 5. 集成指南 (如何接入你的项目)

Niki-docAI 由两部分组成：**核心工具 (Python CLI)** 和 **IDE 扩展**。

### 步骤 1: 安装核心工具 (Python CLI)

`ndoc` CLI 是整个系统的核心，必须安装在你的环境中。

**选项 A: 源码安装 (Beta 版推荐)**
```bash
# 克隆仓库
git clone https://github.com/niki/nk_doc_ai.git
cd nk_doc_ai

# 安装包
pip install .
```

**选项 B: 通过 Pip 安装 (未来支持)**
```bash
pip install niki-doc-ai
```

### 步骤 2: 安装 IDE 扩展 (VS Code)

(即将推出)
