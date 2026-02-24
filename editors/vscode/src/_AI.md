# Context: src
> @CONTEXT: Local | src | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 14:59:54

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[extension.ts](extension.ts#L1)**
    *   `@API`
        *   `PUB:` FUN **activate**`(context: vscode.ExtensionContext)`
        *   `VAL->` VAR **serverOptions**` = {
        command: pythonPath,
        args: ['-m', 'ndoc.ls...`
        *   `VAL->` VAR **clientOptions**` = {
        documentSelector: [
            { scheme: 'file', ...`
        *   `PUB:` FUN **deactivate**`() -> : Thenable<void> | undefined`
<!-- NIKI_AUTO_Context_END -->
