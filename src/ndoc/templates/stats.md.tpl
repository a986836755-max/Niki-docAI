## 核心指标 (Core Metrics)

| 指标 (Metric) | 数值 (Value) | 说明 (Description) |
| :--- | :--- | :--- |
| **总文件数** | {{ total_files }} | 包含代码和文档 |
| **总行数** | {{ total_lines }} | 代码 + 文档总行数 |
| **项目体积** | {{ total_size_kb | round(2) }} KB | 磁盘占用 |
| **预估 Token** | ~{{ estimated_tokens }} | 全局上下文开销 (Size/4) |

## AI 上下文统计 (AI Context Stats)

| 上下文类型 | 数值 | 说明 |
| :--- | :--- | :--- |
| **AI 文档数** | {{ ai_doc_files }} | `_AI.md` 文件数量 |
| **AI 文档行数** | {{ ai_doc_lines }} | 纯上下文描述行数 |
| **AI 预估 Token** | ~{{ ai_estimated_tokens }} | 上下文注入开销 |
| **AI 覆盖率** | {{ ai_coverage | round(1) }}% | 覆盖目录数 / 总扫描目录数 |

## 目录扫描详情 (Directory Scan)

- **已扫描目录**: {{ dirs_with_ai }} / {{ total_dirs_scanned }}
- **源码文件**: {{ src_files }} ({{ src_lines }} 行)
- **文档文件**: {{ total_doc_files }} ({{ total_doc_lines }} 行)
- **文档/代码比**: {{ ratio | round(1) }}%

## 健康度诊断 (Health Check)

- **AI 覆盖率**: {{ health_ai_coverage }}
- **文档密度**: {{ health_doc_ratio }}
