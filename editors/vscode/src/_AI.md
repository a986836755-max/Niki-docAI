# Context: src
> @CONTEXT: Local | src | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 20:34:52

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[extension.ts](extension.ts#L1)** @DEP: fs, path, vscode
    *   `@API`
        *   `PUB:` FUN **activate**`(context: ExtensionContext)`
        *   `VAL->` VAR **serverArgs**` = ['-m', 'ndoc', 'server']`
        *   `VAL->` VAR **env**` = { ...process.env }`
        *   `VAL->` VAR **devRoot**` = "e:\\work\\appcodes\\nk_doc_ai"`
        *   `VAL->` VAR **serverOptions**` = {
        command: serverExecutable,
        args: [...serve...`
        *   `VAL->` VAR **clientOptions**` = {
        documentSelector: [
            { scheme: 'file', ...`
        *   `PUB:` FUN **deactivate**`() -> : Thenable<void> | undefined`
<!-- NIKI_AUTO_Context_END -->
