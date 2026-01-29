# PROJECT RULES
> @CONTEXT: 规则 | 约束 | @TAGS: !RULE !CONST

<!-- NIKI_VERSION: 2.0.0 -->

## !CONST (Invariants)
1.  **Zero Legacy Dependency**: 新代码 **绝不能** 引入 `ndoc_legacy`。
2.  **Zero Overwrite**: `<!-- NIKI_AUTO_... -->` 标记之外的用户内容不可变。
3.  **Doc First**: 文档更新必须先于代码实现。

## !RULE (Development)

### Architecture
*   **!NO_OOP**: 业务逻辑中禁止使用 `class`。`class` 仅用于数据模型 (`dataclass`)。
*   **!PURE**: 逻辑函数应为纯函数 (Input -> Output)。副作用必须隔离在 `Atoms` 中。
*   **!MODULE**: 使用 Python 模块 (Module) 作为命名空间。不要创建 "Manager" 或 "Handler" 类。

### Paradigm (DOD/FP)
*   **!DATA_DRIVEN**: 逻辑即数据 (Logic as Data)。**严禁**硬编码的复杂控制流 (`if-else`, `switch`)。必须将业务规则提取为数据结构 (Table/Config/Rules)，仅编写通用的执行引擎。
*   **!PIPELINE**: 变换即管道 (Transformation as Pipeline)。代码应组织为数据变换链 (`Input -> Transform -> Output`)。
*   **!NO_BRANCH**: 消除分支 (Eliminate Branching)。优先使用字典映射 (Dispatch Table)、模式匹配或多态来替代条件判断。

### Style & Convention
*   **!LANG**: Docstrings 和注释应采用 **Hybrid** 风格 (中文描述，英文技术术语)。
    *   *Good*: `def scan(path): """扫描目录结构 (Scan directory structure)"""`
*   **!TYPE**: 所有函数签名 **必须** 包含类型提示 (Type Hints)。
*   **!DOC**: 每个公共函数 **必须** 包含 Docstring，向 AI 上下文解释其用途。

### Workflow
*   **!ATOMIC**: 提交 (Commits) 必须是原子化的。一个特性，一次提交。
*   **!TEST**: 在完成前使用 `test/playground` 脚本验证更改。

## !RULE (Documentation)
*   **!TAG**: 使用 `_SYNTAX.md` 中定义的标签 (如 `@FLOW`, `!RULE`) 对内容进行分类。
*   **!NO_EMOJI**: 文档中禁止使用 Emoji (优化 Token)。
*   **!LINK**: 链接使用相对路径。
