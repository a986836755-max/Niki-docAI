# PROJECT SYNTAX
> @CONTEXT: DSL 定义 | @TAGS: @SYNTAX @OP

<!-- NIKI_VERSION: 2.0.0 -->

## @MOD
| Mod | Meaning | Concept |
| :--- | :--- | :--- |
| `PUB:` | **Public**: 公开接口 (Exported API) | Scope: Global |
| `PRV:` | **Private**: 私有实现 (Internal Impl) | Scope: Local |
| `GET->`| **Getter**: 读取/属性 (Property) | Flow: Output |

## @KIND
| Kind | Meaning | Context |
| :--- | :--- | :--- |
| `CLS` | **Class**: 类定义 | Object/Type |
| `STC` | **Struct**: 结构体/数据 | Data/Schema |
| `FUN` | **Function**: 函数/方法 | Action/Logic |
| `VAR` | **Variable**: 变量/属性 | State/Data |
| `MOD` | **Module**: 模块/文件 | Container |

## @OP
| Op | Meaning |
| :--- | :--- |
| `->` | **Flow**: 流向 (Logic -> Comp) |
| `<-` | **Read**: 读取 (Sys <- Comp) |
| `=>` | **Map**: 映射 (ID => Sprite) |
| `>>` | **Move**: 移动/转移 (Ptr >> Sys) |
| `?` | **Check**: 检查 (Dirty?) |
| `!` | **Ban**: 禁止 (!Draw) |

## @TAGS
> 全局标签定义。AI 必须遵循这些语义。
> 新增支持属性语法：`@TAG[KEY=VALUE, FLAG]` (e.g., `!RULE[CRITICAL]`, `@ADR[CONF=0.8]`)

### Identity (身份类)
- `@OVERVIEW`: **Summary**. 核心职责/存在意义 (Core responsibility).
- `@API`: **Public**. 公共接口 (Public Interface).
- `@DOMAIN`: **Scope**. 边界/领域 (Boundary/Domain).
- `@MODULE`: **Module**. 独立单元 (Independent unit).

### Logic (逻辑类)
- `@FLOW`: **Process**. 时序/数据流 (Sequence/Data flow).
- `@STATE`: **State**. 状态机/变量 (State machine/Variables).
- `@EVENT`: **Event**. 发射/处理的事件 (Emitted/Handled events).
- `@TECH`: **Technology**. 技术栈信息 (Stack info).

### Contract (契约类)
- `!RULE`: **Constraint**. 强制规则 (Mandatory rule). 支持 `[CRITICAL]` 属性。
- `!CONST`: **Invariant**. 不可变事实 (Immutable fact).
- `!LIMIT`: **Boundary**. 技术边界 (Technical limits).

### Memory (记忆类)
- `@ADR`: **Decision**. 架构决策记录 (Architecture Decision Record). 取代 `@MEMORY`, `@DECISION`.
- `!TODO`: **Plan**. 待办/债务 (Tasks/Debt). 取代 `@BACKLOG`, `@PLAN`.
- `@REF`: **Reference**. 长效引用 (Long-term reference).
- `# @NDOC:OBSERVE`: **Observation**. 观察者快照 (Observation Snapshot).

### Meta (元数据类)
- `@CONTEXT`: **Context**. 范围定义 (Scope definition).
- `@SYNTAX`: **Syntax**. DSL 规则 (DSL rules).
- `@CONFIG`: **Configuration**. 设置/规则 (Settings/Rules).
- `@DEPRECATED`: **No**. 请勿使用 (Do not use).
- `@EXPERIMENTAL`: **WIP**. 不稳定 (Unstable).
- `!LINT`: **Lint Command**. 质量门禁 lint 命令列表 (Quality gate lint commands).
- `!TYPECHECK`: **Typecheck Command**. 质量门禁 typecheck 命令列表 (Quality gate typecheck commands).

### Structural (结构类 - Auto)
- `@AGGREGATE`: **Recursive**. 包含子目录 (Include subdirs).
- `@MAP`: **Navigation**. 链接/结构 (Links/Structure).
- `@graph`: **Dependency**. 依赖关系 (Dependencies).

### Live Markers (自动仪表盘)
- `<!-- NIKI_AUTO_DOC_START -->`: **Generic**. 自动生成块 (Auto-gen block).
- `<!-- NIKI_TODO_START -->`: **Task**. 任务聚合 (Task aggregation).
- `<!-- NIKI_MEMORIES_START -->`: **Memory**. 记忆聚合 (Memory aggregation).

### @DISCOVERED
> 自动发现的潜在概念 (Automatically discovered concepts).
- `@UNKNOWN`: **Placeholder**. 未定义标签 (Undefined tag).
