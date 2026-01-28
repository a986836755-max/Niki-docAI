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

## 2. Tags (标签)
- `@DOMAIN`: Scope/Domain definition.
- `!RULE`: Constraint definition.
- `@CHECK_IGNORE`: Ignore path for audit.
