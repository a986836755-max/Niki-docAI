# Project Rules
> @CONTEXT: Configuration | @TAGS: @CONFIG @RULES

<!-- 
@CONFIG_DECLARATION
This file serves as the central configuration for Niki-docAI. 
Edit this file to customize scanning behavior, documentation style, and special directory handling.
此文件作为 Niki-docAI 的中央配置文件。编辑此文件以自定义扫描行为、文档风格和特殊目录处理。
-->

## Scanning Rules (扫描规则)
> 定义哪些文件应该被忽略或包含。

- `!IGNORE`: .git, .vscode, .idea, __pycache__, node_modules, dist, build, .venv, venv
- `!INCLUDE`: .py, .md, .json, .js, .ts, .html, .css, .yml, .yaml, .toml

## Special Keywords (特殊关键字)
> 用于控制特定目录的文档生成行为。

- `@AGGREGATE`: **Recursive Aggregation**. 
    - Effect: 当目录包含此标记时，不为子目录生成单独的 `_AI.md`，而是将其内容递归聚合到父级 `_AI.md` 中。
    - Use Case: 适用于紧密耦合的模块或小文件集合（如 `utils/`, `models/`）。
- `@CHECK_IGNORE`: **Audit Ignore**. 
    - Effect: 当目录包含此标记时，完全跳过该目录及其子目录的 `_AI.md` 生成。
    - Use Case: 适用于不需要 AI 上下文的第三方库或生成代码（如 `vendors/`, `dist/`）。

## Documentation Style (文档风格)
> 定义生成的文档样式。

- `!LANG`: Chinese (zh-CN)

## Statistics Configuration (统计配置)
> 定义项目统计的更新策略。

- `!STATS_INTERVAL`: 1h  # Minimum interval between auto-updates

