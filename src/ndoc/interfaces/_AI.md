# Context: interfaces
> @CONTEXT: Local | interfaces | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 12:27:57

## !RULE
<!-- Add local rules here -->
*   **Thinking Context Scope**: `LSPService.get_context_for_file` 必须聚合从项目根到文件目录的 `_AI.md` 规则段，输出可直接用于 IDE 展示的 Markdown。
*   **Context Cache**: `LSPService` 需要缓存规则上下文并基于 `_AI.md` 的 mtime 做增量失效，避免重复 IO。
*   **Index Coverage**: `LSPService.index_project` 必须尊重传入的文件列表，避免扫描超出 IDE 作用域。
*   **Index Capability Prep**: `LSPService.index_project` 在扫描前需根据扩展名确保对应语言能力可用，但不应在 IDE 线程中触发自动安装。

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Interfaces: Entry Points. @DEP: .lsp @DEP: .lsp
*   **[lsp.py](lsp.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: ..core, ..core.capabilities, ..flows, ..models.symbol, ..parsing, ... @DEP: ..parsing, ..parsing.langs, re, ..core.capabilities, ..core, typing, ..models.symbol, ..flows ...
<!-- NIKI_AUTO_Context_END -->
