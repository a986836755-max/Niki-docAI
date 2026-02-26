"""
Core: Project Statistics.
核心层：项目统计逻辑。
"""
import os
import time
import re
from pathlib import Path
from typing import Dict
from ..core import io
from ..models.config import ProjectConfig

def should_update_stats(root_path: Path, force: bool) -> bool:
    if force:
        return True
    
    rules_path = root_path / "_RULES.md"
    rules_content = io.read_text(rules_path) or ""
    
    match = re.search(r"!STATS_INTERVAL:\s*(\d+)([hms])", rules_content)
    if not match:
        interval_seconds = 3600 
    else:
        val = int(match.group(1))
        unit = match.group(2)
        if unit == 'h':
            interval_seconds = val * 3600
        elif unit == 'm':
            interval_seconds = val * 60
        else:
            interval_seconds = val

    stats_path = root_path / "_STATS.md"
    if not stats_path.exists():
        return True
        
    try:
        mtime = stats_path.stat().st_mtime
        now = time.time()
        if (now - mtime) < interval_seconds:
            return False
    except:
        return True
        
    return True

def collect_full_stats(config: ProjectConfig) -> Dict:
    root_path = config.scan.root_path
    total_files = 0
    total_lines = 0
    total_size = 0
    doc_files = 0
    doc_lines = 0
    src_files = 0
    src_lines = 0
    ai_doc_files = 0
    ai_doc_lines = 0
    ai_doc_size = 0
    total_dirs_scanned = 0
    dirs_with_ai = 0

    ignore_patterns = set(config.scan.ignore_patterns)
    include_exts = set(config.scan.extensions)

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ignore_patterns and not d.startswith('.')]
        
        total_dirs_scanned += 1
        has_ai_in_this_dir = False
        
        for file in files:
            file_path = Path(root) / file
            
            if any(p in str(file_path) for p in ignore_patterns):
                continue
                
            total_files += 1
            try:
                size = file_path.stat().st_size
                total_size += size
                
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

    estimated_tokens = total_size // 4
    ai_estimated_tokens = ai_doc_size // 4
    
    ratio = 0.0
    if src_lines > 0:
        ratio = ((doc_lines + ai_doc_lines) / src_lines) * 100
    
    ai_coverage = 0.0
    if total_dirs_scanned > 0:
        ai_coverage = (dirs_with_ai / total_dirs_scanned) * 100

    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "total_size": total_size,
        "estimated_tokens": estimated_tokens,
        "ai_doc_files": ai_doc_files,
        "ai_doc_lines": ai_doc_lines,
        "ai_estimated_tokens": ai_estimated_tokens,
        "ai_coverage": ai_coverage,
        "dirs_with_ai": dirs_with_ai,
        "total_dirs_scanned": total_dirs_scanned,
        "doc_files": doc_files,
        "doc_lines": doc_lines,
        "src_files": src_files,
        "src_lines": src_lines,
        "ratio": ratio
    }
