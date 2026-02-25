# Context: src
> @CONTEXT: Local | src | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:45

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[extension.ts](extension.ts#L1)**
    *   `@API`
        *   `PUB:` FUN **activate**`(context: ExtensionContext)` [🔗28]
        *   `VAL->` VAR **serverArgs**` = ['-m', 'ndoc', 'server']` [🔗12]
        *   `VAL->` VAR **env**` = { ...process.env }` [🔗1844]
        *   `VAL->` VAR **devRoot**` = "e:\\work\\appcodes\\nk_doc_ai"` [🔗16]
        *   `VAL->` VAR **serverOptions**` = {
        command: serverExecutable,
        args: [...serve...` [🔗14]
        *   `VAL->` VAR **clientOptions**` = {
        documentSelector: [
            { scheme: 'file', ...` [🔗70]
        *   `PUB:` FUN **deactivate**`() -> : Thenable<void> | undefined` [🔗18]
<!-- NIKI_AUTO_Context_END -->
