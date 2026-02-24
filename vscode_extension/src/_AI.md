# Context: src
> @CONTEXT: Local | src | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 15:40:41

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[extension.ts](extension.ts#L1)**
    *   `@API`
        *   `PUB:` FUN **activate**`(context: ExtensionContext)`
        *   `VAL->` VAR **serverArgs**` = ['-m', 'ndoc', 'server']`
        *   `VAL->` VAR **devRoot**` = "e:\\work\\appcodes\\nk_doc_ai"`
        *   `VAL->` VAR **serverOptions**` = {
        command: serverExecutable,
        args: serverArg...`
        *   `VAL->` VAR **clientOptions**` = {
        documentSelector: [
            { scheme: 'file', ...`
        *   `PUB:` FUN **deactivate**`() -> : Thenable<void> | undefined`
<!-- NIKI_AUTO_Context_END -->
