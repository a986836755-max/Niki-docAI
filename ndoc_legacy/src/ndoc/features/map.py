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

def scan_project_tree(root_path, include_files=False, max_depth=-1):
    """
    Recursively scans the project directory to build a tree structure.
    Returns a list of items.
    """
    items = []
    
    ignore_dirs = utils.get_ignore_dirs()
    
    def _scan(current_path, current_depth):
        if max_depth != -1 and current_depth >= max_depth:
            return

        # Sort: Directories first, then files. Alphabetical within groups.
        try:
            entries = sorted(list(current_path.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            return

        for entry in entries:
            # Skip ignored directories and files
            if entry.name in ignore_dirs or entry.name.startswith('.'):
                continue
                
            # Skip __pycache__ and other common noise
            if entry.name == '__pycache__' or entry.suffix == '.pyc':
                continue

            # Skip meta files (_*.md) from the tree to avoid duplication/clutter
            if entry.name.startswith('_') and entry.suffix == '.md':
                continue

            is_dir = entry.is_dir()
            
            # Filter based on include_files
            if not is_dir and not include_files:
                continue

            # Get Context
            context = None
            if is_dir:
                context = get_ai_context(entry)
                # Fallback to config patterns if no context found
                if not context:
                    # Check exact match or basename match
                    if entry.name.lower() in config.COMMON_DIR_PATTERNS:
                            context = config.COMMON_DIR_PATTERNS[entry.name.lower()]
            else:
                # For files, we usually don't have context unless we read descriptions
                # But we can try to get it if needed. 
                # For now, let's leave file context empty or maybe extract docstring?
                # Extracting docstring here might be slow.
                pass

            item = {
                'name': entry.name,
                'path': entry.relative_to(root_path),
                'type': 'dir' if is_dir else 'file',
                'depth': current_depth,
                'context': context
            }
            items.append(item)
            
            if is_dir:
                # Recurse
                _scan(entry, current_depth + 1)

    _scan(root_path, 0)
    return items

def extract_descriptions_from_lines(lines):
    """
    Extracts manual descriptions from existing map lines.
    Returns: { 'normalized_path': 'description' }
    """
    descriptions = {}
    link_regex = re.compile(r'\[(.*?)\]\((.*?)\)(.*)')
    
    for line in lines:
        match = link_regex.search(line)
        if match:
            # group(1) is display text
            path = match.group(2)
            rest = match.group(3) # usually ": Description"
            
            key = normalize_path(path)
            
            if ':' in rest:
                desc = rest.split(':', 1)[1].strip()
                if desc:
                    descriptions[key] = desc
                    
    return descriptions

def update_map_content(content, root_path, include_files=False, max_depth=-1):
    lines = content.splitlines()
    map_start_idx = -1
    map_end_idx = -1
    in_map = False
    existing_map_lines = []

    # 1. Locate MAP section start
    for i, line in enumerate(lines):
        if config.MAP_HEADER_PATTERN.match(line):
            map_start_idx = i
            break
            
    if map_start_idx == -1:
        return content # No map section found
        
    # 2. Locate the logical end of the map section (Next Section or EOF)
    # This allows us to aggressively clean up any duplicate markers or orphan content
    next_section_idx = len(lines)
    for i in range(map_start_idx + 1, len(lines)):
        # Check for any "## Header"
        if lines[i].strip().startswith("## "):
            next_section_idx = i
            break
            
    # Extract existing descriptions from the ENTIRE range to preserve manual edits
    # regardless of where they are (inside markers, between markers, etc.)
    existing_map_lines = lines[map_start_idx+1 : next_section_idx]
    existing_descriptions = extract_descriptions_from_lines(existing_map_lines)
    
    # 3. Scan project tree
    tree_items = scan_project_tree(root_path, include_files=include_files, max_depth=max_depth)
    
    # 4. Generate new lines
    new_map_lines = []
    
    # Add root items that might not be in scan (like README.md if we want it)
    # But usually README is manually added. 
    # Let's just render the scanned tree.
    
    for item in tree_items:
        indent = "  " * item['depth']
        # icon = "📂 " if item['type'] == 'dir' else "📄 "
        # User requested to remove emojis to save tokens and reduce complexity.
        
        # Determine path for link
        # Use utils.make_file_link for consistency
        abs_path = root_path / item['path']
        link_md = utils.make_file_link(abs_path, root_path, text=item['name'])

        # Determine Description
        # Priority: Manual Edit > Auto Context > Default
        # We use normalized path for lookup to match extract_descriptions logic
        path_str = normalize_path(item['path'])
        description = existing_descriptions.get(path_str)
        if not description:
            description = item['context']
        
        # Bold directories, normal files
        if item['type'] == 'dir':
             line_md = f"**{link_md}**"
        else:
             line_md = link_md

        line = f"{indent}- {line_md}"
        if description:
             line += f": {description}"
             
        new_map_lines.append(line)
        
    # 5. Reassemble content
    # Keep Start Marker -> Insert New Items -> Insert End Marker -> Keep Next Section
    final_lines = lines[:map_start_idx+1] + new_map_lines + ["<!-- NIKI_MAP_END -->"] + lines[next_section_idx:]
    return "\n".join(final_lines)

def process_file(file_path):
    if not file_path.exists():
        return
        
    console.log(f"Updating MAP in {file_path}...")
    content = file_path.read_text(encoding='utf-8')
    
    # Determine if this is Global MAP or Local AI
    is_global_map = file_path.name == "_MAP.md"
    
    if is_global_map:
        # Global Map: Dirs Only, Recursive
        new_content = update_map_content(content, file_path.parent, include_files=False, max_depth=-1)
    else:
        # Local AI: Files + Dirs, Flat (Depth 1)
        # Check for migration: If ## @MAP exists but markers don't, insert them
        if "## @MAP" in content and config.MAP_HEADER_PATTERN.search(content) is None:
             # Try to preserve existing content under @MAP until next section or EOF
             # But simply, let's just insert markers after ## @MAP
             # and wrap existing lines? Or just insert empty markers and let update fill it.
             # If we insert empty markers, the next update_map_content call will fill it.
             # But wait, update_map_content is called right here.
             # So let's modify content string BEFORE calling update_map_content.
             
             # Simple Migration:
             # Find ## @MAP
             # Replace with ## @MAP\n<!-- NIKI_MAP_START -->\n<!-- NIKI_MAP_END -->
             # This might lose existing manual entries if they aren't auto-discovered.
             # But for AI.md, usually it's just README.md or nothing.
             content = content.replace("## @MAP", f"## @MAP\n<!-- NIKI_MAP_START -->\n<!-- NIKI_MAP_END -->")
             
        # Note: root_path is file_path.parent
        new_content = update_map_content(content, file_path.parent, include_files=True, max_depth=1)
    
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
