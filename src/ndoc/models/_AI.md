# Context: models
> @CONTEXT: Local | models | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 02:47:30

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Models: Data Definitions.
*   **[config.py](config.py#L1)**: Models: Configuration definitions. @DEP: dataclasses, typing.Optional, dataclasses.dataclass, typing, typing.List, pathlib.Path, dataclasses.field, pathlib
    *   `@API`
        *   `PUB:` CLS **ScanConfig**
            *   `VAL->` VAR **root_path**`: Path`
            *   `VAL->` VAR **ignore_patterns**`: List[str] = field(default_factory=lambda: [
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".idea",
        ".vscode",
        "dist",
        "build",
        "ndoc_legacy" # Explicitly ignore legacy
    ])`
            *   `VAL->` VAR **extensions**`: List[str] = field(default_factory=list)`
        *   `PUB:` CLS **ProjectConfig**
            *   `VAL->` VAR **scan**`: ScanConfig`
            *   `VAL->` VAR **name**`: str = "Project"`
            *   `VAL->` VAR **version**`: str = "0.1.0"`
*   **[context.py](context.py#L1)**: Models: Context Models. @DEP: dataclasses, typing.Optional, typing.Dict, dataclasses.dataclass, typing, typing.List, pathlib.Path, dataclasses.field, pathlib, typing.Any
    *   `@API`
        *   `PUB:` CLS **Tag**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **args**`: List[str] = field(default_factory=list)`
            *   `VAL->` VAR **line**`: int = 0`
            *   `VAL->` VAR **raw**`: str = ""`
        *   `PUB:` CLS **Section**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **content**`: str`
            *   `VAL->` VAR **raw**`: str`
            *   `VAL->` VAR **start_pos**`: int`
            *   `VAL->` VAR **end_pos**`: int`
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
            *   `GET->` PRP **is_public**`(self) -> bool`
        *   `PUB:` CLS **FileContext**
            *   `VAL->` VAR **path**`: Path`
            *   `VAL->` VAR **rel_path**`: str`
            *   `VAL->` VAR **content**`: Optional[str] = None`
            *   `VAL->` VAR **tags**`: List[Tag] = field(default_factory=list)`
            *   `VAL->` VAR **sections**`: Dict[str, Section] = field(default_factory=dict)`
            *   `VAL->` VAR **symbols**`: List[Symbol] = field(default_factory=list)`
            *   `VAL->` VAR **docstring**`: Optional[str] = None`
            *   `VAL->` VAR **is_core**`: bool = False`
            *   `VAL->` VAR **ast_tree**`: Any = None`
            *   `VAL->` VAR **title**`: Optional[str] = None`
            *   `VAL->` VAR **description**`: Optional[str] = None`
            *   `GET->` PRP **has_content**`(self) -> bool`
        *   `PUB:` CLS **DirectoryContext**
            *   `VAL->` VAR **path**`: Path`
            *   `VAL->` VAR **files**`: List[FileContext] = field(default_factory=list)`
            *   `VAL->` VAR **subdirs**`: List[Path] = field(default_factory=list)`
            *   `GET->` PRP **name**`(self) -> str`
<!-- NIKI_AUTO_Context_END -->
