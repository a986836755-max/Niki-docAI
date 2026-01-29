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

### Structural (结构类)
- `@DOMAIN`: **Scope**. 边界/领域 (Boundary/Domain).
- `@MODULE`: **Module**. 独立单元 (Independent unit).
- `@API`: **Public**. 公共接口 (Public Interface).
- `@AGGREGATE`: **Recursive**. 包含子目录 (Include subdirs).
- `@ARCH`: **Architecture**. 文件列表/图谱 (File list/Graph).
- `@MAP`: **Navigation**. 链接/结构 (Links/Structure).
- `@TREE`: **Directory Tree**. 项目层级 (Project hierarchy).
- `@GRAPH`: **Dependency Graph**. 可视化关系 (Visual relationships).
- `@INDEX`: **Index**. 交叉引用 (Cross-reference).

### Constraint (约束类)
- `!RULE`: **Constraint**. 强制规则 (Mandatory rule).
- `!CONST`: **Invariant**. 不可变事实 (Immutable fact).

### Semantic (语义类)
- `@OVERVIEW`: **Summary**. 核心职责/存在意义 (Core responsibility).
- `@VISION`: **Vision**. 长期目标 (Long-term goal).
- `@USAGE`: **Usage**. 示例/用法 (Examples/How-to).
- `@FLOW`: **Process**. 时序/数据流 (Sequence/Data flow).
- `@STATE`: **State**. 状态机/变量 (State machine/Variables).
- `@EVENT`: **Event**. 发射/处理的事件 (Emitted/Handled events).
- `@DEF`: **Term**. 定义/概念 (Definition/Concept).
- `@TERM`: **Glossary**. 术语定义 (Term definition).
- `@TECH`: **Technology**. 技术栈信息 (Stack info).
- `@STACK`: **Stack**. 依赖/版本 (Dependencies/Versions).
- `@ANALYSIS`: **Analysis**. 洞察/指标 (Insights/Metrics).

### Evolutionary (演进类)
- `!TODO`: **Debt**. 已知问题 (Known issue).
- `@PLAN`: **Roadmap**. 未来计划 (Future plan).
- `@BACKLOG`: **Backlog**. 待办事项 (Future tasks).
- `@MEMORY`: **ADR**. 决策记录 (Decision record).
- `@ADR`: **Decision**. 决策记录 (Record of decisions).
- `@DEPRECATED`: **No**. 请勿使用 (Do not use).
- `@EXPERIMENTAL`: **WIP**. 不稳定 (Unstable).
- `@LEGACY`: **Legacy**. 旧代码 (Old code).

### Meta (元数据类)
- `@META`: **Metadata**. 文件属性 (File attributes).
- `@CONFIG`: **Configuration**. 设置/规则 (Settings/Rules).
- `@CHECK_IGNORE`: **Audit Ignore**. 审计忽略 (Audit Ignore).
- `@CONTEXT`: **Context**. 范围定义 (Scope definition).
- `@TAGS`: **Tag Def**. 标签字典 (Tag dictionary).
- `@SYNTAX`: **Syntax**. DSL 规则 (DSL rules).
- `@OP`: **Operator**. DSL 操作符 (DSL operators).
- `@TOOL`: **Tooling**. CLI 指令 (CLI instructions).

### Live Markers (自动仪表盘)
- `<!-- NIKI_AUTO_DOC_START -->`: **Generic**. 自动生成块开始 (Start of auto-gen block).
- `<!-- NIKI_AUTO_DOC_END -->`: **Generic**. 自动生成块结束 (End of auto-gen block).
- `<!-- NIKI_TODO_START -->`: **Todo**. 任务聚合开始 (Start of task aggregation).
- `<!-- NIKI_CTX_START -->`: **Context**. 实时上下文开始 (Start of live context).
- `<!-- NIKI_MAP_START -->`: **Map**. 文件树开始 (Start of file tree).

### @DISCOVERED
> 从文件头自动发现的标签。
- `@UNKNOWN`: **Unknown**. 占位符 (Placeholder).
- `@TODO`: **Unreviewed**. 发现于 [_NEXT.md] (Found in ...).
