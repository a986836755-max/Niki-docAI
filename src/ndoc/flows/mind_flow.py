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
Flow: Mental Map (Intent Index).
业务流：生成意图索引 (_MIND.md)。
"""
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict
from ..models.config import ProjectConfig
from ..parsing import scanner
from ..core import fs, io
from ..core.cli import ndoc_command

@ndoc_command(name="mind", help="Manage Mind Maps", group="Granular")
def run(config: ProjectConfig) -> bool:
    """
    Scan project for @INTENT tags and generate _MIND.md.
    """
    root = config.scan.root_path
    intents = defaultdict(list)
    
    # 1. Scan all files
    for path in fs.walk_files(root, config.scan.ignore_patterns):
        result = scanner.scan_file(path, root)
        if result and result.intents:
            for intent in result.intents:
                # Normalize intent (lowercase, strip)
                key = intent.lower().strip()
                intents[key].append(str(path.relative_to(root)).replace('\\', '/'))
                
    if not intents:
        print("ℹ️  No @INTENT tags found.")
        return True
        
    # 2. Generate Markdown
    lines = []
    lines.append("# Mental Map (Intent Index)")
    lines.append("> @CONTEXT: Mental Map | @TAGS: @MIND")
    lines.append(f"> Auto-generated from `@INTENT` tags. Maps logic intent to physical files.")
    lines.append("")
    
    # Sort by intent name
    for intent in sorted(intents.keys()):
        # Title case for display
        display_title = intent.title()
        lines.append(f"## {display_title}")
        for rel_path in sorted(set(intents[intent])):
            lines.append(f"*   [{rel_path}]({rel_path})")
        lines.append("")
        
    content = "\n".join(lines)
    
    # 3. Write to _MIND.md in root
    mind_file = root / "_MIND.md"
    io.write_text(mind_file, content)
    print(f"✅ Generated {mind_file} with {len(intents)} intent categories.")
    
    return True
