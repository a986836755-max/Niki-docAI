# Project Status Board
> @CONTEXT: Status | Time View
> 最后更新 (Last Updated): 2026-02-26 12:28:17

## 1. Active Sprint (Sprint Plan)
> Manually add your sprint goals here.
*   [ ] Example Task 1

## 2. Code Tasks (Auto-aggregated)
<!-- NIKI_TODO_START -->
*   🔴 **FIXME** [src/ndoc/flows/status_flow.py:43](src/ndoc/flows/status_flow.py#L43): ": "🔴", # High
*   🔴 **FIXME** [src/ndoc/flows/status_flow.py:82](src/ndoc/flows/status_flow.py#L82): ": 0, "XXX": 1, "HACK": 2, "TODO": 3, "NOTE": 4}
*   🟣 **XXX** [src/ndoc/atoms/_AI.md:10](src/ndoc/atoms/_AI.md#L10): ')` to ensure on-demand loading and auto-provisioning of dependencies.
*   🟣 **XXX** [src/ndoc/flows/status_flow.py:44](src/ndoc/flows/status_flow.py#L44): ": "🟣",   # Critical
*   🚧 **HACK** [src/ndoc/flows/status_flow.py:45](src/ndoc/flows/status_flow.py#L45): ": "🚧",  # Warning
*   🔵 **TODO** [_SYNTAX.md:55](_SYNTAX.md#L55): `: **Plan**. 待办/债务 (Tasks/Debt). 取代 `@BACKLOG`, `@PLAN`.
*   🔵 **TODO** [src/ndoc/_AI.md:21](src/ndoc/_AI.md#L21): ` and `stats` commands must route through `status` and shared status logic.
*   🔵 **TODO** [src/ndoc/_AI.md:22](src/ndoc/_AI.md#L22): `/`stats` 为兼容转发。
*   🔵 **TODO** [src/ndoc/core/capabilities.py:378](src/ndoc/core/capabilities.py#L378): Use a proper logger
*   🔵 **TODO** [src/ndoc/core/fs.py:56](src/ndoc/core/fs.py#L56): Advanced directory filtering with gitignore
*   🔵 **TODO** [src/ndoc/entry.py:125](src/ndoc/entry.py#L125): ", "deps", "symbols", "data", "inject", "all", "watch", "doctor", "init", "verify", "clean", "stats", "update", "archive", "lsp", "prompt", "server", "check", "arch", "status", "help", "adr", "mind", "lesson", "impact", "skeleton", "search", "lint", "typecheck"], help="Command to execute")
*   🔵 **TODO** [src/ndoc/entry.py:207](src/ndoc/entry.py#L207): ":
*   🔵 **TODO** [src/ndoc/entry.py:208](src/ndoc/entry.py#L208): ' command is deprecated. Using 'status' instead.")
*   🔵 **TODO** [src/ndoc/flows/_AI.md:13](src/ndoc/flows/_AI.md#L13): /Stats aggregation; legacy flows must delegate without duplicating logic.
*   🔵 **TODO** [src/ndoc/flows/_AI.md:14](src/ndoc/flows/_AI.md#L14): /Stats 聚合统一由 `status_flow` 生成与维护。
*   🔵 **TODO** [src/ndoc/flows/prompt_flow.py:167](src/ndoc/flows/prompt_flow.py#L167): Implement dependency API extraction
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:14](src/ndoc/flows/status_flow.py#L14): ) 和 Stats Flow。
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:30](src/ndoc/flows/status_flow.py#L30): /NEXT LOGIC ---
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:36](src/ndoc/flows/status_flow.py#L36): , FIXME, etc.
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:46](src/ndoc/flows/status_flow.py#L46): ": "🔵",  # Medium
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:85](src/ndoc/flows/status_flow.py#L85): in sorted_todos:
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:86](src/ndoc/flows/status_flow.py#L86): .file_path.relative_to(root).as_posix()
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:87](src/ndoc/flows/status_flow.py#L87): .line}]({rel_path}#L{todo.line})"
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:88](src/ndoc/flows/status_flow.py#L88): .priority_icon} **{todo.type}** {link}: {todo.content}"
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:157](src/ndoc/flows/status_flow.py#L157): List
*   🔵 **TODO** [src/ndoc/flows/status_flow.py:455](src/ndoc/flows/status_flow.py#L455): section
*   🔵 **TODO** [src/ndoc/flows/syntax_flow.py:82](src/ndoc/flows/syntax_flow.py#L82): `: **Debt**. 已知问题 (Known issue).
*   🔵 **TODO** [src/ndoc/flows/syntax_flow.py:104](src/ndoc/flows/syntax_flow.py#L104): **. 任务聚合开始 (Start of task aggregation).
*   🔵 **TODO** [src/ndoc/flows/syntax_flow.py:111](src/ndoc/flows/syntax_flow.py#L111): `: **Unreviewed**. 发现于 [_NEXT.md] (Found in ...).
*   🔵 **TODO** [src/ndoc/flows/todo_flow.py:12](src/ndoc/flows/todo_flow.py#L12): Aggregation.
*   🔵 **TODO** [src/ndoc/flows/todo_flow.py:13](src/ndoc/flows/todo_flow.py#L13): /FIXME 标记到 _NEXT.md。
*   🔵 **TODO** [src/ndoc/lsp_server.py:98](src/ndoc/lsp_server.py#L98): Refactor scanner to accept string content.
*   🔵 **TODO** [src/ndoc/parsing/scanner.py:266](src/ndoc/parsing/scanner.py#L266): /FIXME 等标记.
*   🔵 **TODO** [src/ndoc/parsing/scanner.py:272](src/ndoc/parsing/scanner.py#L272): (#task-123): fix this
*   🔵 **TODO** [src/ndoc/parsing/scanner.py:274](src/ndoc/parsing/scanner.py#L274): |FIXME|XXX|HACK|NOTE|DONE)\b(?:\(#([\w-]+)\))?:?\s*(.*)$", re.MULTILINE
*   🔵 **TODO** [src/ndoc/parsing/scanner.py:456](src/ndoc/parsing/scanner.py#L456): , @DECISION, @INTENT, @LESSON.
*   🔵 **TODO** [src/ndoc/parsing/scanner.py:465](src/ndoc/parsing/scanner.py#L465): |FIXME|HACK|NOTE|XXX)\s*:?\s*(.*?)$", re.MULTILINE | re.IGNORECASE)
*   🔵 **TODO** [src/ndoc/parsing/scanner.py:573](src/ndoc/parsing/scanner.py#L573): Move to text_utils or dedicated todo parser
*   🔵 **TODO** [src/ndoc/parsing/scanner.py:574](src/ndoc/parsing/scanner.py#L574): ... or FIXME: ...
*   🔵 **TODO** [src/ndoc/parsing/scanner.py:576](src/ndoc/parsing/scanner.py#L576): |FIXME|XXX|HACK|NOTE)\b[:\s]*(.*)")
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:41](temp_build_dart/tree-sitter-dart/grammar.js#L41): general things to add
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:44](temp_build_dart/tree-sitter-dart/grammar.js#L44): type test operators: as, is, and is!
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:45](temp_build_dart/tree-sitter-dart/grammar.js#L45): assignment operators: ??=, and ~/=
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:46](temp_build_dart/tree-sitter-dart/grammar.js#L46): ?? operator
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:47](temp_build_dart/tree-sitter-dart/grammar.js#L47): cascade notation: dot dot accesses each object
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:48](temp_build_dart/tree-sitter-dart/grammar.js#L48): conditional member access: blah?.foo
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:49](temp_build_dart/tree-sitter-dart/grammar.js#L49): rethrow keyword
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:50](temp_build_dart/tree-sitter-dart/grammar.js#L50): override operator notations
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:51](temp_build_dart/tree-sitter-dart/grammar.js#L51): correct import statements to be strings
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:52](temp_build_dart/tree-sitter-dart/grammar.js#L52): sync* and async* functions, plus yields
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:647](temp_build_dart/tree-sitter-dart/grammar.js#L647): use the op names in place of these.
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:830](temp_build_dart/tree-sitter-dart/grammar.js#L830): The spec says optional but it breaks tests, and I'm not sure in a good way.
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:1199](temp_build_dart/tree-sitter-dart/grammar.js#L1199): add rethrow statement.
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:1439](temp_build_dart/tree-sitter-dart/grammar.js#L1439): remove unnecessary annotation related stuff.
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:1789](temp_build_dart/tree-sitter-dart/grammar.js#L1789): This should only work with native?
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:1873](temp_build_dart/tree-sitter-dart/grammar.js#L1873): add in the 'late' keyword from the informal draft spec:
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/grammar.js:2697](temp_build_dart/tree-sitter-dart/grammar.js#L2697): add support for triple-slash comments as a special category.
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/queries/highlights.scm:5](temp_build_dart/tree-sitter-dart/queries/highlights.scm#L5): does not work
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/queries/highlights.scm:78](temp_build_dart/tree-sitter-dart/queries/highlights.scm#L78): does not work
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/queries/highlights.scm:117](temp_build_dart/tree-sitter-dart/queries/highlights.scm#L117): add method/call_expression to grammar and
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/queries/highlights.scm:142](temp_build_dart/tree-sitter-dart/queries/highlights.scm#L142): inaccessbile nodes
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/queries/highlights.scm:161](temp_build_dart/tree-sitter-dart/queries/highlights.scm#L161): "rethrow" @keyword
*   🔵 **TODO** [temp_build_dart/tree-sitter-dart/test/corpus/flutter.txt:104](temp_build_dart/tree-sitter-dart/test/corpus/flutter.txt#L104): implement build
*   ℹ️ **NOTE** [_DOGFOOD.md:35](_DOGFOOD.md#L35): In a real Python code change scenario, it would list specific `test_*.py` files to run.*
*   ℹ️ **NOTE** [editors/vscode/src/extension.ts:126](editors/vscode/src/extension.ts#L126): client.sendRequest('workspace/executeCommand', ...) is the standard way
*   ℹ️ **NOTE** [src/ndoc/core/capabilities.py:31](src/ndoc/core/capabilities.py#L31): Keys should match what is used in import tree_sitter_{key}
*   ℹ️ **NOTE** [src/ndoc/flows/arch_flow.py:95](src/ndoc/flows/arch_flow.py#L95): graph keys are file paths now, not modules.
*   ℹ️ **NOTE** [src/ndoc/flows/check_flow.py:59](src/ndoc/flows/check_flow.py#L59): Ideally we should use a persistent index, but for now we rebuild.
*   ℹ️ **NOTE** [src/ndoc/flows/deps_flow.py:710](src/ndoc/flows/deps_flow.py#L710): **: This view is aggregated by module/package. Detailed per-file dependencies are available in local `_AI.md` files.
*   ℹ️ **NOTE** [src/ndoc/flows/doctor_flow.py:145](src/ndoc/flows/doctor_flow.py#L145): For doctor flow, we might want to check existing installation status first
*   ℹ️ **NOTE** [src/ndoc/flows/status_flow.py:47](src/ndoc/flows/status_flow.py#L47): ": "ℹ️"   # Info
*   ℹ️ **NOTE** [src/ndoc/lsp_server.py:96](src/ndoc/lsp_server.py#L96): We should scan content from memory (document.source) to be real-time
*   ℹ️ **NOTE** [src/ndoc/parsing/ast/symbols.py:59](src/ndoc/parsing/ast/symbols.py#L59): We'll update the loop at the end to include path if available
*   ℹ️ **NOTE** [src/ndoc/parsing/scanner.py:141](src/ndoc/parsing/scanner.py#L141): scan_file_content is defined in this module
*   ℹ️ **NOTE** [src/ndoc/parsing/scanner.py:560](src/ndoc/parsing/scanner.py#L560): text_utils.extract_tags_from_text is regex based, works for comments in any language
*   ℹ️ **NOTE** [tests/test_ast.py:108](tests/test_ast.py#L108): 'name' might be ambiguous if multiple classes have it, but in fixture User.name is unique top level? No, it's inside User.
*   ℹ️ **NOTE** [tests/test_scanner.py:36](tests/test_scanner.py#L36): just a note"
*   ℹ️ **NOTE** [tests/test_scanner.py:40](tests/test_scanner.py#L40): "
<!-- NIKI_TODO_END -->

<!-- NIKI_STATS_START -->
## 3. Project Health (Metrics)
| Metric | Value | Description |
| :--- | :--- | :--- |
| **Files** | 157 | Total file count |
| **AI Context** | 24 nodes | _AI.md count |
| **AI Coverage** | 61.5% | Directory coverage |
| **Doc Ratio** | 9.6% | Context lines / Code lines |

## 4. Architecture Health
| Metric | Status | Details |
| :--- | :--- | :--- |
| **Circular Deps** | ✅ None | Dependency cycles |

<!-- NIKI_STATS_END -->

---
*Generated by Niki-docAI*
