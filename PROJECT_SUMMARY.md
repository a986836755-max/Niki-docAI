# Niki-docAI 项目核心功能综述

> **Context Ops & Architecture Guard for AI-Assisted Development**
> 为 AI 辅助开发打造的上下文运维与架构守护体系。

---

## 1. 项目概述 (Introduction)

Niki-docAI (ndoc) 是一个专为 AI 辅助编程时代设计的智能工具链。它不生产给人类阅读的传统文档，而是致力于构建一个**动态的、结构化的、机器可读的“上下文数据库”**。

通过自动化的代码分析与文档生成，Niki-docAI 旨在消除人类工程师与 AI 助手（如 Copilot, Cursor, Trae）之间的信息不对称，确保 AI 在理解项目全貌、遵循架构规范的前提下进行编码。其核心理念是 **"Documentation as Code"** 和 **"Context Ops"**。

---

## 2. 核心痛点与解决方案 (The Problem & Solution)

在现代 AI 辅助开发中，我们面临三大核心挑战：

1.  **上下文丢失 (Context Loss)**：AI 往往只能看到当前打开的文件，缺乏对项目整体结构、模块依赖和设计意图的全局认知。
2.  **幻觉与假设 (Hallucination)**：当文档缺失或过时，AI 会基于错误的假设生成代码，导致架构腐化。
3.  **维护负担 (Maintenance Burden)**：人工维护架构图、依赖关系和 API 文档成本高昂且难以持续。

Niki-docAI 通过**纯 ECS (Entity-Component-System) 架构**驱动的自动化流水线，将代码库实时转化为 AI 可理解的知识图谱，从根本上解决上述问题。

---

## 3. 功能体系详解 (Functional Architecture)

我们将核心功能划分为五个领域，覆盖从编码辅助到架构治理的全生命周期。

### 3.1 领域一：全景导航与上下文构建 (Context & Navigation)
> **解决问题**：AI 的“管中窥豹”问题，提供全局视野与局部细节。

*   **项目结构映射 (`ndoc map`)**
    *   **功能特征**：生成 `_MAP.md`，以树状结构展示项目文件布局，并附带基于元数据（Docstring）的简要说明。
    *   **实现手段**：通过 `MapReportPlugin` 遍历 ECS 实体，构建轻量级目录树，包含精准的行号链接（如 `file.py#L1`），便于 AI 快速索引。
    *   **适用对象**：AI 助手（用于快速定位文件），新入职工程师（用于快速熟悉项目）。

*   **递归上下文生成 (`ndoc context`)**
    *   **功能特征**：在每个目录下生成 `_AI.md`，提供该目录的深度上下文，包括 API 签名、类/方法定义、可见性标记（PUB/PRV）及局部依赖。
    *   **实现手段**：`SyntaxAnalysisPlugin` 解析源码 AST 填充 `SymbolComponent`，`ContextReportPlugin` 渲染详细的 Markdown 描述。支持递归生成，形成分层上下文网络。
    *   **适用对象**：AI 助手（在编写具体业务逻辑时引用详细接口定义）。

*   **代码骨架提取 (`ndoc skeleton`)**
    *   **功能特征**：生成文件的高密度语义骨架（仅包含接口定义、类签名和 Docstring，去除实现细节），Token 压缩率高达 70%。
    *   **实现手段**：基于 AST（抽象语法树）遍历，保留声明节点，剔除函数体。
    *   **适用对象**：AI 助手（在上下文窗口有限时，快速理解大文件结构）。

*   **LSP 符号查询 (`ndoc lsp`)**
    *   **功能特征**：提供类似 IDE 的“跳转到定义”和“查找引用”功能，直接在 CLI 中查询符号的定义位置和引用链。
    *   **实现手段**：内置轻量级 LSP 服务，建立符号索引。
    *   **适用对象**：AI 助手（精准定位代码依赖），开发者（在无 IDE 环境下查阅代码）。

### 3.2 领域二：架构治理与质量守护 (Architecture & Quality)
> **解决问题**：架构腐化、依赖混乱与规范执行难。

*   **架构全景视图 (`ndoc arch`)**
    *   **功能特征**：生成 `_ARCH.md`，宏观展示技术栈（Languages）、物料清单（BOM/第三方依赖）及核心目录结构。
    *   **实现手段**：`ArchitectureReportPlugin` 聚合文件扩展名统计技术栈，解析 `package.json`/`requirements.txt` 等清单文件生成 BOM。
    *   **适用对象**：架构师，技术负责人在做技术选型或审计时使用。

*   **依赖可视化与环路检测 (`ndoc deps`)**
    *   **功能特征**：生成 `_DEPS.md`，包含 Mermaid 格式的依赖关系图（区分 Stable/Hub/Volatile 区域），计算不稳定性指标（Instability），并**自动检测循环依赖**。
    *   **实现手段**：`DependencyReportPlugin` 基于 `GraphComponent` 构建依赖图，应用 Tarjan 算法检测强连通分量（SCC），并使用 `views.mermaid` 渲染分层图表。
    *   **适用对象**：架构师（优化解耦），CI/CD 流水线（阻断架构劣化）。

