# Niki-docAI 项目功能落地状态报告

> **最后更新 (Last Updated)**: 2026-02-27
> **版本 (Version)**: 2.0.0-beta

本文档详细记录了 `PROJECT_SUMMARY.md` 中列出的核心功能的实际落地与实现情况。经过对源码的全面审查，我们对每个功能的状态进行了诚实的评级。

---

## 1. 落地状态概览 (Status Overview)

| 领域 (Domain) | 功能点 (Feature) | 状态 (Status) | 备注 (Remarks) |
| :--- | :--- | :--- | :--- |
| **全景导航** | 结构映射 (`map`) | ✅ **已实现** | 基于 ECS Plugin，支持 Tree 视图与 Docstring 摘要。 |
| | 上下文生成 (`context`) | ✅ **已实现** | 核心功能，基于 ECS Plugin，支持递归与详细符号解析。 |
| | 骨架提取 (`skeleton`) | ✅ **已实现** | 独立的 AST 遍历逻辑，支持多语言函数体压缩。 |
| | LSP 查询 (`lsp`) | ✅ **已实现** | CLI 命令功能完整，底层使用 `LSPService` 进行内存索引。 |
| **架构治理** | 架构视图 (`arch`) | ✅ **已实现** | 支持多语言 BOM 解析与技术栈统计。 |
| | 依赖分析 (`deps`) | ✅ **已实现** | 集成 Mermaid 可视化与 Tarjan 环路检测算法。 |
| | 约束检查 (`check`) | ✅ **已实现** | 支持 `!RULE` 语法与 AST 匹配。 |
| | 影响分析 (`impact`) | ⚠️ **部分实现** | 实现了 Git Diff 提取，但依赖图反向遍历逻辑依赖非标准 Context 字段，稳定性待验证。 |
| | 测试映射 (Test Map) | ⚠️ **实验性** | `TestUsageMapper` 已存在但未集成到主流程，目前仅作为独立模块。 |
| | 质量门禁 (`lint`) | ✅ **已实现** | 封装 Shell 命令，功能简单稳定。 |
| **知识管理** | 记忆归档 (`archive`) | ✅ **已实现** | 支持 VectorDB 嵌入与多种标记提取。 |
| | 短期记忆 (Hippocampus)| ✅ **已实现** | 核心逻辑已在 `brain/hippocampus.py` 中实现。 |
| | 统计追踪 (`stats`) | ✅ **已实现** | 集成代码度量与 TODO 扫描 (`StatusPlugin`)。 |
| | 架构决策 (`adr`) | ✅ **已实现** | 独立的 Report Plugin，基于扫描器提取 `@DECISION`。 |
| | 数据字典 (`data`) | ⚠️ **部分实现** | 插件仅支持 Python (dataclass/Enum/TypedDict)，其他语言支持缺失。 |
| | 语义检索 (`search`) | ⚠️ **部分实现** | 依赖 VectorDB，目前仅实现了查询封装，缺乏独立的索引更新流水线。 |
| | 智能提示 (`prompt`) | ✅ **已实现** | `PromptService` 集成了规则、上下文摘要和相关 API 推荐。 |
| **环境效能** | 能力自检 (`caps`) | ✅ **已实现** | 支持 Tree-sitter 动态加载。 |
| | 环境诊断 (`doctor`) | ✅ **已实现** | 覆盖 OS、Python、依赖检查。 |
| | 初始化 (`init`) | ✅ **已实现** | 生成标准配置文件。 |
| | 清理维护 (`clean`) | ✅ **已实现** | 基础文件清理。 |
| | 上下文注入 (`inject`) | ✅ **已实现** | 支持头部注入。 |
| **高级扩展** | 守护模式 (`watch`) | ✅ **已实现** | 基于 `watchdog` 的去抖动监听，集成海马体。 |
| | IDE 服务 (`server`) | ✅ **基本实现** | 基于 `pygls` 实现，支持 `textDocument/didOpen` 等基础事件，具备基本的校验能力。 |
| | VS Code 插件 | 📅 **计划中** | 代码库中有 `editors/vscode` 目录，但尚未构建发布。 |
| | Plugin SDK | ✅ **已实现** | `ndoc.sdk.interfaces` 定义清晰，已用于所有内部插件。 |
| | 全量领航 (`pilot`) | ✅ **已实现** | `ndoc all` 别名。 |

