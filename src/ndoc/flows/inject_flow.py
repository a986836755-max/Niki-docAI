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
Flow: Inject Context Header (Header Injection).
业务流：将上下文规则注入到源代码头部。
"""
import re
from pathlib import Path
from typing import List, Optional

from ..core import io, fs
from ..core.logger import logger
from ..parsing import scanner
from ..models.config import ProjectConfig

# --- Markers ---
# We use a distinct marker block for injection with explicit start/end tags
HEADER_START_TAG = "# <NIKI_AUTO_HEADER_START>\n"
HEADER_END_TAG = "# <NIKI_AUTO_HEADER_END>\n"

HEADER_START = f"{HEADER_START_TAG}# ------------------------------------------------------------------------------\n# 🧠 Niki-docAI Context (Auto-Generated)\n"
HEADER_END = f"# ------------------------------------------------------------------------------\n{HEADER_END_TAG}"

# More strict regex: Only match !RULE or !CONST blocks, stop at ANY next ## header
RULE_REGEX = re.compile(r"##\s+!(RULE|CONST)(.*?)(?=\n##|\Z)", re.DOTALL)

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
    # This is safer than regex for markdown structure
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
                    
                # Skip Dependency Links (format: * **[file.py](...)**: <AI Context> ...)
                if "<AI Context>" in line:
                    continue
                    
                # Skip Code Snippet markers if they somehow got in
                if line.startswith("```"):
                    continue

                # Clean up bold/italic slightly for readability in comments
                # (Optional, but nice)
                
                # Truncate
                if len(line) > 120:
                    line = line[:117] + "..."
                    
                rules.append(line)
                
    return rules

def generate_header(file_path: Path, config: ProjectConfig) -> str:
    """
    Generate the header content for a file.
    """
    root = config.scan.root_path
    current_dir = file_path.parent
    
    lines = [HEADER_START]
    
    # 1. Project Global Rules (from root _AI.md or _RULES.md)
    # Actually, let's just use _RULES.md for global constraints
    global_rules_path = root / "_RULES.md"
    if global_rules_path.exists():
        # We need a way to extract summary from _RULES.md too.
        # Assuming _RULES.md has similar !RULE structure or we just take the first few bullets?
        # For now, let's stick to _AI.md recursion for simplicity and specificity.
        pass

    # 2. Local Context (from current dir _AI.md)
    ai_path = current_dir / "_AI.md"
    local_rules = extract_summary_rules(ai_path)
    
    if local_rules:
        lines.append(f"#\n# [Local Rules] ({ai_path.name})\n")
        for rule in local_rules:
             lines.append(f"# {rule}\n")
    else:
        # If no local rules, maybe don't inject anything? 
        # Or inject a placeholder?
        # Let's return empty if no rules found to keep it clean.
        return ""

    lines.append(HEADER_END)
    return "".join(lines)

def inject_file(file_path: Path, config: ProjectConfig) -> bool:
    """
    Inject context header into a file.
    Aggressively cleans up ANY previous Niki-docAI context headers.
    """
    if file_path.suffix != ".py":
        return False
        
    content = io.read_text(file_path)
    if not content:
        return False
        
    lines = content.splitlines(keepends=True)
    if not lines:
        return False

    # --- AGGRESSIVE CLEANUP LOGIC ---
    # We want to remove any block of comments at the start that looks like our header.
    # Characteristics:
    # 1. Starts near top (ignoring shebang/coding decl)
    # 2. Contains "Niki-docAI Context" OR just matches our separator style
    # 3. Ends with a separator line
    
    # Identify insertion point (skip shebang/encoding)
    start_search_idx = 0
    while start_search_idx < len(lines) and (
        lines[start_search_idx].startswith("#!") or 
        "coding:" in lines[start_search_idx]
    ):
        start_search_idx += 1
        
    # --- DETECTION LOGIC (New Tags & Old Heuristics) ---
    removal_start = -1
    removal_end = -1
    
    # 1. Check for Explicit Tags (New Standard)
    tag_start = -1
    tag_end = -1
    
    for i in range(start_search_idx, min(len(lines), start_search_idx + 50)):
        if "<NIKI_AUTO_HEADER_START>" in lines[i]:
            tag_start = i
            break
            
    if tag_start != -1:
        # Look for end tag
        for j in range(tag_start + 1, min(len(lines), tag_start + 300)):
            if "<NIKI_AUTO_HEADER_END>" in lines[j]:
                tag_end = j
                break
        
        if tag_end != -1:
            removal_start = tag_start
            removal_end = tag_end

    # 2. Fallback: Old Heuristic (If no tags found)
    if removal_start == -1:
        # Heuristic: If we see a separator line early on, check if it's ours
        for i in range(start_search_idx, min(len(lines), start_search_idx + 20)): # Look ahead 20 lines max for start
            line = lines[i].strip()
            if line.startswith("# ----------------"):
                # Potential start found. Check if it's likely ours.
                # It's ours if:
                # A) The next few lines contain "Niki-docAI"
                # B) It's followed by another separator line within reasonable distance
                
                is_our_header = False
                temp_end = -1
                
                # Scan forward for end or signature
                for j in range(i + 1, min(len(lines), i + 300)): # Allow long headers (old ones were huge)
                    sub_line = lines[j].strip()
                    if "Niki-docAI" in sub_line or "[Local Rules]" in sub_line:
                        is_our_header = True
                    if sub_line.startswith("# ----------------"):
                        temp_end = j
                        # Don't break immediately, find the LAST separator if multiple? 
                        # No, usually header is bounded by two separators.
                        # But wait, old headers might have internal separators?
                        # Let's assume standard format: Start Sep ... End Sep.
                        # But to be safe, if we found "Niki-docAI" inside, the next separator is likely the end.
                        if is_our_header:
                             break
                
                # If we found an end and confirm it's ours (or just looks like a header block at top), mark for removal
                if temp_end != -1 and is_our_header:
                    removal_start = i
                    removal_end = temp_end
                    break
    
    # Execute removal if found
    if removal_start != -1 and removal_end != -1:
        del lines[removal_start : removal_end + 1]
        # Also remove any trailing newline left behind to avoid gap accumulation
        if removal_start < len(lines) and lines[removal_start].strip() == "":
             del lines[removal_start]


    # --- INJECTION LOGIC ---
    header = generate_header(file_path, config)
    if not header:
        # If no header needed (no rules), we are done (cleanup only)
        # But check if we actually changed anything
        new_content_cleanup = "".join(lines)
        if new_content_cleanup != content:
            io.write_text(file_path, new_content_cleanup)
            return True
        return False
        
    # Insert new header
    lines.insert(start_search_idx, header)
    
    new_content = "".join(lines)
    if new_content != content:
        io.write_text(file_path, new_content)
        return True
        
    return False

def run(config: ProjectConfig, target: str = None):
    """
    Execute injection flow.
    """
    root = config.scan.root_path
    
    if target:
        path = Path(target)
        if not path.is_absolute():
            path = root / path
        
        if path.is_file():
            if inject_file(path, config):
                logger.info(f"Injected: {path.relative_to(root)}")
            else:
                logger.debug(f"Skipped: {path.relative_to(root)} (No rules or not supported)")
        else:
            # Dir
             files = fs.walk_files(path, config.scan.ignore_patterns)
             for f in files:
                 if inject_file(f, config):
                     logger.info(f"Injected: {f.relative_to(root)}")
    else:
        # All
        files = fs.walk_files(root, config.scan.ignore_patterns)
        count = 0
        for f in files:
             if inject_file(f, config):
                 logger.info(f"Injected: {f.relative_to(root)}")
                 count += 1
        logger.info(f"Injection complete. Updated {count} files.")
