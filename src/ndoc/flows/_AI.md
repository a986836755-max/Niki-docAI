# Context: flows
> @CONTEXT: Local | flows | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 11:29:48

## !RULE
*   **Incremental Update Integration**: All flows (Map, Context, Symbols, Todo, Data) are now integrated with `scanner.scan_file`, which uses `FileCache` to avoid re-parsing unchanged files.
*   **Logic as Data (Data Registry)**: `data_flow.py` extracts `@dataclass`, `Enum`, and `TypedDict` to `_DATA.md`, providing a centralized view of the project's data models.
*   **Dependency Visualization**: `deps_flow.py` generates a Mermaid graph in `_DEPS.md`, capturing both module-level and package-level dependencies via improved AST import extraction.
*   **Project Archiving**: `archive_flow.py` implements the "MEMORY" rule, automatically archiving completed tasks from `_NEXT.md` to `_MEMORY.md`.

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
- `语义化文档补完`: 在开发完成后，主动编辑 `_AI.md` 填充设计意图与调用约束，确保文档具有“人类可读的语义”。
- `标签与元数据对齐`: 根据模块引入的新技术栈，动态更新 `_AI.md` 顶部的 `@TAGS`。

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
*   **[symbols_flow.py](symbols_flow.py#L1)**: Flow: Symbol Index Generation. @DEP: typing.Dict, collections, datetime, atoms.io, collections.defaultdict, pathlib.Path, atoms.scanner, atoms.ast, models.context, models.config, pathlib, typing.List, datetime.datetime, models.config.ProjectConfig, atoms, typing, typing.Optional, models.context.Symbol, atoms.fs
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
*   **[verify_flow.py](verify_flow.py#L1)**: Flow: Verification. @DEP: ndoc.models.config, sys, ndoc.models.config.ProjectConfig
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
<!-- NIKI_AUTO_Context_END -->"`
        *   `VAL->` VAR **timestamp**` = datetime.now().strftime("%Y-%m-%d %H:%M:%S")`
        *   `VAL->` VAR **template**` = f"""# Context: {path.name}
> @CONTEXT: Local | {path.name} | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 11:29:48

## !RULE
<!-- Add local rules here -->

{start_marker}
{content}
{end_marker}
"""`
        *   `VAL->` VAR **wrapped_content**` = f"\n\n{start_marker}\n{content}\n{end_marker}\n"`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PUB:` FUN **update_directory**`(path: Path, config: ProjectConfig) -> bool`
*   **[deps_flow.py](deps_flow.py#L1)**: Flow: Dependency Graph Generation. @DEP: atoms, collections, datetime, models.config, pathlib, typing
    *   `@API`
        *   `PUB:` FUN **collect_imports**`(root: Path) -> Dict[str, List[str]]`
        *   `VAL->` VAR **import_map**` = {}`
        *   `VAL->` VAR **ignore**` = {'.git', '__pycache__', 'venv', 'env', 'node_modules', 'dist', 'build', 'site-packages'}`
        *   `VAL->` VAR **files**` = fs.walk_files(root, ignore_patterns=list(ignore), extensions={'.py'})`
        *   `VAL->` VAR **content**` = io.read_text(file_path)`
        *   `VAL->` VAR **imports**` = deps.extract_imports(content)`
        *   `VAL->` VAR **rel_path**` = file_path.relative_to(root).as_posix()`
        *   `PUB:` FUN **build_dependency_graph**`(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]`
        *   `VAL->` VAR **graph**` = defaultdict(set)`
        *   `VAL->` VAR **path_to_mod**` = {}`
        *   `VAL->` VAR **mod_to_path**` = {}`
        *   `VAL->` VAR **clean_path**` = path`
        *   `VAL->` VAR **clean_path**` = clean_path[4:]`
        *   `VAL->` VAR **clean_path**` = clean_path[:-3]`
        *   `VAL->` VAR **clean_path**` = clean_path[:-11]`
        *   `VAL->` VAR **module_name**` = clean_path.replace('/', '.')`
        *   `VAL->` VAR **source_mod**` = path_to_mod.get(file_path)`
        *   `VAL->` VAR **root_pkg**` = source_mod.split('.')[0]`
        *   `PUB:` FUN **generate_mermaid_graph**`(graph: Dict[str, Set[str]]) -> str`
        *   `VAL->` VAR **lines**` = ["graph TD"]`
        *   `VAL->` VAR **targets**` = sorted(list(graph[source]))`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `VAL->` VAR **target_file**` = config.scan.root_path / "_DEPS.md"`
        *   `VAL->` VAR **import_map**` = collect_imports(config.scan.root_path)`
        *   `VAL->` VAR **graph**` = build_dependency_graph(import_map)`
        *   `VAL->` VAR **mermaid**` = generate_mermaid_graph(graph)`
        *   `VAL->` VAR **timestamp**` = datetime.now().strftime("%Y-%m-%d %H:%M:%S")`
        *   `VAL->` VAR **content**` = f"""# Dependency Graph
> 最后更新 (Last Updated): 2026-01-31 11:29:48

> Auto-generated by Niki-docAI.

## Module Graph (Internal)

{mermaid}

> **Note**: Detailed per-file dependencies (Raw Imports) have been moved to local `_AI.md` files to keep this view clean.
"""`
*   **[doctor_flow.py](doctor_flow.py#L1)**: Flow: System Diagnostics. @DEP: importlib, ndoc.models.config, pathlib, platform, shutil, sys, tree_sitter, tree_sitter_python, typing
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `VAL->` VAR **all_passed**` = True`
        *   `VAL->` VAR **all_passed**` = False`
        *   `VAL->` VAR **dependencies**` = [
        ("watchdog", "Watchdog (File Monitor)"),
        ("tree_sitter", "Tree-sitter (Parser Core)"),
        ("tree_sitter_python", "Tree-sitter Python Grammar"),
        ("colorama", "Colorama (Terminal Color)"),
    ]`
        *   `VAL->` VAR **all_passed**` = False`
        *   `VAL->` VAR **all_passed**` = False`
        *   `PRV:` FUN _pass`(msg: str)`
        *   `PRV:` FUN _fail`(msg: str)`
        *   `PRV:` FUN _warn`(msg: str)`
        *   `PRV:` FUN _check_import`(module_name: str) -> bool`
        *   `PRV:` FUN _check_tree_sitter_bindings`() -> bool`
        *   `VAL->` VAR **PY_LANGUAGE**` = Language(tree_sitter_python.language())`
        *   `VAL->` VAR **parser**` = Parser(PY_LANGUAGE)`
        *   `PRV:` FUN _check_project_files`(config: ProjectConfig)`
        *   `VAL->` VAR **root**` = config.scan.root_path`
*   **[init_flow.py](init_flow.py#L1)**: Flow: Initialization. @DEP: ndoc.flows, ndoc.models.config
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
*   **[map_flow.py](map_flow.py#L1)**: Flow: Map Generation. @DEP: atoms, dataclasses, datetime, models.config, pathlib, typing
    *   `@API`
        *   `PUB:` CLS **MapContext**
            *   `VAL->` VAR **root**`: Path`
            *   `VAL->` VAR **ignore_patterns**`: List[str]`
        *   `PUB:` FUN **format_dir_entry**`(name: str, level: int) -> str`
        *   `VAL->` VAR **indent**` = "    " * level`
        *   `PUB:` FUN **format_file_entry**`(path: Path, root: Path, level: int) -> str`
        *   `VAL->` VAR **indent**` = "    " * level`
        *   `VAL->` VAR **name**` = path.name`
        *   `VAL->` VAR **rel_path**` = path.relative_to(root).as_posix()`
        *   `VAL->` VAR **rel_path**` = name`
        *   `VAL->` VAR **summary**` = ""`
        *   `VAL->` VAR **content**` = io.read_text(path)`
        *   `VAL->` VAR **docstring**` = scanner.extract_docstring(content)`
        *   `VAL->` VAR **raw_summary**` = scanner.extract_summary(content, docstring)`
        *   `VAL->` VAR **raw_summary**` = raw_summary[:47] + "..."`
        *   `VAL->` VAR **summary**` = f" - *{raw_summary}*"`
        *   `PUB:` FUN **build_tree_lines**`(current_path: Path, context: MapContext, level: int = 0) -> List[str]`
        *   `VAL->` VAR **lines**` = []`
        *   `VAL->` VAR **filter_config**` = fs.FileFilter(ignore_patterns=set(context.ignore_patterns))`
        *   `VAL->` VAR **entries**` = fs.list_dir(current_path, filter_config)`
        *   `PUB:` FUN **generate_tree_content**`(config: ProjectConfig) -> str`
        *   `VAL->` VAR **context**` = MapContext(
        root=config.scan.root_path,
        ignore_patterns=config.scan.ignore_patterns
    )`
        *   `VAL->` VAR **lines**` = build_tree_lines(context.root, context)`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `VAL->` VAR **map_file**` = config.scan.root_path / "_MAP.md"`
        *   `VAL->` VAR **tree_content**` = generate_tree_content(config)`
        *   `VAL->` VAR **start_marker**` = "<!-- NIKI_MAP_START -->"`
        *   `VAL->` VAR **end_marker**` = "<!-- NIKI_MAP_END -->"`
        *   `VAL->` VAR **timestamp**` = datetime.now().strftime("%Y-%m-%d %H:%M:%S")`
        *   `VAL->` VAR **template**` = f"""# Project Map
> @CONTEXT: Map | Project Structure
> 最后更新 (Last Updated): 2026-01-31 11:29:48

## @STRUCTURE
{start_marker}
{tree_content}
{end_marker}
"""`
        *   `VAL->` VAR **success**` = io.update_section(map_file, start_marker, end_marker, tree_content)`
*   **[stats_flow.py](stats_flow.py#L1)**: Flow: Statistics. @DEP: datetime, ndoc.atoms, ndoc.models.config, os, pathlib, re, time
    *   `@API`
        *   `PUB:` FUN **check_should_update**`(root_path: Path, force: bool) -> bool`
        *   `VAL->` VAR **rules_path**` = root_path / "_RULES.md"`
        *   `VAL->` VAR **rules_content**` = io.read_text(rules_path) or ""`
        *   `VAL->` VAR **match**` = re.search(r"!STATS_INTERVAL:\s*(\d+)([hms])", rules_content)`
        *   `VAL->` VAR **interval_seconds**` = 3600`
        *   `VAL->` VAR **val**` = int(match.group(1))`
        *   `VAL->` VAR **unit**` = match.group(2)`
        *   `VAL->` VAR **interval_seconds**` = val * 3600`
        *   `VAL->` VAR **interval_seconds**` = val * 60`
        *   `VAL->` VAR **interval_seconds**` = val`
        *   `VAL->` VAR **stats_path**` = root_path / "_STATS.md"`
        *   `VAL->` VAR **mtime**` = stats_path.stat().st_mtime`
        *   `VAL->` VAR **now**` = time.time()`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
        *   `VAL->` VAR **root_path**` = config.scan.root_path`
        *   `VAL->` VAR **total_files**` = 0`
        *   `VAL->` VAR **total_lines**` = 0`
        *   `VAL->` VAR **total_size**` = 0`
        *   `VAL->` VAR **doc_files**` = 0`
        *   `VAL->` VAR **doc_lines**` = 0`
        *   `VAL->` VAR **src_files**` = 0`
        *   `VAL->` VAR **src_lines**` = 0`
        *   `VAL->` VAR **ai_doc_files**` = 0`
        *   `VAL->` VAR **ai_doc_lines**` = 0`
        *   `VAL->` VAR **ai_doc_size**` = 0`
        *   `VAL->` VAR **total_dirs_scanned**` = 0`
        *   `VAL->` VAR **dirs_with_ai**` = 0`
        *   `VAL->` VAR **ignore_patterns**` = set(config.scan.ignore_patterns)`
        *   `VAL->` VAR **include_exts**` = set(config.scan.extensions)`
        *   `VAL->` VAR **has_ai_in_this_dir**` = False`
        *   `VAL->` VAR **file_path**` = Path(root) / file`
        *   `VAL->` VAR **size**` = file_path.stat().st_size`
        *   `VAL->` VAR **is_text**` = False`
        *   `VAL->` VAR **lines_count**` = 0`
        *   `VAL->` VAR **has_ai_in_this_dir**` = True`
        *   `VAL->` VAR **is_text**` = True`
        *   `VAL->` VAR **is_text**` = True`
        *   `VAL->` VAR **is_text**` = True`
        *   `VAL->` VAR **lines_count**` = sum(1 for _ in f)`
        *   `VAL->` VAR **estimated_tokens**` = total_size // 4`
        *   `VAL->` VAR **ai_estimated_tokens**` = ai_doc_size // 4`
        *   `VAL->` VAR **ratio**` = 0.0`
        *   `VAL->` VAR **ratio**` = ((doc_lines + ai_doc_lines) / src_lines) * 100`
        *   `VAL->` VAR **ai_coverage**` = 0.0`
        *   `VAL->` VAR **ai_coverage**` = (dirs_with_ai / total_dirs_scanned) * 100`
        *   `VAL->` VAR **timestamp**` = datetime.now().strftime("%Y-%m-%d %H:%M:%S")`
        *   `VAL->` VAR **content**` = f"""# 项目统计报告 (Project Statistics)
> @CONTEXT: Project Metrics | @TAGS: @STATS @AUTO
> 最后更新 (Last Updated): 2026-01-31 11:29:48

## 核心指标 (Core Metrics)

| 指标 (Metric) | 数值 (Value) | 说明 (Description) |
| :--- | :--- | :--- |
| **总文件数** | {total_files} | 包含代码和文档 |
| **总行数** | {total_lines} | 代码 + 文档总行数 |
| **项目体积** | {total_size / 1024:.2f} KB | 磁盘占用 |
| **预估 Token** | ~{estimated_tokens} | 全局上下文开销 (Size/4) |

## AI 上下文统计 (AI Context Stats)
> 针对 `_AI.md` 递归上下文文件的专项统计。

| 指标 (Metric) | 数值 (Value) | 说明 (Description) |
| :--- | :--- | :--- |
| **_AI.md 文件数** | {ai_doc_files} | 局部上下文节点数 |
| **_AI.md 总行数** | {ai_doc_lines} | 上下文总厚度 |
| **_AI.md Token** | ~{ai_estimated_tokens} | 上下文 Token 开销 |
| **目录覆盖率** | {ai_coverage:.1f}% ({dirs_with_ai}/{total_dirs_scanned}) | 包含 `_AI.md` 的目录比例 |

## 全局组成 (Global Composition)

| 类型 (Type) | 文件数 (Files) | 行数 (Lines) | 占比 (Ratio) |
| :--- | :--- | :--- | :--- |
| **源代码 (Source)** | {src_files} | {src_lines} | - |
| **文档 (Docs)** | {doc_files + ai_doc_files} | {doc_lines + ai_doc_lines} | {ratio:.1f}% (Doc/Code) |

## 健康度检查 (Health Check)

- **AI 上下文覆盖率**: {ai_coverage:.1f}%
  - {"✅ 覆盖良好 (>50%)" if ai_coverage > 50 else "⚠️ 覆盖率较低 (<50%)，建议补充 `_AI.md`"}
- **文档/代码比率**: {ratio:.1f}%
  - {"✅ 文档丰富 (>20%)" if ratio > 20 else "⚠️ 文档较少 (<20%)"}
"""`
        *   `VAL->` VAR **stats_path**` = root_path / "_STATS.md"`
*   **[syntax_flow.py](syntax_flow.py#L1)**: Flow: Syntax Manual Sync. @DEP: ndoc.atoms, ndoc.models.config, pathlib
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
        *   `VAL->` VAR **syntax_file**` = config.scan.root_path / "_SYNTAX.md"`
*   **[tech_flow.py](tech_flow.py#L1)**: Flow: Tech Stack Snapshot Generation. @DEP: datetime, ndoc.atoms, ndoc.models.config, pathlib
    *   `@API`
        *   `PUB:` FUN **generate_tech_content**`(config: ProjectConfig) -> str`
        *   `VAL->` VAR **lines**` = []`
        *   `VAL->` VAR **root_path**` = config.scan.root_path`
        *   `VAL->` VAR **languages**` = deps.detect_languages(root_path, set(config.scan.ignore_patterns))`
        *   `VAL->` VAR **bar_len**` = int(pct / 5)`
        *   `VAL->` VAR **bar**` = "█" * bar_len + "░" * (20 - bar_len)`
        *   `VAL->` VAR **all_deps**` = deps.get_project_dependencies(root_path)`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `VAL->` VAR **content**` = generate_tech_content(config)`
        *   `VAL->` VAR **tech_file**` = config.scan.root_path / "_TECH.md"`
        *   `VAL->` VAR **timestamp**` = datetime.now().strftime("%Y-%m-%d %H:%M:%S")`
        *   `VAL->` VAR **template**` = f"""# Tech Stack Snapshot
> @CONTEXT: Global | _TECH.md | @TAGS: @TECH @DEPS
> 最后更新 (Last Updated): 2026-01-31 11:29:48

{content}

---
*Generated by Niki-docAI*
"""`
*   **[todo_flow.py](todo_flow.py#L1)**: Flow: Todo Aggregation. @DEP: atoms, dataclasses, datetime, models.config, pathlib, typing
    *   `@API`
        *   `PUB:` CLS **TodoItem**
            *   `VAL->` VAR **file_path**`: Path`
            *   `VAL->` VAR **line**`: int`
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **content**`: str`
            *   `GET->` PRP **priority_icon**`(self) -> str`
            *   `VAL->` VAR **icons**` = {
            "FIXME": "🔴", # High
            "XXX": "🟣",   # Critical
            "HACK": "🚧",  # Warning
            "TODO": "🔵",  # Medium
            "NOTE": "ℹ️"   # Info
        }`
        *   `PUB:` FUN **collect_todos**`(root: Path, ignore_patterns: List[str]) -> List[TodoItem]`
        *   `VAL->` VAR **todos**` = []`
        *   `VAL->` VAR **filter_config**` = fs.FileFilter(
        ignore_patterns=set(ignore_patterns + ["_NEXT.md", "_TODO.md"]) # Avoid self-referencing
    )`
        *   `VAL->` VAR **files**` = fs.walk_files(root, list(filter_config.ignore_patterns))`
        *   `VAL->` VAR **content**` = io.read_text(file_path)`
        *   `VAL->` VAR **raw_todos**` = scanner.extract_todos(content)`
        *   `PUB:` FUN **format_todo_lines**`(todos: List[TodoItem], root: Path) -> str`
        *   `VAL->` VAR **lines**` = []`
        *   `VAL->` VAR **priority_order**` = {"FIXME": 0, "XXX": 1, "HACK": 2, "TODO": 3, "NOTE": 4}`
        *   `VAL->` VAR **sorted_todos**` = sorted(todos, key=lambda x: (priority_order.get(x.type, 99), x.file_path, x.line))`
        *   `VAL->` VAR **rel_path**` = todo.file_path.relative_to(root).as_posix()`
        *   `VAL->` VAR **link**` = f"[{rel_path}:{todo.line}]({rel_path}#L{todo.line})"`
        *   `VAL->` VAR **line**` = f"*   {todo.priority_icon} **{todo.type}** {link}: {todo.content}"`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `VAL->` VAR **next_file**` = config.scan.root_path / "_NEXT.md"`
        *   `VAL->` VAR **todos**` = collect_todos(config.scan.root_path, config.scan.ignore_patterns)`
        *   `VAL->` VAR **content**` = format_todo_lines(todos, config.scan.root_path)`
        *   `VAL->` VAR **start_marker**` = "<!-- NIKI_TODO_START -->"`
        *   `VAL->` VAR **end_marker**` = "<!-- NIKI_TODO_END -->"`
        *   `VAL->` VAR **timestamp**` = datetime.now().strftime("%Y-%m-%d %H:%M:%S")`
        *   `VAL->` VAR **template**` = f"""# Todo List
> @CONTEXT: Todos | _NEXT.md
> 最后更新 (Last Updated): 2026-01-31 11:29:48

{start_marker}
{content}
{end_marker}
"""`
        *   `VAL->` VAR **success**` = io.update_section(next_file, start_marker, end_marker, content)`
*   **[update_flow.py](update_flow.py#L1)**: Flow: Self-Update Flow. @DEP: pathlib, subprocess, sys, typing
    *   `@API`
        *   `PRV:` FUN _is_git_repo`(path: Path) -> bool`
        *   `PUB:` FUN **run**`() -> bool`
        *   `VAL->` VAR **current_file**` = Path(__file__).resolve()`
        *   `VAL->` VAR **src_root**` = current_file.parent.parent.parent`
        *   `VAL->` VAR **repo_root**` = src_root.parent`
        *   `VAL->` VAR **repo_root**` = src_root`
        *   `VAL->` VAR **status**` = subprocess.run(["git", "status", "--porcelain"], cwd=repo_root, capture_output=True, text=True)`
        *   `VAL->` VAR **result**` = subprocess.run(["git", "pull"], cwd=repo_root, text=True)`
*   **[verify_flow.py](verify_flow.py#L1)**: Flow: Verification. @DEP: ndoc.models.config, sys
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `VAL->` VAR **root**` = config.scan.root_path`
        *   `VAL->` VAR **required_files**` = [
        "_MAP.md",
        "_TECH.md",
        "_AI.md",
        "_RULES.md",
        "_SYNTAX.md"
    ]`
        *   `VAL->` VAR **missing**` = []`
        *   `VAL->` VAR **fpath**` = root / fname`
<!-- NIKI_AUTO_Context_END -->
