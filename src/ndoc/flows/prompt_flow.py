"""
Flow: Prompt Generation (AI Thinking Context).
业务流：为 AI 生成思考所需的上下文 Prompt。
"""
import re
from pathlib import Path
from typing import List, Optional

from ..atoms import io, scanner
from ..models.config import ProjectConfig

# --- Markers ---
RULE_MARKER = "## !RULE"
CTX_START = "<!-- NIKI_CTX_START -->"

def extract_rules_from_ai(ai_path: Path) -> str:
    """
    从 _AI.md 中提取 !RULE 和 记忆部分。
    """
    if not ai_path.exists():
        return ""
        
    content = io.read_text(ai_path) or ""
    
    # 提取 ## !RULE 之后的内容，直到下一个 ## 或文件结束
    match = re.search(r"## !RULE(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def get_context_prompt(file_path: Path, config: ProjectConfig) -> str:
    """
    生成针对特定文件的上下文 Prompt。
    包含：
    1. 当前目录的 _AI.md 中的规则 (Local Rules)
    2. 父级目录的 _AI.md 中的规则 (Inherited Rules - recursively)
    3. 项目根目录的 _RULES.md (Global Rules)
    """
    root = config.scan.root_path
    
    # Ensure file_path is absolute
    if not file_path.is_absolute():
        file_path = (root / file_path).resolve()
        
    current_dir = file_path.parent if file_path.is_file() else file_path
    
    rules = []
    
    # 1. Global Rules (_RULES.md)
    global_rules_path = root / "_RULES.md"
    if global_rules_path.exists():
        rules.append(f"### Global Rules ({global_rules_path.name})\n{io.read_text(global_rules_path)}")

    # 2. Inherited Rules (Leaf -> Root, but usually we want Root -> Leaf for context)
    # Let's collect path from root to current_dir
    try:
        rel_path = current_dir.relative_to(root)
        parts = rel_path.parts
        
        # Traverse from root down to current_dir
        path_cursor = root
        # Check root _AI.md first (if any)
        ai_file = path_cursor / "_AI.md"
        content = extract_rules_from_ai(ai_file)
        if content:
             rules.append(f"### Project Context ({path_cursor.name})\n{content}")
             
        for part in parts:
            path_cursor = path_cursor / part
            ai_file = path_cursor / "_AI.md"
            content = extract_rules_from_ai(ai_file)
            if content:
                rules.append(f"### Module Context ({part})\n{content}")
                
    except ValueError:
        # file_path is not in root, just check current dir
        ai_file = current_dir / "_AI.md"
        content = extract_rules_from_ai(ai_file)
        if content:
            rules.append(f"### Local Context ({current_dir.name})\n{content}")

    return "\n\n".join(rules)

def run(file_path: str, config: ProjectConfig) -> bool:
    """
    打印 Prompt Context 到标准输出。
    """
    path = Path(file_path)
    prompt = get_context_prompt(path, config)
    
    print("-" * 20 + " AI CONTEXT START " + "-" * 20)
    print(prompt)
    print("-" * 20 + " AI CONTEXT END " + "-" * 20)
    return True
