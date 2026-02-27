# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **RULE**: @LAYER(core) CANNOT_IMPORT @LAYER(ui) --> [context_flow.py:198](context_flow.py#L198)
# *   **RULE**: @FORBID(hardcoded_paths) --> [context_flow.py:199](context_flow.py#L199)
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Decision Snapshot (ADR).
业务流：生成架构决策记录 (_ADR.md)。
"""
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict
from ..models.config import ProjectConfig
from ..parsing import scanner
from ..core import fs, io
from ..core.cli import ndoc_command

@ndoc_command(name="adr", help="Manage Architecture Decision Records (ADR)", group="Granular")
def run(config: ProjectConfig) -> bool:
    """
    Scan project for @DECISION tags and generate _ADR.md.
    """
    root = config.scan.root_path
    decisions = []
    
    # 1. Scan all files
    for path in fs.walk_files(root, config.scan.ignore_patterns):
        # We can use scanner.scan_file to leverage cache
        result = scanner.scan_file(path, root)
        if result and result.decisions:
            for d in result.decisions:
                decisions.append({
                    "file": path,
                    "rel_path": str(path.relative_to(root)).replace('\\', '/'),
                    "content": d['content'],
                    "line": d['line']
                })
                
    if not decisions:
        print("ℹ️  No @DECISION tags found.")
        return True
        
    # 2. Group by directory/module for better readability
    grouped = defaultdict(list)
    for d in decisions:
        # Group by top-level folder or 'Root'
        parts = Path(d['rel_path']).parts
        group = parts[0] if len(parts) > 1 else "Root"
        grouped[group].append(d)
        
    # 3. Generate Markdown
    lines = []
    lines.append("# Architecture Decision Records (ADR)")
    lines.append("> @CONTEXT: Architecture | @TAGS: @ADR")
    lines.append(f"> Auto-generated from `@DECISION` tags in source code.")
    lines.append("")
    
    for group in sorted(grouped.keys()):
        lines.append(f"## {group}")
        for d in grouped[group]:
            link = f"[{d['rel_path']}]({d['rel_path']}#L{d['line']})"
            lines.append(f"*   **{d['content']}**")
            lines.append(f"    *   Source: {link}")
        lines.append("")
        
    content = "\n".join(lines)
    
    # 4. Write to _ADR.md in root
    adr_file = root / "_ADR.md"
    io.write_text(adr_file, content)
    print(f"✅ Generated {adr_file} with {len(decisions)} decisions.")
    
    return True
