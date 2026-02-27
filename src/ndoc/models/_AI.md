# Context: models
> @CONTEXT: Recursive Context | models | @TAGS: @AI
> 最后更新 (Last Updated): 2026-02-27 18:00:27

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->



## @FILES
<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[_AI.md](_AI.md#L1)**: Context: models
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START>
*   **[config.py](config.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: dataclasses, pathlib, typing
    *   `@API`
        *   `PUB:` CLS **ScanConfig**
            *   `VAL->` VAR **root_path**`: Path`
            *   `VAL->` VAR **ignore_patterns**`: List[str] = field(default_factory=lambda: [
        ".git",
        "__p...`
            *   `VAL->` VAR **extensions**`: List[str] = field(default_factory=list)`
        *   `PUB:` CLS **TemplateConfig**
            *   `VAL->` VAR **base_dir**`: Optional[Path] = None`
            *   `VAL->` VAR **overrides**`: Dict[str, Path] = field(default_factory=dict)`
            *   `VAL->` VAR **header**`: str = "components/doc_header.tpl"`
            *   `VAL->` VAR **footer**`: str = "components/doc_footer.tpl"`
        *   `PUB:` CLS **ProjectConfig**
            *   `VAL->` VAR **scan**`: ScanConfig`
            *   `VAL->` VAR **template**`: TemplateConfig = field(default_factory=TemplateConfig)`
            *   `VAL->` VAR **lint_commands**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **typecheck_commands**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **name**`: str = "Project"`
            *   `VAL->` VAR **version**`: str = "0.1.0"`
*   **[context.py](context.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: src/ndoc/models/symbol.py
    *   `@API`
        *   `PUB:` CLS **Section**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **content**`: str`
            *   `VAL->` VAR **raw**`: str`
            *   `VAL->` VAR **start_pos**`: int`
            *   `VAL->` VAR **end_pos**`: int`
        *   `PUB:` CLS **FileContext**
            *   `VAL->` VAR **path**`: Path`
            *   `VAL->` VAR **rel_path**`: str`
            *   `VAL->` VAR **content**`: Optional[str] = None`
            *   `VAL->` VAR **tags**`: List[Tag] = field(default_factory=list)`
            *   `VAL->` VAR **sections**`: Dict[str, Section] = field(default_factory=dict)`
            *   `VAL->` VAR **symbols**`: List[Symbol] = field(default_factory=list)`
            *   `VAL->` VAR **imports**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **docstring**`: Optional[str] = None`
            *   `VAL->` VAR **description**`: Optional[str] = None`
            *   `VAL->` VAR **is_core**`: bool = False`
            *   `VAL->` VAR **memories**`: List[Dict[str, Any]] = field(default_factory=list)`
            *   `VAL->` VAR **ast_tree**`: Any = None`
            *   `VAL->` VAR **title**`: Optional[str] = None`
            *   `VAL->` VAR **description**`: Optional[str] = None`
            *   `GET->` PRP **has_content**`(self) -> bool`
        *   `PUB:` CLS **DirectoryContext**
            *   `VAL->` VAR **path**`: Path`
            *   `VAL->` VAR **files**`: List[FileContext] = field(default_factory=list)`
            *   `VAL->` VAR **subdirs**`: List[Path] = field(default_factory=list)`
            *   `GET->` PRP **name**`(self) -> str`
*   **[map.py](map.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: dataclasses, pathlib, typing
    *   `@API`
        *   `PUB:` CLS **MapContext**
            *   `VAL->` VAR **root**`: Path`
            *   `VAL->` VAR **ignore_patterns**`: List[str]`
*   **[scan.py](scan.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: src/ndoc/models/context.py, src/ndoc/models/symbol.py
    *   `@API`
        *   `PUB:` CLS **TokenRule**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **pattern**`: Pattern`
            *   `VAL->` VAR **group_map**`: Dict[str, int]`
        *   `PUB:` CLS **ScanResult**
            *   `VAL->` VAR **tags**`: List[Tag] = field(default_factory=list)`
            *   `VAL->` VAR **sections**`: Dict[str, Section] = field(default_factory=dict)`
            *   `VAL->` VAR **symbols**`: List[Symbol] = field(default_factory=list)`
            *   `VAL->` VAR **docstring**`: str = ""`
            *   `VAL->` VAR **summary**`: str = ""`
            *   `VAL->` VAR **todos**`: List[dict] = field(default_factory=list)`
            *   `VAL->` VAR **memories**`: List[dict] = field(default_factory=list)`
            *   `VAL->` VAR **decisions**`: List[dict] = field(default_factory=list)`
            *   `VAL->` VAR **intents**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **lessons**`: List[dict] = field(default_factory=list)`
            *   `VAL->` VAR **calls**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **imports**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **tokens**`: Dict[str, int] = field(default_factory=dict)`
            *   `VAL->` VAR **is_core**`: bool = False`
*   **[status.py](status.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: dataclasses, pathlib, typing
    *   `@API`
        *   `PUB:` CLS **TodoItem**
            *   `VAL->` VAR **file_path**`: Path`
            *   `VAL->` VAR **line**`: int`
            *   `VAL->` VAR **type**`: str`
            *   `VAL->` VAR **content**`: str`
            *   `VAL->` VAR **task_id**`: Optional[str] = None`
            *   `GET->` PRP **priority_icon**`(self) -> str`
*   **[symbol.py](symbol.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: dataclasses, typing
    *   `@API`
        *   `PUB:` CLS **Tag**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **args**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **line**`: int = 0`
            *   `VAL->` VAR **raw**`: str = ""`
            *   `VAL->` VAR **attributes**`: Dict[str, Any] = field(default_factory=dict)`
        *   `PUB:` CLS **Symbol**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **kind**`: str`
            *   `VAL->` VAR **line**`: int`
            *   `VAL->` VAR **docstring**`: Optional[str] = None`
            *   `VAL->` VAR **signature**`: Optional[str] = None`
            *   `VAL->` VAR **parent**`: Optional[str] = None`
            *   `VAL->` VAR **is_core**`: bool = False`
            *   `VAL->` VAR **visibility**`: str = "public"`
            *   `VAL->` VAR **lang**`: str = "unknown"`
            *   `VAL->` VAR **decorators**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **bases**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **full_content**`: str = ""`
            *   `VAL->` VAR **path**`: Optional[str] = None`
            *   `VAL->` VAR **tags**`: List[Tag] = field(default_factory=list)`
            *   `VAL->` VAR **test_usages**`: List[Dict[str, Any]] = field(default_factory=list)`
            *   `GET->` PRP **is_public**`(self) -> bool`
<!-- NIKI_AUTO_Context_END -->

---
*Generated by Niki-docAI*
