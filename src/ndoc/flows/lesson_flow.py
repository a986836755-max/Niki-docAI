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
Flow: Lesson Learned (Memory Consolidation).
业务流：经验回环检查 (Pre-commit Check).
"""
from pathlib import Path
from typing import List, Dict, Any
from ..models.config import ProjectConfig
from ..parsing import scanner
from ..core import fs, io
from ..core.cli import ndoc_command

def run_check(config: ProjectConfig, target_files: List[str] = None) -> bool:
    """
    Check if changes violate any @LESSON learned in the past.
    This is a simplified check: it warns if you edit a file that has lessons.
    In future, this could use LLM to verify if the lesson is violated.
    """
    root = config.scan.root_path
    has_violations = False
    
    # If no target files provided (e.g. not running as hook), scan all?
    # Usually this runs on staged files. For now, let's just scan all files 
    # and print lessons as a "Refresher" if we were to implement a 'remind' command.
    
    # But the requirement is "Pre-commit Memory Check".
    # Assuming we get a list of changed files (simulated here)
    
    targets = []
    if target_files:
        targets = [Path(f).resolve() for f in target_files]
    else:
        # Fallback: Scan everything and just list lessons (Audit mode)
        print("ℹ️  Scanning project for Lessons Learned...")
        targets = list(fs.walk_files(root, config.scan.ignore_patterns))

    for path in targets:
        if not path.exists():
            continue
            
        result = scanner.scan_file(path, root)
        if result and result.lessons:
            print(f"🧠 Memory Recall for {path.relative_to(root)}:")
            for lesson in result.lessons:
                print(f"  ❗ LESSON: {lesson['content']}")
                # In a strict mode, we might require manual confirmation or LLM check
                # For now, we just surface it.
    
    return True

@ndoc_command(name="lesson", help="Manage Learned Lessons", group="Granular")
def run(config: ProjectConfig) -> bool:
    """
    Generate _LESSONS.md summary.
    """
    root = config.scan.root_path
    lessons = []
    
    for path in fs.walk_files(root, config.scan.ignore_patterns):
        result = scanner.scan_file(path, root)
        if result and result.lessons:
            for l in result.lessons:
                lessons.append({
                    "file": path,
                    "rel_path": str(path.relative_to(root)).replace('\\', '/'),
                    "content": l['content'],
                    "line": l['line']
                })
                
    if not lessons:
        print("ℹ️  No @LESSON tags found.")
        return True
        
    lines = []
    lines.append("# Lessons Learned (Project Memory)")
    lines.append("> @CONTEXT: Experience | @TAGS: @LESSON")
    lines.append(f"> Auto-generated from `@LESSON` tags.")
    lines.append("")
    
    for l in lessons:
        link = f"[{l['rel_path']}]({l['rel_path']}#L{l['line']})"
        lines.append(f"*   **{l['content']}**")
        lines.append(f"    *   Context: {link}")
        
    content = "\n".join(lines)
    io.write_text(root / "_LESSONS.md", content)
    print(f"✅ Generated _LESSONS.md with {len(lessons)} items.")
    return True
