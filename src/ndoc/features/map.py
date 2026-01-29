import os
import re
from pathlib import Path
from ndoc.core import console, config, utils

# -----------------------------------------------------------------------------
# Map Update Logic (formerly update_map.py)
# -----------------------------------------------------------------------------

def normalize_path(p):
    return str(p).replace('\\', '/').strip('/')

def get_ai_context(path):
    """
    Reads the 'Context' field.
    - If path is a directory, looks for _AI.md inside it.
    - If path is a file, looks inside the file itself.
    Returns None if not found.
    """
    target_file = None
    if path.is_dir():
        target_file = path / '_AI.md'
    else:
        target_file = path

    if not target_file.exists():
        return None
    
    try:
        content = target_file.read_text(encoding='utf-8')
        # Look for > **Context**: Description
        match = re.search(r'>\s*\*\*Context\*\*:\s*(.*)', content)
        if match:
            return match.group(1).strip()
    except:
        pass
    return None

def parse_map_section(lines):
    """
    Parses the MAP section lines into a dictionary of entries.
    Returns: entries { 'folder_name': { 'line': str, 'children': [str] } }
    """
    entries = {}
    current_key = None
    
    item_regex = re.compile(r'^\s{0,3}[\*\-]\s+(.*)')
    link_regex = re.compile(r'\[(.*?)\]\((.*?)\)')

    for line in lines:
        match = item_regex.match(line)
        if match:
            indent = len(line) - len(line.lstrip())
            
            if indent < 4: # Top level item
                content = match.group(1)
                link_match = link_regex.search(content)
                if link_match:
                    display_text = link_match.group(1)
                    path = link_match.group(2)
                    
                    key = None
                    if display_text.endswith('/'):
                        key = normalize_path(display_text)
                    else:
                        key = normalize_path(path)
                    
                    if not key or key == '.':
                        current_key = None
                    else:
                        current_key = key
                        entries[current_key] = {'line': line, 'children': []}
                else:
                    current_key = None
            else:
                # Child item
                if current_key:
                    entries[current_key]['children'].append(line)
        else:
            if current_key:
                entries[current_key]['children'].append(line)
            
    return entries

def scan_physical_dirs(root_path):
    """
    Scans immediate subdirectories and meta-files (_*.md) of root_path.
    Returns a dict: { 'name': 'context_description' }
    """
    results = {}
    if not root_path.exists():
        return results
        
    for item in root_path.iterdir():
        is_valid = False
        
        # 1. Directories
        if item.is_dir():
            if item.name not in config.IGNORE_DIRS and not item.name.startswith('.'):
                is_valid = True
        
        # 2. Meta-Files (starting with _)
        elif item.is_file() and item.name.startswith('_') and item.name.endswith('.md'):
            if item.name != '_MAP.md':
                is_valid = True
                
        if is_valid:
            context = get_ai_context(item)
            # Fix: If get_ai_context returns None, try to find @DOMAIN tag
            if not context and item.is_dir():
                try:
                    ai_file = item / "_AI.md"
                    if ai_file.exists():
                        content = ai_file.read_text(encoding='utf-8')
                        match = re.search(r'@DOMAIN:\s*(.*)', content)
                        if match:
                            context = match.group(1).strip()
                except: pass
                
            results[item.name] = context
            
    return results

def update_map_content(content, root_path):
    lines = content.splitlines()
    new_lines = []
    in_map = False
    map_lines = []
    
    map_start_idx = -1
    map_end_idx = -1
    
    # 1. Extract MAP section
    for i, line in enumerate(lines):
        if config.MAP_HEADER_PATTERN.match(line):
            in_map = True
            map_start_idx = i
            continue
            
        if in_map:
            if config.NEXT_HEADER_PATTERN.match(line):
                in_map = False
                map_end_idx = i
            else:
                map_lines.append(line)
        
    if map_start_idx == -1:
        # No map header found, just return content
        return content

    # If EOF reached while in_map
    if in_map and map_end_idx == -1:
        map_end_idx = len(lines)

    # 2. Parse existing entries
    existing_entries = parse_map_section(map_lines)
    
    # 3. Scan physical directories
    physical_items = scan_physical_dirs(root_path)
    
    # 4. Merge
    final_lines = []
    processed_keys = set()
    
    # 4a. Process existing keys (Updates & Deletes)
    for key, data in existing_entries.items():
        if key in physical_items:
            # Update description if available
            context = physical_items[key]
            processed_keys.add(key)
            
            line = data['line']
            children = data['children']
            
            if context:
                if ':' in line:
                    prefix = line.split(':', 1)[0]
                    new_line = f"{prefix}: {context}"
                    final_lines.append(new_line)
                else:
                    final_lines.append(f"{line}: {context}")
            else:
                final_lines.append(line)
                
            final_lines.extend(children)
        else:
            # Check if it exists as a file even if scan_physical_dirs missed it (files without _AI context?)
            # Or if it was manually added.
            # But we want to auto-remove deleted items.
            if (root_path / key).exists():
                 final_lines.append(data['line'])
                 final_lines.extend(data['children'])
            else:
                 pass

    # 4b. Add new directories
    new_keys = sorted([k for k in physical_items.keys() if k not in processed_keys])
    for key in new_keys:
        context = physical_items[key]
        desc = context if context else "(Pending Description)"
        
        is_dir = (root_path / key).is_dir()
        
        if is_dir:
            final_lines.append(f"*   **[{key}/]({key}/)**: {desc}")
        else:
            final_lines.append(f"*   **[{key}]({key})**: {desc}")
        
    # 5. Re-insert into content
    prefix_lines = lines[:map_start_idx+1]
    suffix_lines = lines[map_end_idx:]
    
    return "\n".join(prefix_lines + final_lines + suffix_lines) + "\n"

def process_file(file_path):
    if not file_path.exists():
        return
        
    console.log(f"Updating MAP in {file_path}...")
    content = file_path.read_text(encoding='utf-8')
    new_content = update_map_content(content, file_path.parent)
    
    if new_content != content:
        file_path.write_text(new_content, encoding='utf-8')
        console.detail("Status", "Updated")
    else:
        console.detail("Status", "No changes")

def update_map(root=None):
    """Updates _MAP.md and _AI.md map sections recursively."""
    if root is None:
        root = utils.get_project_root()
        
    # 1. Update root _MAP.md
    process_file(root / '_MAP.md')
    
    # 2. Update all _AI.md files
    for ai_file in root.rglob('_AI.md'):
        process_file(ai_file)
    
    console.success("Map Update Complete.")
