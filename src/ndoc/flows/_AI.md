# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 16:49:04

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Flows: Business Logic Pipelines.
*   **[archive_flow.py](archive_flow.py#L1)**: Flow: Project Archiving & Memory. @DEP: atoms, datetime.datetime, datetime, atoms.llm, atoms.io, models.config.ProjectConfig, pathlib.Path, re, models.config, pathlib
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _extract_memory`(config: ProjectConfig, archived_content: list, memory_file: Path)`
*   **[clean_flow.py](clean_flow.py#L1)**: Flow: Clean / Reset. @DEP: typing.List, typing, ndoc.models.config, os, pathlib.Path, typing.Optional, ndoc.models.config.ProjectConfig, pathlib
    *   `@API`
        *   `VAL->` VAR **GENERATED_FILES**` = [
    "_AI.md",
    "_MAP.md",
    "_TECH.md",
    "_DEPS.md",
    "_NEXT.md",
    "_SYMBOLS.md",
    "_DATA.md",
    "_STATS.md",
    "_SYNTAX.md",
    # _ARCH.md is typically manual or hybrid, avoiding delete for safety unless confirmed
]`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str = None, force: bool = False) -> bool`
*   **[config_flow.py](config_flow.py#L1)**: Flow: Configuration Loading. @DEP: typing.List, typing.Set, typing, ndoc.models.config, ndoc.models.config.ScanConfig, pathlib.Path, re, ndoc.atoms, ndoc.atoms.io, ndoc.models.config.ProjectConfig, pathlib
    *   `@API`
        *   `VAL->` VAR **RULES_TEMPLATE**` = """# Project Rules
> @CONTEXT: Configuration | @TAGS: @CONFIG @RULES

## Scanning Rules (扫描规则)
> 定义哪些文件应该被忽略或包含。

- `!IGNORE`: .git, .vscode, .idea, __pycache__, node_modules, dist, build, .venv, venv
- `!INCLUDE`: .py, .md, .json, .js, .ts, .html, .css, .yml, .yaml, .toml

## Documentation Style (文档风格)
> 定义生成的文档样式。

- `!LANG`: Chinese (zh-CN)

## ALM & Memory Rules (ALM与记忆规则)
> 定义项目生命周期与自动归档规则。

- `MEMORY文档对齐`: 定期更新_MEMORY.md，每当_NEXT.md中一项功能/模块完成，将其归档入_MEMORY.md。
- `交付即更新`: 在完成代码修改后，习惯性运行 `ndoc all`，确保改动被即时索引。

## Special Keywords (特殊关键字)
> 用于控制特定目录的文档生成行为。

- `@AGGREGATE`: **Recursive Aggregation**. 当目录包含此标记时，不为子目录生成单独的 `_AI.md`，而是将其内容递归聚合到父级 `_AI.md` 中。
- `@CHECK_IGNORE`: **Audit Ignore**. 当目录包含此标记时，完全跳过该目录及其子目录的 `_AI.md` 生成。
"""`
        *   `PUB:` FUN **load_project_config**`(root_path: Path) -> ProjectConfig`
        *   `PUB:` FUN **ensure_rules_file**`(root_path: Path, force: bool = False) -> bool`
        *   `PRV:` FUN _parse_rules`(file_path: Path, config: ProjectConfig) -> None`
*   **[context_flow.py](context_flow.py#L1)**: Flow: Recursive Context Generation. @DEP: models.context.FileContext, datetime, atoms.io, dataclasses.dataclass, dataclasses, pathlib.Path, atoms.scanner, atoms.ast, models.context, models.config, pathlib, models.context.DirectoryContext, atoms.deps, typing.List, datetime.datetime, models.config.ProjectConfig, atoms, typing, dataclasses.field, typing.Optional, re, atoms.fs
    *   `@API`
        *   `PUB:` FUN **format_file_summary**`(ctx: FileContext, root: Optional[Path] = None) -> str`
        *   `PUB:` FUN **format_symbol_list**`(ctx: FileContext) -> str`
        *   `PRV:` FUN _format_single_symbol`(sym, level: int)`
        *   `PUB:` FUN **format_dependencies**`(ctx: FileContext) -> str`
        *   `PUB:` FUN **generate_dir_content**`(context: DirectoryContext) -> str`
        *   `PUB:` FUN **cleanup_legacy_map**`(file_path: Path) -> None`
        *   `PUB:` FUN **process_directory**`(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False) -> Optional[DirectoryContext]`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PUB:` FUN **update_directory**`(path: Path, config: ProjectConfig) -> bool`
*   **[data_flow.py](data_flow.py#L1)**: Flow: Data Registry Generation. @DEP: typing.Dict, datetime, atoms.io, pathlib.Path, dataclasses, dataclasses.dataclass, atoms.scanner, atoms.ast, models.context, models.config, pathlib, typing.List, typing.Any, datetime.datetime, models.config.ProjectConfig, atoms, typing, models.context.Symbol, atoms.fs
    *   `@API`
        *   `PUB:` CLS **DataDefinition**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **path**`: str`
            *   `VAL->` VAR **docstring**`: str`
            *   `VAL->` VAR **fields**`: List[str]`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PUB:` FUN **get_plural**`(name: str) -> str`
*   **[deps_flow.py](deps_flow.py#L1)**: Flow: Dependency Graph Generation. @DEP: atoms, typing.List, typing.Set, atoms.deps, typing, datetime.datetime, datetime, atoms.io, models.config.ProjectConfig, collections.defaultdict, pathlib.Path, typing.Dict, models.config, atoms.fs, pathlib, collections
    *   `@API`
        *   `PUB:` FUN **collect_imports**`(root: Path) -> Dict[str, List[str]]`
        *   `PUB:` FUN **build_dependency_graph**`(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]`
        *   `PUB:` FUN **generate_mermaid_graph**`(graph: Dict[str, Set[str]]) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[doctor_flow.py](doctor_flow.py#L1)**: Flow: System Diagnostics. @DEP: typing.List, typing, ndoc.models.config, tree_sitter.Language, platform, importlib, pathlib.Path, tree_sitter.Parser, tree_sitter_python, sys, tree_sitter, shutil, typing.Tuple, ndoc.models.config.ProjectConfig, pathlib
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _pass`(msg: str)`
        *   `PRV:` FUN _fail`(msg: str)`
        *   `PRV:` FUN _warn`(msg: str)`
        *   `PRV:` FUN _check_import`(module_name: str) -> bool`
        *   `PRV:` FUN _check_tree_sitter_bindings`() -> bool`
        *   `PRV:` FUN _check_project_files`(config: ProjectConfig)`
*   **[init_flow.py](init_flow.py#L1)**: Flow: Initialization. @DEP: ndoc.flows.config_flow, ndoc.models.config, ndoc.flows, ndoc.flows.syntax_flow, ndoc.models.config.ProjectConfig
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[map_flow.py](map_flow.py#L1)**: Flow: Map Generation. @DEP: atoms, typing.List, datetime.datetime, datetime, typing, concurrent.futures.ThreadPoolExecutor, atoms.io, models.config.ProjectConfig, dataclasses, pathlib.Path, dataclasses.dataclass, typing.Dict, concurrent.futures, atoms.scanner, typing.Callable, models.config, atoms.fs, pathlib
    *   `@API`
        *   `PUB:` CLS **MapContext**
            *   `VAL->` VAR **root**`: Path`
            *   `VAL->` VAR **ignore_patterns**`: List[str]`
        *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str`
        *   `PUB:` FUN **format_file_entry**`(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str`
        *   `PUB:` FUN **extract_file_summary**`(path: Path) -> str`
        *   `PUB:` FUN **build_tree_lines**`(current_path: Path, context: MapContext, level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]`
        *   `PUB:` FUN **generate_tree_content**`(config: ProjectConfig) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[plan_flow.py](plan_flow.py#L1)**: Flow: Project Planning. @DEP: atoms, datetime.datetime, datetime, atoms.llm, atoms.io, models.config.ProjectConfig, pathlib.Path, models.config, atoms.fs, pathlib
    *   `@API`
        *   `VAL->` VAR **PLAN_SYSTEM_PROMPT**` = """
You are a senior software architect and project manager. 
Your task is to take a high-level "Objective" and break it down into actionable tasks for a developer.
These tasks will be added to the project's `_NEXT.md` roadmap.

Rules:
1. Keep tasks specific and actionable.
2. Group tasks logically into a new section.
3. Use Markdown format with checkboxes: * [ ] #task-id: description.
4. Each task MUST have a unique `#task-id` (e.g., #refactor-auth, #ui-login).
5. Output ONLY the new section content in Markdown, starting with a level 3 header `###`.

Current context:
You are working on Niki-docAI, a tool that generates documentation context for AI assistants.
"""`
        *   `PUB:` FUN **run**`(config: ProjectConfig, objective: str) -> bool`
*   **[stats_flow.py](stats_flow.py#L1)**: Flow: Statistics. @DEP: datetime.datetime, datetime, ndoc.models.config, os, pathlib.Path, re, ndoc.atoms, ndoc.atoms.io, time, ndoc.models.config.ProjectConfig, pathlib
    *   `@API`
        *   `PUB:` FUN **check_should_update**`(root_path: Path, force: bool) -> bool`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[symbols_flow.py](symbols_flow.py#L1)**: Flow: Symbol Index Generation. @DEP: typing.Dict, collections, datetime, atoms.io, collections.defaultdict, pathlib.Path, atoms.lsp, atoms.scanner, atoms.ast, models.context, models.config, pathlib, typing.List, datetime.datetime, models.config.ProjectConfig, atoms, typing, typing.Optional, models.context.Symbol, atoms.fs
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _get_kind_icon`(kind: str) -> str`
*   **[syntax_flow.py](syntax_flow.py#L1)**: Flow: Syntax Manual Sync. @DEP: ndoc.models.config, pathlib.Path, ndoc.atoms, ndoc.atoms.io, ndoc.models.config.ProjectConfig, pathlib
    *   `@API`
        *   `VAL->` VAR **SYNTAX_TEMPLATE**` = r"""# PROJECT SYNTAX
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
"""`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[tech_flow.py](tech_flow.py#L1)**: Flow: Tech Stack Snapshot Generation. @DEP: datetime.datetime, datetime, ndoc.models.config, pathlib.Path, ndoc.atoms, ndoc.atoms.io, ndoc.models.config.ProjectConfig, pathlib, ndoc.atoms.deps
    *   `@API`
        *   `PUB:` FUN **generate_tech_content**`(config: ProjectConfig) -> str`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[todo_flow.py](todo_flow.py#L1)**: Flow: Todo Aggregation. @DEP: atoms, typing.List, datetime.datetime, datetime, typing, atoms.io, models.config.ProjectConfig, pathlib.Path, dataclasses, dataclasses.dataclass, typing.Dict, typing.Optional, re, atoms.scanner, models.config, atoms.fs, pathlib
    *   `@API`
        *   `PUB:` CLS **TodoItem**
            *   `VAL->` VAR **file_path**`: Path`
            *   `VAL->` VAR **line**`: int`
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **content**`: str`
            *   `VAL->` VAR **task_id**`: Optional[str] = None`
            *   `GET->` PRP **priority_icon**`(self) -> str`
        *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]`
        *   `PUB:` FUN **format_todo_lines**`(todos: List[TodoItem], root: Path) -> str`
        *   `PUB:` FUN **sync_tasks**`(config: ProjectConfig, todos: List[TodoItem]) -> bool`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[update_flow.py](update_flow.py#L1)**: Flow: Self-Update Flow. @DEP: typing, pathlib.Path, typing.Optional, sys, subprocess, pathlib
    *   `@API`
        *   `PRV:` FUN _is_git_repo`(path: Path) -> bool`
        *   `PUB:` FUN **run**`() -> bool`
*   **[verify_flow.py](verify_flow.py#L1)**: Flow: Verification. @DEP: atoms, ndoc.models.config, atoms.io, atoms.fs, sys, atoms.scanner, ndoc.models.config.ProjectConfig
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _verify_rules_content`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _check_architecture`(config: ProjectConfig) -> bool`
<!-- NIKI_AUTO_Context_END -->
