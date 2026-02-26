# Context: interfaces
> @CONTEXT: Local | interfaces | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 20:35:01

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Interfaces: Entry Points. @DEP: .lsp
*   **[lsp.py](lsp.py#L1)**: Atoms: Lightweight LSP-like features. @DEP: ..core, ..core.capabilities, ..core.logger, ..models.symbol, ..parsing, ...
    *   `@API`
        *   `PRV:` FUN _extract_rule_block`(content: str) -> List[str]`
        *   `PUB:` CLS **LSPService**
            *   `PRV:` MET __init__`(self, root: Path)`
            *   `PUB:` MET **index_project**`(self, files: Optional[List[Path]] = None, config: Any = None)`
            *   `PUB:` MET **update_file**`(self, file_path: Path)`
            *   `PUB:` MET **find_definitions**`(self, name: str) -> List[Symbol]`
            *   `PUB:` MET **get_reference_count**`(self, name: str) -> int`
            *   `PUB:` MET **invalidate_context_cache**`(self, changed_path: Optional[Path] = None) -> None`
            *   `PRV:` MET _get_ai_rules`(self, ai_path: Path) -> List[str]`
            *   `PUB:` MET **get_context_for_file**`(self, file_path: Path) -> str`
            *   `PUB:` MET **find_references**`(self, name: str) -> List[Dict[str, Any]]`
        *   `VAL->` VAR _INSTANCE`: Optional[LSPService] = None`
        *   `PUB:` FUN **get_service**`(root: Path) -> LSPService`
<!-- NIKI_AUTO_Context_END -->
