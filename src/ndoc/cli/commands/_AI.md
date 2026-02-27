# Context: commands
> @CONTEXT: Recursive Context | commands | @TAGS: @AI
> 最后更新 (Last Updated): 2026-02-27 18:00:27

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->



## @FILES
<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[_AI.md](_AI.md#L1)**: Context: commands
*   **[__init__.py](__init__.py#L1)**: CLI Commands Package. @DEP: .
*   **[adr.py](adr.py#L1)**: Command: Architecture Decision Records (ADR). @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/adr_report.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[all.py](all.py#L1)**: Command: Run All Analysis (ECS Pipeline). @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[arch.py](arch.py#L1)**: Command: Architecture. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/arch_report.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[archive.py](archive.py#L1)**: Command: Archive. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/collector.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[caps.py](caps.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/capability_map.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, auto_install: bool = True) -> bool`
*   **[check.py](check.py#L1)**: Command: Check Constraints. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/checker.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: Optional[str] = None) -> bool`
*   **[clean.py](clean.py#L1)**: Command: Clean. @DEP: src/ndoc/core/cli.py, src/ndoc/flows/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: Optional[str] = None, force: bool = False) -> bool`
*   **[context.py](context.py#L1)**: Command: Context. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/collector.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[data.py](data.py#L1)**: Command: Data Schema Registry. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/collector.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[deps.py](deps.py#L1)**: Command: Dependencies. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/collector.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: Optional[str] = None) -> bool`
*   **[doctor.py](doctor.py#L1)**: Command: Doctor. @DEP: src/ndoc/core/cli.py, src/ndoc/core/logger.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
        *   `PRV:` FUN _pass`(msg: str)`
        *   `PRV:` FUN _fail`(msg: str)`
        *   `PRV:` FUN _warn`(msg: str)`
        *   `PRV:` FUN _check_import`(module_name: str) -> bool`
        *   `PRV:` FUN _check_project_files`(config: ProjectConfig)`
*   **[impact.py](impact.py#L1)**: Command: Impact Analysis. @DEP: src/ndoc/core/cli.py, src/ndoc/core/templates.py, src/ndoc/kernel/bootstrap.py, src/ndoc/models/config.py, src/ndoc/services/impact_service.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[init.py](init.py#L1)**: Command: Init. @DEP: src/ndoc/core/__init__.py, src/ndoc/core/cli.py, src/ndoc/core/templates.py, src/ndoc/flows/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, force: bool = False) -> bool`
        *   `PRV:` FUN _ensure_syntax_file`(root: Path, force: bool = False)`
*   **[inject.py](inject.py#L1)**: Command: Inject. @DEP: src/ndoc/core/cli.py, src/ndoc/flows/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: Optional[str] = None) -> bool`
*   **[lint.py](lint.py#L1)**: Command: Lint. @DEP: src/ndoc/core/cli.py, src/ndoc/flows/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[lsp.py](lsp.py#L1)**: Command: LSP Query. @DEP: src/ndoc/core/__init__.py, src/ndoc/core/cli.py, src/ndoc/core/logger.py, src/ndoc/interfaces/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str) -> bool`
*   **[map.py](map.py#L1)**: Command: Map. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/collector.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[pilot.py](pilot.py#L1)**: Command: Pilot (Legacy Alias). @DEP: src/ndoc/cli/commands/__init__.py, src/ndoc/core/cli.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[prompt.py](prompt.py#L1)**: Command: AI Prompt. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/models/config.py, src/ndoc/services/prompt_service.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, target: str, focus: bool = False) -> bool`
*   **[search.py](search.py#L1)**: Command: Search. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/models/config.py, src/ndoc/services/search_service.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig, query: str, limit: int = 5) -> bool`
*   **[server.py](server.py#L1)**: Command: LSP Server. @DEP: src/ndoc/__init__.py, src/ndoc/core/cli.py
    *   `@API`
        *   `PUB:` FUN **run**`(stdio: bool = True) -> bool`
*   **[skeleton.py](skeleton.py#L1)**: Command: Skeleton Generator. @DEP: src/ndoc/core/__init__.py, src/ndoc/core/cli.py, src/ndoc/parsing/ast/__init__.py
    *   `@API`
        *   `PUB:` FUN **run**`(target: str) -> bool`
*   **[stats.py](stats.py#L1)**: Command: Project Statistics. @DEP: src/ndoc/core/cli.py, src/ndoc/kernel/bootstrap.py, src/ndoc/kernel/context.py, src/ndoc/models/config.py, src/ndoc/plugins/collector.py, ...
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[typecheck.py](typecheck.py#L1)**: Command: Typecheck. @DEP: src/ndoc/core/cli.py, src/ndoc/flows/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[update.py](update.py#L1)**: Command: Update. @DEP: src/ndoc/core/cli.py, src/ndoc/flows/__init__.py
    *   `@API`
        *   `PUB:` FUN **run**`() -> bool`
*   **[verify.py](verify.py#L1)**: Command: Verify. @DEP: src/ndoc/core/cli.py, src/ndoc/flows/__init__.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
*   **[watch.py](watch.py#L1)**: Command: Watch Mode. @DEP: src/ndoc/core/cli.py, src/ndoc/daemon.py, src/ndoc/models/config.py
    *   `@API`
        *   `PUB:` FUN **run**`(config: ProjectConfig) -> bool`
<!-- NIKI_AUTO_Context_END -->

---
*Generated by Niki-docAI*
