# Context: plugins
> @CONTEXT: Recursive Context | plugins | @TAGS: @AI
> 最后更新 (Last Updated): 2026-02-27 18:00:27

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->



## @FILES
<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[_AI.md](_AI.md#L1)**: Context: plugins
*   **[adr_report.py](adr_report.py#L1)**: ADR Report Plugin (Action). @DEP: src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/parsing/__init__.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **AdrReportPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[arch_report.py](arch_report.py#L1)**: Architecture Report Plugin (Action). @DEP: src/ndoc/core/__init__.py, src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/parsing/__init__.py, src/ndoc/sdk/interfaces.py, ...
    *   `@API`
        *   `PUB:` CLS **ArchitectureReportPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[capability_map.py](capability_map.py#L1)**: Capability Map Plugin (Action). @DEP: src/ndoc/core/__init__.py, src/ndoc/kernel/context.py, src/ndoc/parsing/__init__.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **CapabilityMapPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[checker.py](checker.py#L1)**: Constraint Checker Plugin (Action). @DEP: src/ndoc/brain/__init__.py, src/ndoc/kernel/context.py, src/ndoc/models/context.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **ConstraintCheckerPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[collector.py](collector.py#L1)**: Standard File Collector Plugin. @DEP: src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **FileCollectorPlugin**
            *   `PUB:` MET **ndoc_collect_entities**`(self, root_path: str) -> List[Entity]`
*   **[context_report.py](context_report.py#L1)**: Context Report Plugin (Action). @DEP: src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/models/context.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py, ...
    *   `@API`
        *   `PUB:` CLS **ContextReportPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[data_schema.py](data_schema.py#L1)**: Data Schema Plugin (Action). @DEP: src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/parsing/__init__.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **DataSchemaPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[deps_report.py](deps_report.py#L1)**: Dependency Report Plugin (Action). @DEP: src/ndoc/core/__init__.py, src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/parsing/deps/__init__.py, src/ndoc/sdk/interfaces.py, ...
    *   `@API`
        *   `PUB:` CLS **DependencyReportPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[deps_sensor.py](deps_sensor.py#L1)**: Dependency Graph Sensor Plugin. @DEP: src/ndoc/parsing/deps/__init__.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **DependencySensorPlugin**
            *   `PRV:` MET __init__`(self)`
            *   `PUB:` MET **ndoc_process_syntax**`(self, entity: Entity) -> Dict[str, Any]`
            *   `PUB:` MET **ndoc_process_dependencies**`(self, context)`
*   **[lesson_report.py](lesson_report.py#L1)**: Lesson Report Plugin (Action). @DEP: src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/parsing/__init__.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **LessonReportPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[map_report.py](map_report.py#L1)**: Map Report Plugin (Action). @DEP: src/ndoc/core/__init__.py, src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py, ...
    *   `@API`
        *   `PUB:` CLS **MapReportPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
            *   `PUB:` MET **build_tree_lines_from_ecs**`(current_path: Path, level: int = 0) -> List[str]`
*   **[memory_report.py](memory_report.py#L1)**: Memory Report Plugin (Action). @DEP: src/ndoc/brain/vectordb.py, src/ndoc/core/__init__.py, src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/sdk/interfaces.py, ...
    *   `@API`
        *   `PUB:` CLS **MemoryReportPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[mind_map.py](mind_map.py#L1)**: Mind Map Plugin (Action). @DEP: src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/parsing/__init__.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **MindMapPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[scanner.py](scanner.py#L1)**: Syntax Analysis Plugin (Sensor). @DEP: src/ndoc/core/logger.py, src/ndoc/parsing/__init__.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **SyntaxAnalysisPlugin**
            *   `PUB:` MET **ndoc_process_syntax**`(self, entity: Entity) -> Dict[str, Any]`
*   **[stats_report.py](stats_report.py#L1)**: Stats Report Plugin (Action). @DEP: src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `PUB:` CLS **StatsReportPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[status.py](status.py#L1)**: Status Report Plugin (Ported from Status Flow). @DEP: src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/sdk/interfaces.py, src/ndoc/sdk/models.py
    *   `@API`
        *   `VAL->` VAR **TODO_PATTERN**` = re.compile(r'#\s*(TODO|FIXME|XXX):\s*(.*)', re.IGNORECASE)`
        *   `PUB:` CLS **StatusPlugin**
            *   `PUB:` MET **ndoc_process_syntax**`(self, entity: Entity) -> Dict[str, Any]`
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
*   **[syntax_manual.py](syntax_manual.py#L1)**: Syntax Manual Plugin (Action). @DEP: src/ndoc/core/__init__.py, src/ndoc/core/templates.py, src/ndoc/kernel/context.py, src/ndoc/sdk/interfaces.py
    *   `@API`
        *   `PUB:` CLS **SyntaxManualPlugin**
            *   `PUB:` MET **ndoc_generate_docs**`(self, context: KernelContext)`
<!-- NIKI_AUTO_Context_END -->

---
*Generated by Niki-docAI*