---

## 2. 详细实现评估 (Detailed Assessment)

### 2.1 落地情况较好的功能 (Well Implemented)

这些功能是项目的基石，代码结构清晰（ECS 架构），逻辑完整，且经过了多次重构优化。

1.  **Context & Map (`ndoc context`, `ndoc map`)**
    *   **实现**: 完全基于 ECS Kernel -> Sensor -> Action 流水线。
    *   **优势**: 解耦了文件扫描与报告生成，支持递归与缓存，性能优异。
    *   **代码**: `ndoc.plugins.context_report`, `ndoc.plugins.map_report`。

2.  **Deps & Arch (`ndoc deps`, `ndoc arch`)**
    *   **实现**: 拥有强大的依赖解析器（支持 Python AST, package.json, go.mod 等）和可视化渲染引擎。
    *   **优势**: Mermaid 图表生成逻辑 (`views.mermaid`) 非常成熟，支持分层展示。
    *   **代码**: `ndoc.plugins.deps_report`, `ndoc.plugins.arch_report`。

3.  **Skeleton Generation (`ndoc skeleton`)**
    *   **实现**: `ndoc.parsing.ast.skeleton` 模块通过 Tree-sitter 遍历 AST，精准识别函数/类体并进行压缩。
    *   **优势**: 逻辑独立且健壮，支持多语言扩展。

4.  **Prompt Generation (`ndoc prompt`)**
    *   **实现**: `PromptService` 能够综合文件内容、全局规则、语法摘要和依赖信息生成高质量的 AI 上下文。
    *   **优势**: 真正体现了 "Context Ops" 的价值，为 AI 提供了结构化的输入。

### 2.2 尚需完善的功能 (Needs Improvement)

这些功能核心逻辑已存在，但在完整性、多语言支持或集成度上仍有欠缺。

1.  **Impact Analysis**
    *   **现状**: `ImpactService` 能够获取 Git 变更，但其反向依赖分析依赖于 `context.graph` 这一非标准字段（应使用 `GraphComponent`），且目前仅支持静态 Import 分析。
    *   **改进**: 需要规范化图数据访问，并引入更深层的调用图分析（Call Graph）。

2.  **Data Schema (`ndoc data`)**
    *   **现状**: `DataSchemaPlugin` 目前硬编码了 Python 的 `dataclass`, `Enum`, `TypedDict` 识别逻辑，缺乏对 TypeScript Interface 或 Rust Struct 的支持。
    *   **改进**: 需要将语言特定的数据结构提取逻辑下沉到 `langs` 模块。

3.  **Semantic Search (`ndoc search`)**
    *   **现状**: `SearchService` 只是 `VectorDB` 的查询包装器，它假设 `ndoc all` 已经完成了索引构建。缺乏独立的、增量的索引更新命令。
    *   **改进**: 将 Embedding 过程解耦为独立的 `IndexingPlugin`。

4.  **LSP Server (`ndoc server`)**
    *   **现状**: `ndoc.lsp_server` 基于 `pygls` 实现了基础服务，能够响应 `didSave` 并运行 `scanner`。但目前仅发布 Diagnostics，缺乏 Hover, Definition 等高级特性的处理程序。
    *   **改进**: 需要实现 `textDocument/hover` 和 `textDocument/definition` 处理器，复用 `LSPService` 的逻辑。

---

## 3. 下一步计划 (Next Steps)

1.  **完善 LSP Server**: 在 `lsp_server.py` 中注册 `TEXT_DOCUMENT_HOVER` 和 `TEXT_DOCUMENT_DEFINITION` 处理器。
2.  **多语言数据解析**: 扩展 `DataSchemaPlugin` 支持 TS Interface 和 Rust Struct。
3.  **集成测试映射**: 将 `TestUsageMapper` 插件化，生成 `_TESTS.md`。
4.  **发布 VS Code 插件**: 编译并发布 `editors/vscode`。
