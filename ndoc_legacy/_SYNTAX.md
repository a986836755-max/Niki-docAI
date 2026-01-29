# PROJECT SYNTAX
> @CONTEXT: DSL Definition | @TAGS: @SYNTAX @OP
<!-- NIKI_VERSION: 0.1.0 -->

## @OP
| Op | Meaning |
| :--- | :--- |
| `->` | **Flow**: Logic -> Comp |
| `<-` | **Read**: Sys <- Comp |
| `=>` | **Map**: ID => Sprite |
| `>>` | **Move**: Ptr >> Sys |
| `?` | **Check**: Dirty? |
| `+` | **Mix**: Pos + Vel |
| `!` | **Ban**: !Draw |

## @TAGS
> Global Tag Definitions. AI MUST follow these semantics.

### Structural
- `@DOMAIN`: **Scope**. Boundary/Domain.
- `@MODULE`: **Module**. Independent unit.
- `@API`: **Public**. Public Interface.
- `@AGGREGATE`: **Recursive**. Include subdirs.
- `@ARCH`: **Architecture**. File list/Graph.
- `@MAP`: **Navigation**. Links/Structure.
- `@TREE`: **Directory Tree**. Project hierarchy.
- `@GRAPH`: **Dependency Graph**. Visual relationships.
- `@INDEX`: **Index**. Cross-reference.

### Constraint
- `!RULE`: **Constraint**. Mandatory rule.
- `!CONST`: **Invariant**. Immutable fact.

### Semantic
- `@OVERVIEW`: **Summary**. Core responsibility/Why it exists.
- `@VISION`: **Vision**. Long-term goal.
- `@USAGE`: **Usage**. Examples/How-to.
- `@FLOW`: **Process**. Sequence/Data flow.
- `@STATE`: **State**. State machine/Variables.
- `@EVENT`: **Event**. Emitted/Handled events.
- `@DEF`: **Term**. Definition/Concept.
- `@TERM`: **Glossary**. Term definition.
- `@TECH`: **Technology**. Stack info.
- `@STACK`: **Stack**. Dependencies/Versions.
- `@ANALYSIS`: **Analysis**. Insights/Metrics.

### Evolutionary
- `!TODO`: **Debt**. Known issue.
- `@PLAN`: **Roadmap**. Future plan.
- `@BACKLOG`: **Backlog**. Future tasks.
- `@MEMORY`: **ADR**. Decision record.
- `@ADR`: **Decision**. Record of decisions.
- `@DEPRECATED`: **No**. Do not use.
- `@EXPERIMENTAL`: **WIP**. Unstable.
- `@LEGACY`: **Legacy**. Old code.

### Meta
- `@META`: **Metadata**. File attributes.
- `@CONFIG`: **Configuration**. Settings/Rules.
- `@CHECK_IGNORE`: **Audit Ignore**.
- `@CONTEXT`: **Context**. Scope definition.
- `@TAGS`: **Tag Def**. Tag dictionary.
- `@SYNTAX`: **Syntax**. DSL rules.
- `@OP`: **Operator**. DSL operators.
- `@TOOL`: **Tooling**. CLI instructions.

### Live Markers (Auto-Dashboard)
- `<!-- NIKI_AUTO_DOC_START -->`: **Generic**. Start of auto-gen block.
- `<!-- NIKI_AUTO_DOC_END -->`: **Generic**. End of auto-gen block.
- `<!-- NIKI_TODO_START -->`: **Todo**. Start of task aggregation.
- `<!-- NIKI_CTX_START -->`: **Context**. Start of live context.
- `<!-- NIKI_MAP_START -->`: **Map**. Start of file tree.

### @DISCOVERED
> Auto-discovered tags from file headers.
- `@UNKNOWN`: **Unknown**. Placeholder.
- `@TODO`: **Unreviewed**. Found in [_NEXT.md].