*   **静态约束检查 (`ndoc check`)**
    *   **功能特征**：基于 `_RULES.md` 中定义的规则（如 `!RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui)`），对代码进行静态断言检查。
    *   **实现手段**：`ConstraintCheckerPlugin` 结合 AST 信息与规则引擎，扫描代码中的违规引用或模式。
    *   **适用对象**：CI/CD 流水线，代码审查环节。

*   **变更影响分析 (`ndoc impact`)**
    *   **功能特征**：结合 Git 变更记录与依赖图谱，自动分析代码修改可能影响的下游模块和测试用例。
    *   **实现手段**：`ImpactService` 获取 Git diff，在依赖图中反向遍历引用链。
    *   **适用对象**：开发者（提交代码前自测），QA（精准回归测试）。

*   **测试用例反向映射 (Test Mapping)**
    *   **功能特征**：自动建立测试用例与被测代码之间的映射关系，支持通过被测函数反查测试用例。
    *   **实现手段**：`TestUsageMapper` 基于 AST 扫描 `tests/` 目录下的函数调用，解析 Import 别名建立引用链。
    *   **适用对象**：QA（回归测试范围确定），AI 助手（为生成的代码寻找参考测试）。

*   **代码质量门禁 (`ndoc lint` / `ndoc typecheck`)**
    *   **功能特征**：封装项目特定的 Lint 和 Typecheck 命令（如 pylint, mypy），提供统一的调用入口。
    *   **实现手段**：`quality_flow` 读取 `_RULES.md` 中的配置并执行 shell 命令。
    *   **适用对象**：CI/CD 流水线。

### 3.3 领域三：知识沉淀与记忆管理 (Knowledge Management)
> **解决问题**：重复踩坑、决策丢失、隐性知识难以传承。

*   **项目记忆归档 (`ndoc archive`)**
    *   **功能特征**：扫描代码中的特殊标记（`@DECISION`, `@LESSON`, `@INTENT`），汇聚生成 `_MEMORY.md`，并支持向量化存储以便检索。
    *   **实现手段**：`MemoryReportPlugin` 提取分散在注释中的非结构化知识，将其结构化并持久化，构建项目的“长期记忆”。
    *   **适用对象**：团队全员（复盘回顾），AI 助手（通过 RAG 检索历史教训以避免重复错误）。

*   **短期记忆热度图 (Hippocampus)**
    *   **功能特征**：实时追踪开发者的文件访问与编辑行为，计算文件与 Tag 的“热度”（Heat），识别当前活跃上下文。
    *   **实现手段**：`Hippocampus` 模块维护一个带衰减因子的滑动窗口缓冲区，基于时间戳计算热度值。
    *   **适用对象**：AI 助手（优先推荐近期活跃的上下文）。

*   **项目统计与任务追踪 (`ndoc stats`)**
    *   **功能特征**：生成 `_STATS.md`（代码行数、复杂度、注释率等统计）和 `_STATUS.md`（自动聚合代码中的 TODO/FIXME 标记）。
    *   **实现手段**：`StatsReportPlugin` 计算代码度量，`StatusPlugin` 扫描源码中的任务标记。
    *   **适用对象**：项目经理（进度监控），开发者（任务清单）。

*   **架构决策记录 (`_ADR.md`)**
    *   **功能特征**：自动聚合代码中标记的架构决策（`@DECISION`），形成按模块分类的决策日志。
    *   **实现手段**：`AdrReportPlugin` 提取决策元数据并生成文档。
    *   **适用对象**：架构师，新成员（理解设计背后的“为什么”）。

*   **数据字典注册 (`ndoc data`)**
    *   **功能特征**：自动识别项目中的数据结构（`dataclass`, `TypedDict`, `Enum`, `struct`），生成中心化的数据字典 `_DATA.md`。
    *   **实现手段**：`DataSchemaPlugin` 专门解析数据定义类语法节点。
    *   **适用对象**：前后端开发者（对齐接口字段），AI 助手（理解业务数据模型）。

*   **语义检索与 Prompt 生成 (`ndoc search` / `ndoc prompt`)**
    *   **功能特征**：支持自然语言搜索代码库（RAG），并为 AI 生成包含相关上下文的 Prompt 片段。
    *   **实现手段**：`SearchService` / `PromptService` 基于向量数据库（VectorDB）进行语义匹配。
    *   **适用对象**：开发者（寻找功能实现），AI 助手（增强上下文）。

### 3.4 领域四：环境感知与效能工具 (Environment & Utility)
> **解决问题**：工具链配置繁琐、运行环境不一致。

