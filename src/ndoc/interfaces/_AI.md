# Context: interfaces
> @CONTEXT: Local | interfaces | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:50

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """ @DEP: lsp
*   **[lsp.py](lsp.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: re, models.symbol, typing, models.config, pathlib, parsing, core, flows
    *   `@API`
        *   `PUB:` CLS **LSPService** [🔗14]
            *   `PRV:` MET __init__`(self, root: Path)` [🔗44]
            *   `PUB:` MET **index_project**`(self, files: List[Path])` [🔗5]
            *   `PUB:` MET **find_definitions**`(self, name: str) -> List[Symbol]` [🔗3]
            *   `PUB:` MET **get_reference_count**`(self, name: str) -> int` [🔗4]
            *   `PUB:` MET **get_context_for_file**`(self, file_path: Path) -> str` [🔗2]
            *   `PUB:` MET **find_references**`(self, name: str) -> List[Dict[str, Any]]` [🔗3]
        *   `VAL->` VAR _INSTANCE`: Optional[LSPService] = None` [🔗7]
        *   `PUB:` FUN **get_service**`(root: Path) -> LSPService` [🔗11]
<!-- NIKI_AUTO_Context_END -->
