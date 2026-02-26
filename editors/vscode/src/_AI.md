# Context: src
> @CONTEXT: Local | src | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:27:51

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->
*   **Context Command Bridge**: 扩展必须通过 `workspace/executeCommand` 调用 `ndoc.getThinkingContext`，并在输出面板展示结果。
*   **Restart Safety**: `ndoc.restartServer` 需要完整重启 LanguageClient，确保 LSP 异常时可恢复。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[extension.ts](extension.ts#L1)** @DEP: fs, path, vscode @DEP: fs, path, vscode
<!-- NIKI_AUTO_Context_END -->
