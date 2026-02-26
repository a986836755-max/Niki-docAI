# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: New flows (like `capability_flow.py`) must be registered in `entry.py` to ensure ...
# *   **Auto-Provisioning**: `capability_flow` acts as the project's "immune system", proactively detecting and install...
# *   **Doctor Integration**: `doctor_flow` should reuse the `CapabilityManager` logic to verify system health, rather ...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Prompt Generation (AI Thinking Context).
业务流：为 AI 生成思考所需的上下文 Prompt。
"""
import re
from pathlib import Path
from typing import List, Optional

from ..core import io
from ..core.logger import logger
from ..parsing import scanner
from ..brain import index
from ..parsing.ast import skeleton
# from ..brain.vectordb import VectorDB # Runtime import
from ..models.config import ProjectConfig

RULE_MARKER = "## !RULE"
CTX_START = "<!-- NIKI_CTX_START -->"

# --- Condensation Logic ---

def extract_syntax_summary(root: Path) -> str:
    """
    Extract condensed syntax definition from _SYNTAX.md.
    Only retains @TAGS and their short descriptions.
    """
    syntax_path = root / "_SYNTAX.md"
    if not syntax_path.exists():
        return ""
        
    content = io.read_text(syntax_path)
    lines = content.splitlines()
    summary = []
    
    in_tags_section = False
    for line in lines:
        line = line.strip()
        if line.startswith("## @TAGS") or line.startswith("### @TAGS"):
            in_tags_section = True
            summary.append("## 3. Syntax Reference (Condensed)")
            continue
            
        if in_tags_section:
            if line.startswith("## ") and not line.startswith("## @"): # New major section
                break
                
            # Extract list items: - `@TAG`: **Meaning**. Description
            # We want: @TAG: Meaning
            if line.startswith("- `") or line.startswith("* `"):
                # Regex to extract tag and meaning
                # - `@API`: **Public**. ...
                match = re.match(r"[-*]\s+`(@[A-Z_]+)`:\s*\*\*([^*]+)\*\*", line)
                if match:
                    tag, meaning = match.groups()
                    summary.append(f"- {tag}: {meaning}")
                    
    return "\n".join(summary)

def extract_global_rules(root: Path) -> str:
    """
    Extract critical global rules from _RULES.md.
    Only retains !RULE, !CONST, !LIMIT lines.
    """
    rules_path = root / "_RULES.md"
    if not rules_path.exists():
        return ""
        
    content = io.read_text(rules_path)
    lines = content.splitlines()
    summary = []
    summary.append("## 1. Critical Constraints (Global)")
    
    for line in lines:
        line = line.strip()
        # Filter for strict rules
        if line.startswith("- `!RULE`") or line.startswith("- `!CONST`") or line.startswith("- `!LIMIT`"):
            summary.append(line)
        # Also support plain text format if used: - !RULE: ...
        elif line.startswith("- !RULE") or line.startswith("- !CONST"):
            summary.append(line)
            
    if len(summary) == 1: # Only header
        return ""
        
    return "\n".join(summary)

def get_context_prompt(file_path: str, config: ProjectConfig, focus: bool = False, use_skeleton: bool = False) -> str:
    """
    生成针对特定文件的上下文 Prompt。
    支持 Focus Mode: 只返回最相关的 5% 上下文。
    """
    root = config.scan.root_path
    target = root / file_path
    
    if not target.exists():
        return f"Error: File not found: {file_path}"

    target_path = target.resolve()
    
    # 1. Target Code (Skeleton or Full)
    target_section = ""
    if target_path.exists():
        raw_content = io.read_text(target_path)
        if raw_content:
            if use_skeleton:
                skel = skeleton.generate_skeleton(raw_content, str(target_path))
                target_section = f"## 4. Target Code (Skeleton)\nFile: {target_path.relative_to(root)}\n```python\n{skel}\n```"
            else:
                # Limit size if too large?
                target_section = f"## 4. Target Code\nFile: {target_path.relative_to(root)}\n```\n{raw_content}\n```"
    else:
        target_section = f"## 4. Target Code\n(File not found: {target_path.name})"

    # 2. Global Rules (Condensed)
    global_rules = extract_global_rules(root)
    
    # 3. Syntax (Condensed)
    syntax_summary = extract_syntax_summary(root)
    
    # 4. Domain Context (Nearest _AI.md)
    domain_context = ""
    current = target_path.parent if target_path.is_file() else target_path
    
    # Find nearest _AI.md
    ai_path = None
    while current != root.parent:
        candidate = current / "_AI.md"
        if candidate.exists():
            ai_path = candidate
            break
        current = current.parent
        
    if ai_path:
        # Extract !RULE and @DOMAIN from local context
        ai_content = io.read_text(ai_path)
        lines = ai_content.splitlines()
        filtered_lines = []
        filtered_lines.append(f"## 2. Domain Context ({ai_path.relative_to(root)})")
        
        # Extract local rules and domain definition
        for line in lines:
            line = line.strip()
            if "!RULE" in line or "!CONST" in line:
                filtered_lines.append(line)
            elif "@DOMAIN" in line or "@OVERVIEW" in line:
                filtered_lines.append(line)
            # Also include memory/auto-detected rules
            elif "**RULE**:" in line: # Auto-detected rules format
                filtered_lines.append(line)
                
        domain_context = "\n".join(filtered_lines)

    # 5. Related APIs (Imports) - Placeholder for now
    # Ideally we scan target_path imports, find their _AI.md, and extract @API signatures.
    # This requires running scanner on target_path first.
    related_apis = ""
    # TODO: Implement dependency API extraction
    
    # Assemble
    parts = [
        f"# Context for {target_path.name}",
        global_rules,
        domain_context,
        syntax_summary,
        related_apis,
        target_section
    ]
    
    if focus:
        # Use Vector DB to find relevant snippets
        from ..brain.vectordb import VectorDB
        db = VectorDB(root)
        
        related_snippets = []
        if db.collection:
            # Query using file content or name
            query = target_path.name
            if target_path.exists() and io.read_text(target_path):
                query = io.read_text(target_path)[:500] # Use first 500 chars
                
            results = db.search(query, n_results=5)
            if results:
                related_snippets.append("## 5. Related Context (Semantic Search)")
                for res in results:
                    path = res.get('id', 'unknown')
                    content = res.get('document', '')
                    # Truncate content
                    preview = content[:300] + "..." if len(content) > 300 else content
                    related_snippets.append(f"### {path}\n```\n{preview}\n```")
        
        parts.insert(4, "\n".join(related_snippets))

    return "\n\n".join([p for p in parts if p])

def _get_full_context(file_path: Path, root: Path) -> str:
    """
    Legacy full context generation.
    """
    current_dir = file_path.parent if file_path.is_file() else file_path
    
    rules = []
    
    # 1. Global Rules (_RULES.md)
    global_rules_path = root / "_RULES.md"
    if global_rules_path.exists():
        rules.append(f"### Global Rules ({global_rules_path.name})\n{io.read_text(global_rules_path)}")
        
    # 2. _SYNTAX.md
    syntax_path = root / "_SYNTAX.md"
    if syntax_path.exists():
        rules.append(f"### Syntax\n{io.read_text(syntax_path)}")

    # 3. Inherited Rules
    try:
        if file_path.is_absolute() and str(file_path).startswith(str(root)):
            rel_path = file_path.relative_to(root)
            parts = rel_path.parts[:-1] if file_path.is_file() else rel_path.parts
            
            path_cursor = root
            # Root _AI.md
            ai_file = path_cursor / "_AI.md"
            if ai_file.exists():
                 rules.append(f"### Project Context ({path_cursor.name})\n{io.read_text(ai_file)}")
                 
            for part in parts:
                path_cursor = path_cursor / part
                ai_file = path_cursor / "_AI.md"
                if ai_file.exists():
                    rules.append(f"### Module Context ({part})\n{io.read_text(ai_file)}")
    except ValueError:
        pass

    return "\n\n".join(rules)

def run(file_path: str, config: ProjectConfig, focus: bool = False) -> bool:
    """
    打印 Prompt Context 到标准输出。
    """
    path = Path(file_path)
    prompt = get_context_prompt(path, config, focus)
    
    print("-" * 20 + " AI CONTEXT START " + "-" * 20)
    print(prompt)
    print("-" * 20 + " AI CONTEXT END " + "-" * 20)
    return True
