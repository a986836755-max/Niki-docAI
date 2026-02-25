# Context: models
> @CONTEXT: Local | models | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:51

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Core Context Models**: `context.py` defines `FileContext`, `DirectoryContext`, and `Symbol`. These are the primary data structures for documentation generation.
*   **Symbol Structure**: `Symbol` captures language-agnostic metadata (kind, visibility, line number) and now includes `test_usages` to link definitions to test cases.
*   **Symbol Refactoring**: `Symbol` class has been moved to `ndoc.models.symbol` to reduce coupling and improve maintainability.

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """
*   **[config.py](config.py#L1)**: """ @DEP: pathlib, dataclasses, typing
    *   `@API`
        *   `PUB:` CLS **ScanConfig** [🔗15] ↳ Usage: [tests/test_capability_flow.py#L15]
            *   `VAL->` VAR **root_path**`: Path` [🔗136]
            *   `VAL->` VAR **ignore_patterns**`: List[str] = field(default_factory=lambda: [
        ".git",
        "__p...` [🔗97]
            *   `VAL->` VAR **extensions**`: List[str] = field(default_factory=list)` [🔗2175]
        *   `PUB:` CLS **ProjectConfig** [🔗123] ↳ Usage: [tests/test_capability_flow.py#L15]
            *   `VAL->` VAR **scan**`: ScanConfig` [🔗280]
            *   `VAL->` VAR **name**`: str = "Project"` [🔗25070]
            *   `VAL->` VAR **version**`: str = "0.1.0"` [🔗6250]
*   **[context.py](context.py#L1)**: """ @DEP: pathlib, dataclasses, typing, symbol
    *   `@API`
        *   `PUB:` CLS **Section** [🔗78]
            *   `VAL->` VAR **name**`: str` [🔗25070]
            *   `VAL->` VAR **content**`: str` [🔗2268]
            *   `VAL->` VAR **raw**`: str` [🔗683]
            *   `VAL->` VAR **start_pos**`: int` [🔗4]
            *   `VAL->` VAR **end_pos**`: int` [🔗3]
        *   `PUB:` CLS **FileContext** [🔗42]
            *   `VAL->` VAR **path**`: Path` [🔗8904]
            *   `VAL->` VAR **rel_path**`: str` [🔗64]
            *   `VAL->` VAR **content**`: Optional[str] = None` [🔗2268]
            *   `VAL->` VAR **tags**`: List[Tag] = field(default_factory=list)` [🔗855]
            *   `VAL->` VAR **sections**`: Dict[str, Section] = field(default_factory=dict)` [🔗107]
            *   `VAL->` VAR **symbols**`: List[Symbol] = field(default_factory=list)` [🔗702]
            *   `VAL->` VAR **docstring**`: Optional[str] = None` [🔗71]
            *   `VAL->` VAR **description**`: Optional[str] = None` [🔗1957]
            *   `VAL->` VAR **is_core**`: bool = False` [🔗18]
            *   `VAL->` VAR **memories**`: List[Dict[str, Any]] = field(default_factory=list)` [🔗32]
            *   `VAL->` VAR **ast_tree**`: Any = None` [🔗2]
            *   `VAL->` VAR **title**`: Optional[str] = None` [🔗858]
            *   `VAL->` VAR **description**`: Optional[str] = None` [🔗1957]
            *   `GET->` PRP **has_content**`(self) -> bool` [🔗6]
        *   `PUB:` CLS **DirectoryContext** [🔗10]
            *   `VAL->` VAR **path**`: Path` [🔗8904]
            *   `VAL->` VAR **files**`: List[FileContext] = field(default_factory=list)` [🔗2608]
            *   `VAL->` VAR **subdirs**`: List[Path] = field(default_factory=list)` [🔗18]
            *   `GET->` PRP **name**`(self) -> str` [🔗25070]
*   **[symbol.py](symbol.py#L1)**: """ @DEP: dataclasses, typing
    *   `@API`
        *   `PUB:` CLS **Tag** [🔗174]
            *   `VAL->` VAR **name**`: str` [🔗25070]
            *   `VAL->` VAR **args**`: List[str] = field(default_factory=list)` [🔗3868]
            *   `VAL->` VAR **line**`: int = 0` [🔗3227]
            *   `VAL->` VAR **raw**`: str = ""` [🔗683]
            *   `VAL->` VAR **attributes**`: Dict[str, Any] = field(default_factory=dict)` [🔗1605]
        *   `PUB:` CLS **Symbol** [🔗1659]
            *   `VAL->` VAR **name**`: str` [🔗25070]
            *   `VAL->` VAR **kind**`: str` [🔗10695]
            *   `VAL->` VAR **line**`: int` [🔗3227]
            *   `VAL->` VAR **docstring**`: Optional[str] = None` [🔗71]
            *   `VAL->` VAR **signature**`: Optional[str] = None` [🔗2464]
            *   `VAL->` VAR **parent**`: Optional[str] = None` [🔗8153]
            *   `VAL->` VAR **is_core**`: bool = False` [🔗18]
            *   `VAL->` VAR **visibility**`: str = "public"` [🔗194]
            *   `VAL->` VAR **lang**`: str = "unknown"` [🔗139]
            *   `VAL->` VAR **decorators**`: List[str] = field(default_factory=list)` [🔗189]
            *   `VAL->` VAR **bases**`: List[str] = field(default_factory=list)` [🔗29]
            *   `VAL->` VAR **full_content**`: str = ""` [🔗9]
            *   `VAL->` VAR **path**`: Optional[str] = None` [🔗8904]
            *   `VAL->` VAR **tags**`: List[Tag] = field(default_factory=list)` [🔗855]
            *   `VAL->` VAR **test_usages**`: List[Dict[str, Any]] = field(default_factory=list)` [🔗11]
            *   `GET->` PRP **is_public**`(self) -> bool` [🔗27]
<!-- NIKI_AUTO_Context_END -->
