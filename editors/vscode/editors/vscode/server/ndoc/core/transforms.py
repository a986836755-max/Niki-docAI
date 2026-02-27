"""
Core: Data Transforms.
核心层：数据增强与转换逻辑。
"""
from pathlib import Path
from typing import Optional, List
from ..core import io
from ..models.context import FileContext
from ..models.config import ProjectConfig
from ..parsing.deps.test_mapper import TestUsageMapper

def inject_test_usages(f_ctx: FileContext, test_mapper: TestUsageMapper, config: ProjectConfig):
    """
    Inject test usage information into symbols.
    Modifies f_ctx in-place.
    """
    try:
        # Rel path relative to root: src/ndoc/...
        rel_path = Path(f_ctx.rel_path)
        parts = list(rel_path.parts)
        # Simple heuristic for python projects in src layout
        if parts and parts[0] == "src":
            parts = parts[1:]
        
        module_path = ".".join(parts)
        if module_path.endswith(".py"):
            module_path = module_path[:-3]
        
        module_name = module_path
        
        for sym in f_ctx.symbols:
            full_name = f"{module_name}.{sym.name}"
            usages = test_mapper.get_usages(full_name)
            if usages:
                sym.test_usages = usages
                
            # Check parent for methods (Class.method)
            if sym.parent:
                parent_full_name = f"{module_name}.{sym.parent}.{sym.name}"
                usages_p = test_mapper.get_usages(parent_full_name)
                if usages_p:
                    if sym.test_usages:
                        # Merge without duplicates
                        existing_paths = {f"{u['path']}:{u['line']}" for u in sym.test_usages}
                        for u in usages_p:
                            key = f"{u['path']}:{u['line']}"
                            if key not in existing_paths:
                                sym.test_usages.append(u)
                    else:
                        sym.test_usages = usages_p
                        
    except Exception:
        pass

def inject_header_to_file(file_path: Path, header_content: str) -> bool:
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
                is_our_header = False
                temp_end = -1
                
                # Scan forward for end or signature
                for j in range(i + 1, min(len(lines), i + 300)): # Allow long headers (old ones were huge)
                    sub_line = lines[j].strip()
                    if "Niki-docAI" in sub_line or "[Local Rules]" in sub_line:
                        is_our_header = True
                    if sub_line.startswith("# ----------------"):
                        temp_end = j
                        if is_our_header:
                             break
                
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

    if not header_content:
        # If no header needed (no rules), we are done (cleanup only)
        # But check if we actually changed anything
        new_content_cleanup = "".join(lines)
        if new_content_cleanup != content:
            io.write_text(file_path, new_content_cleanup)
            return True
        return False
        
    # Insert new header
    lines.insert(start_search_idx, header_content)
    
    new_content = "".join(lines)
    if new_content != content:
        io.write_text(file_path, new_content)
        return True
        
    return False
