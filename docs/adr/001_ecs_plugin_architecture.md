# ADR-001: 基于 ECS 内核与插件化架构 (ECS-Based Kernel & Plugin Architecture)

> **状态 (Status)**: 已接受 (Accepted)
> **日期 (Date)**: 2026-02-27
> **背景 (Context)**: 从脚本集合工具转型为 AI 原生代码分析平台

## 1. 背景与问题 (Context & Problem)
当前的 Niki-docAI 架构遵循单体式的 "Flow -> Core" 模式。
随着我们需要支持更多编程语言、更深度的依赖分析（图谱）以及 AI 特性（向量化），我们面临以下挑战：
- **耦合严重**: 业务逻辑 (Flows) 与文件 IO、解析逻辑紧密耦合。
- **性能瓶颈**: 基于对象的全量文件建模在大规模代码库中开销巨大。
- **扩展困难**: 新增一种语言或分析类型往往需要修改核心代码。

## 2. 决策 (Decision)
我们将系统重构为 **内核 (Kernel) + 插件 (Plugin)** 架构，并引入 **ECS (Entity-Component-System)** 和 **DOD (面向数据设计)** 理念。

### 2.1. 核心内核 (The Kernel: Data-Oriented Core)
内核充当代码库的内存数据库。

*   **实体 (Entity)**: 代表 `File` (文件)、`Symbol` (符号) 或 `Module` (模块)。本质上只是一个唯一的 ID。
*   **组件 (Component)**: 附加在实体上的纯数据结构。
    *   `SyntaxComponent`: 原始源码、AST 句柄。
    *   `GraphComponent`: 依赖关系邻接表。
    *   `VectorComponent`: Embedding 向量数据。
    *   `MetaComponent`: 标签、TODO、Docstrings。
*   **系统 (System)**: 查询特定组件并转换数据的逻辑单元。

### 2.2. 插件架构 (Plugin Architecture)
所有的业务价值都通过实现标准化接口的插件来交付。

*   **感知插件 (Sensor Plugins)**: 负责“读”。例如 `LanguageParser` (语法解析), `VectorEmbedder` (向量化)。
*   **行动插件 (Action Plugins)**: 负责“写”。例如 `DocGenerator` (文档生成), `CodeInjector` (代码注入)。
*   **业务流插件 (Flows as Plugins)**: 现有的业务流 (`arch`, `status`) 将重写为查询内核数据的插件。

### 2.3. 技术选型 (Technology Stack)
为了实现高性能与可扩展性，我们引入以下核心库：

*   **数据存储 (Data Store)**: **SQLite**
    *   作为 ECS 的后端存储，提供高效的关系查询能力 (e.g. "查找所有包含 TODO 的 Python 文件")。
*   **向量引擎 (Vector Engine)**: **ChromaDB**
    *   负责向量数据的存储与检索，作为内核的认知层核心。
*   **数据模型 (Data Modeling)**: **Pydantic v2**
    *   利用 Rust 内核提供极速的序列化/反序列化能力，定义 Component Schema。
*   **插件系统 (Plugin System)**: **Pluggy**
    *   采用 pytest 的核心插件库，提供强大的 Hook 机制，实现业务解耦。

## 3. 迁移策略 (Migration Strategy: Strangler Fig)
我们不会一次性重写所有代码，而是采用“绞杀植物”模式。

1.  **阶段一：地基 (Foundation)**: 建立 `ndoc.kernel` 和 `ndoc.sdk`。定义 `Entity/Component` 模型与 `Pluggy` 钩子。
2.  **阶段二：试点 (Pilot)**: 将 **Status Flow** 移植到新架构，作为第一个插件。
3.  **阶段三：双轨运行 (Dual Run)**: 新旧内核并存运行。
4.  **阶段四：切换 (Cutover)**: 逐步移植剩余 Flow，最终废弃 `ndoc.core`。

## 4. 收益 (Benefits)
- **解耦 (Decoupling)**: 插件仅与内核的数据 Schema 交互，插件之间互不感知。
- **性能 (Performance)**: 基于组件的批量处理 (DOD) 比遍历对象树更快。
- **AI 原生 (AI-Ready)**: 向量组件成为一等公民，原生支持 RAG (检索增强生成) 场景。
