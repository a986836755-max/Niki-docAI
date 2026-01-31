# Project Rules
> @CONTEXT: Configuration | @TAGS: @CONFIG @RULES

## Scanning Rules (扫描规则)
> 定义哪些文件应该被忽略或包含。

- `!IGNORE`: .git, .vscode, .idea, __pycache__, node_modules, dist, build, .venv, venv,vendors
- `!INCLUDE`: .py, .cs, .md, .json, .js, .ts, .html, .css, .yml, .yaml, .toml

## Documentation Style (文档风格)
> 定义生成的文档样式。

- `!LANG`: Chinese (zh-CN)

## ALM & Memory Rules (ALM与记忆规则)
> 定义项目生命周期与自动归档规则。

- `MEMORY文档对齐`: 定期更新_MEMORY.md，每当_NEXT.md中一项功能/模块完成，将其归档入_MEMORY.md。
- `交付即更新`: 在完成代码修改后，习惯性运行 `ndoc all`，确保改动被即时索引。

## Special Keywords (特殊关键字)
> 用于控制特定目录的文档生成行为。

- `@AGGREGATE`: **Recursive Aggregation**. 当目录包含此标记时，不为子目录生成单独的 `_AI.md`，而是将其内容递归聚合到父级 `_AI.md` 中。
- `@CHECK_IGNORE`: **Audit Ignore**. 当目录包含此标记时，完全跳过该目录及其子目录的 `_AI.md` 生成。
