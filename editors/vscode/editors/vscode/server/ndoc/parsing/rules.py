"""
Parsing: Rule Extraction.
感知层：规则提取与解析。
"""
import re
from pathlib import Path
from typing import List

from ..core import io

def extract_summary_rules(ai_path: Path) -> List[str]:
    """
    Extract concise rules from _AI.md.
    Strictly filters out API definitions and code signatures.
    """
    if not ai_path.exists():
        return []
        
    content = io.read_text(ai_path) or ""
    rules = []
    
    # 1. First, split by ## headers to process blocks safely
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Check if this is a RULE or CONST section
        if section.startswith("!RULE") or section.startswith("!CONST"):
            # Remove the header line
            lines = section.splitlines()
            if not lines:
                continue
            
            # Process body lines
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                # Only take list items
                if not line.startswith(("-", "*")):
                    continue
                    
                # --- FILTERING LOGIC ---
                # Skip API signatures
                if any(x in line for x in ["PUB:", "PRV:", "VAL->", "GET->", "`@API`"]):
                    continue
                    
                # Skip Dependency Links
                if "<AI Context>" in line:
                    continue
                    
                # Skip Code Snippet markers
                if line.startswith("```"):
                    continue

                # Truncate
                if len(line) > 120:
                    line = line[:117] + "..."
                    
                rules.append(line)
                
    return rules

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
            if line.startswith("- `") or line.startswith("* `"):
                # Regex to extract tag and meaning
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

def extract_domain_context(target_path: Path, root: Path) -> str:
    """
    Extract domain context from nearest _AI.md.
    """
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
                
        return "\n".join(filtered_lines)
    return ""
