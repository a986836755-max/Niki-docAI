"""
Flow: Statistics.
业务流：项目统计 (Project Statistics).
"""
import os
import re
import time
from datetime import datetime
from pathlib import Path
from ndoc.models.config import ProjectConfig
from ndoc.atoms import io

def check_should_update(root_path: Path, force: bool) -> bool:
    if force:
        return True
    
    # 1. Parse Interval from _RULES.md
    rules_path = root_path / "_RULES.md"
    rules_content = io.read_text(rules_path) or ""
    
    match = re.search(r"!STATS_INTERVAL:\s*(\d+)([hms])", rules_content)
    if not match:
        # Default: 1 hour if not configured
        interval_seconds = 3600 
    else:
        val = int(match.group(1))
        unit = match.group(2)
        if unit == 'h': interval_seconds = val * 3600
        elif unit == 'm': interval_seconds = val * 60
        else: interval_seconds = val # seconds

    # 2. Check _STATS.md mtime
    stats_path = root_path / "_STATS.md"
    if not stats_path.exists():
        return True
        
    try:
        mtime = stats_path.stat().st_mtime
        now = time.time()
        if (now - mtime) < interval_seconds:
            # print(f"⏳ Stats update skipped (Next update in {int((mtime + interval_seconds - now)/60)}m)")
            return False
    except:
        return True
        
    return True

def run(config: ProjectConfig, force: bool = False) -> bool:
    """
    执行统计 (Execute Statistics).
    Generates _STATS.md.
    """
    root_path = config.scan.root_path
    
    if not check_should_update(root_path, force):
        return True

    print(f"Calculating statistics for {config.name}...")
    
    total_files = 0
    total_lines = 0
    total_size = 0
    
    doc_files = 0
    doc_lines = 0
    
    src_files = 0
    src_lines = 0
    
    # AI Stats
    ai_doc_files = 0
    ai_doc_lines = 0
    ai_doc_size = 0
    total_dirs_scanned = 0
    dirs_with_ai = 0
    
    ignore_patterns = set(config.scan.ignore_patterns)
    include_exts = set(config.scan.extensions)
    
    # Simple walker
    for root, dirs, files in os.walk(root_path):
        # Ignore logic (simplified)
        dirs[:] = [d for d in dirs if d not in ignore_patterns and not d.startswith('.')]
        
        total_dirs_scanned += 1
        has_ai_in_this_dir = False
        
        for file in files:
            file_path = Path(root) / file
            
            # Skip ignored files
            if any(p in str(file_path) for p in ignore_patterns):
                continue
                
            total_files += 1
            try:
                size = file_path.stat().st_size
                total_size += size
                
                # Try reading lines for text files
                is_text = False
                lines_count = 0
                
                if file == '_AI.md':
                    has_ai_in_this_dir = True
                    ai_doc_files += 1
                    is_text = True
                elif file.endswith('.md'):
                    doc_files += 1
                    is_text = True
                elif file_path.suffix in include_exts:
                    src_files += 1
                    is_text = True
                
                if is_text:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines_count = sum(1 for _ in f)
                            total_lines += lines_count
                            
                            if file == '_AI.md':
                                ai_doc_lines += lines_count
                                ai_doc_size += size
                            elif file.endswith('.md'):
                                doc_lines += lines_count
                            elif file_path.suffix in include_exts:
                                src_lines += lines_count
                    except:
                        pass
                        
            except Exception as e:
                pass
        
        if has_ai_in_this_dir:
            dirs_with_ai += 1

    # Rough Token Estimation
    estimated_tokens = total_size // 4
    ai_estimated_tokens = ai_doc_size // 4
    
    # Calculate Ratio
    ratio = 0.0
    if src_lines > 0:
        ratio = ((doc_lines + ai_doc_lines) / src_lines) * 100
    
    ai_coverage = 0.0
    if total_dirs_scanned > 0:
        ai_coverage = (dirs_with_ai / total_dirs_scanned) * 100

    # Generate Markdown Content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# 项目统计报告 (Project Statistics)
> @CONTEXT: Project Metrics | @TAGS: @STATS @AUTO
> 最后更新 (Last Updated): {timestamp}

## 核心指标 (Core Metrics)

| 指标 (Metric) | 数值 (Value) | 说明 (Description) |
| :--- | :--- | :--- |
| **总文件数** | {total_files} | 包含代码和文档 |
| **总行数** | {total_lines} | 代码 + 文档总行数 |
| **项目体积** | {total_size / 1024:.2f} KB | 磁盘占用 |
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
| **文档 (Docs)** | {doc_files + ai_doc_files} | {doc_lines + ai_doc_lines} | {ratio:.1f}% (Doc/Code) |

## 健康度检查 (Health Check)

- **AI 上下文覆盖率**: {ai_coverage:.1f}%
  - {"✅ 覆盖良好 (>50%)" if ai_coverage > 50 else "⚠️ 覆盖率较低 (<50%)，建议补充 `_AI.md`"}
- **文档/代码比率**: {ratio:.1f}%
  - {"✅ 文档丰富 (>20%)" if ratio > 20 else "⚠️ 文档较少 (<20%)"}
"""
    
    # Write to _STATS.md
    stats_path = root_path / "_STATS.md"
    if io.write_text(stats_path, content):
        print(f"✅ Statistics updated: {stats_path.name}")
    
    return True
