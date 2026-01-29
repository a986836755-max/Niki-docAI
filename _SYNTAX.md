# NIKI_DOC_SYNTAX
> **Context**: Definition of Documentation Syntax, Operators, and Tags.
> **Tags**: `@SYNTAX`
<!-- NIKI_VERSION: 0.1.0 -->

## 1. Operators (逻辑操作符)
| Op | Meaning |
| :--- | :--- |
| `->` | **Flow/Write**: Data flow or write. `Logic -> Comp` (Logic writes Comp). |
| `<-` | **Read**: Read access. `Sys <- Comp` (System reads Comp). |
| `=>` | **Map/Transform**: Mapping or transformation. `TypeID => Sprite` (Map ID to Sprite). |
| `>>` | **Move/Transfer**: Strong ownership transfer. `UniquePtr >> System`. |
| `?` | **Optional/Check**: Optional or conditional check. `Dirty?` (If Dirty). |
| `+` | **Combine**: Combination or dependency. `Pos + Vel`. |
| `!` | **Ban**: Prohibition. `!DrawCall`. |

## 2. Global Tags (通用标签库)
These tags are standard across all Niki-docAI projects.

### Structural (结构类)
- `@DOMAIN`: **Scope Definition**. Defines the domain or boundary of a directory.
- `@MODULE`: **Module Definition**. Marks a directory as a distinct software module.
- `@API`: **Public Interface**. Marks a file or function as a public API.
- `@AGGREGATE`: **Aggregation**. Aggregates subdirectories into current context (stops sub-context creation).

### Behavioral (行为类)
- `@FLOW`: **Process Flow**. Describes a sequence of steps or data flow.
- `@STATE`: **State Definition**. Describes a state machine or state variable.
- `@EVENT`: **Event Definition**. Describes an event emitted or handled.

### Constraint (约束类)
- `!RULE`: **Constraint**. A mandatory rule that must be followed.
- `!CONST`: **Invariant**. A value or condition that must remain constant.
- `!TODO`: **Technical Debt**. A known issue or missing feature.

### Meta (元数据类)
- `@DEPRECATED`: **Deprecation Warning**. This element should no longer be used.
- `@EXPERIMENTAL`: **Unstable**. This feature is subject to change.
- `@LEGACY`: **Legacy Code**. Old code maintained for compatibility.
- `@CHECK_IGNORE`: **Audit Ignore**. Excludes path from automated checks.
