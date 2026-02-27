"""
View: Header Injection.
视图层：源代码头部 Context Header 渲染。
"""
from pathlib import Path
from typing import List
from ..core.templates import get_template

# --- Markers ---
HEADER_START_TAG = "# <NIKI_AUTO_HEADER_START>\n"
HEADER_END_TAG = "# <NIKI_AUTO_HEADER_END>\n"

def generate_header(file_path: Path, local_rules: List[str]) -> str:
    """
    Generate the header content for a file.
    """
    rules_content = ""
    if local_rules:
        # Assuming file_path is relative to the directory containing _AI.md
        # but simpler logic: just use the rules list.
        # We assume local_rules came from the sibling _AI.md
        ai_name = "_AI.md" 
        
        lines = []
        lines.append(f"# [Local Rules] ({ai_name})")
        for rule in local_rules:
             lines.append(f"# {rule}")
        rules_content = "\n".join(lines)
    
    template = get_template("header_injection.tpl")
    return template.format(rules_content=rules_content)