*   **能力自检 (`ndoc caps`)**
    *   **功能特征**：自动检测项目所需语言（Python, TS, Rust 等），并验证/安装对应的 Tree-sitter 解析器绑定。
    *   **实现手段**：`CapabilityMapPlugin` 扫描文件后缀，动态加载核心解析能力。
    *   **适用对象**：DevOps，初次配置环境的开发者。

*   **环境诊断 (`ndoc doctor`)**
    *   **功能特征**：全方位检查 OS、Python 版本、依赖库及项目配置文件的健康状态。
    *   **适用对象**：遇到运行问题时的排查工具。

*   **项目初始化 (`ndoc init`)**
    *   **功能特征**：生成标准的 Niki-docAI 配置文件（`_RULES.md`, `_SYNTAX.md`）。
    *   **适用对象**：新项目接入。

*   **清理与维护 (`ndoc clean` / `ndoc update` / `ndoc verify`)**
    *   **功能特征**：清理生成产物、自我更新、验证文档完整性。
    *   **适用对象**：日常维护。

*   **上下文注入 (`ndoc inject`)**
    *   **功能特征**：将生成的上下文头（Header）注入到源代码文件中，使代码文件本身携带上下文信息。
    *   **适用对象**：遗留代码库治理。

### 3.5 领域五：高级扩展与生态集成 (Advanced & Ecosystem)
> **解决问题**：实时性需求、IDE 原生体验与二次开发能力。

*   **实时守护模式 (`ndoc watch`)**
    *   **功能特征**：后台驻留的守护进程，监听文件变更事件（Debounce），增量更新对应的 `_AI.md` 和 `_MAP.md`，确保存档永远最新。
    *   **实现手段**：基于 `watchdog` 库实现文件系统监听器，结合 `Hippocampus` 短期记忆模块处理高频变更。
    *   **适用对象**：本地开发环境。

*   **IDE 语言服务 (`ndoc server`)**
    *   **功能特征**：启动标准 LSP (Language Server Protocol) 服务，为 VS Code 等编辑器提供 Niki-docAI 的语义能力（如规则检查、文档提示）。
    *   **实现手段**：`lsp_server` 模块实现基于 stdio 的 JSON-RPC 通信。
    *   **适用对象**：IDE 插件开发者，需要集成 ndoc 能力的编辑器。

*   **IDE 集成 (VS Code Extension)**
    *   **功能特征**：提供 VS Code 插件，支持侧边栏导航、实时文档预览、代码跳转辅助等原生 IDE 体验。
    *   **实现手段**：基于 `editors/vscode` 目录下的 TypeScript 扩展实现，与 Python 内核通信。
    *   **适用对象**：习惯 IDE 操作的开发者。

*   **插件开发 SDK (Plugin SDK)**
    *   **功能特征**：提供标准的 `SensorPlugin` 和 `ActionPlugin` 接口，允许开发者通过编写 Python 类扩展 `ndoc` 的分析与生成能力。
    *   **实现手段**：`ndoc.sdk.interfaces` 定义了基于 `pluggy` 的钩子规范（HookSpecs）。
    *   **适用对象**：需要定制化分析逻辑的高级用户。

*   **全量领航模式 (`ndoc pilot`)**
    *   **功能特征**：`ndoc all` 的别名，一键执行完整的 ECS 流水线，生成所有类型的文档（Map, Context, Deps, Arch, Stats, Status 等）。
    *   **适用对象**：日常开发结束时的归档操作。

*   **高度可配置系统 (`ProjectConfig`)**
    *   **功能特征**：支持通过配置文件自定义扫描规则、忽略模式、模板覆盖（Template Overrides）及外部工具命令。
    *   **实现手段**：`ndoc.models.config` 定义了灵活的配置数据模型。
    *   **适用对象**：有特定规范要求的团队。

---

## 4. 技术实现总结 (Technical Summary)

Niki-docAI 2.0 采用了高性能的 **ECS (Entity-Component-System) 架构**：

*   **Kernel (内核)**：负责插件生命周期管理与流水线调度。
*   **Entities (实体)**：代码文件被抽象为统一的 ID（路径）。
*   **Components (组件)**：数据载体，如 `SymbolComponent`（符号信息）、`GraphComponent`（依赖关系）、`MetaComponent`（元数据）、`MemoryComponent`（记忆片段）。
*   **Plugins (插件/系统)**：
    *   **Sensors (感知器)**：如 `FileCollector`, `SyntaxAnalysis`，负责将代码转化为 Component 数据。
    *   **Actions (执行器)**：如各类 `ReportPlugin`，负责消费 Component 数据并生成 Markdown 文档或执行检查。

这种架构确保了各功能模块的高度解耦与复用，使得 `ndoc` 能够灵活适应不同规模和技术栈的项目，成为连接人类意图与 AI 执行的坚实桥梁。
