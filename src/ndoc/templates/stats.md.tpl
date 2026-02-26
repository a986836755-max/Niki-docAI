## 核心指标 (Core Metrics)

| 指标 (Metric) | 数值 (Value) | 说明 (Description) |
| :--- | :--- | :--- |
| **总文件数** | {total_files} | 包含代码和文档 |
| **总行数** | {total_lines} | 代码 + 文档总行数 |
| **项目体积** | {total_size_kb:.2f} KB | 磁盘占用 |
| **预估 Token** | ~{estimated_tokens} | 全局上下文开销 (Size/4) |

## AI 上下文统计 (AI Context Stats)
> 针对 `_AI.md` 递归上下文文件的专项统计。

| 指标 (Metric) | 数值 (Value) | 说明 (Description) |
| :--- | :--- | :--- |
| **_AI.md 文件数** | {ai_doc_files} | 局部上下文节点数 |
| **_AI.md 总行数** | {ai_doc_lines} | 上下文总厚度 |
| **_AI.md Token** | ~{ai_estimated_tokens} | 上下文 Token 开销 |
| **目录覆盖率** | {ai_coverage:.1f}% ({dirs_with_ai}/{total_dirs_scanned}) | 包含 `_AI.md` 的目录比例 |

## 全局组成 (Global Composition)

| 类型 (Type) | 文件数 (Files) | 行数 (Lines) | 占比 (Ratio) |
| :--- | :--- | :--- | :--- |
| **源代码 (Source)** | {src_files} | {src_lines} | - |
| **文档 (Docs)** | {total_doc_files} | {total_doc_lines} | {ratio:.1f}% (Doc/Code) |

## 健康度检查 (Health Check)

- **AI 上下文覆盖率**: {ai_coverage:.1f}%
  - {health_ai_coverage}
- **文档/代码比率**: {ratio:.1f}%
  - {health_doc_ratio}
