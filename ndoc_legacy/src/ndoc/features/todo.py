import re
import os
from pathlib import Path
from ndoc.core import console, config, utils
from ndoc.base import io, scanner

# Markers for Todo Section
TODO_START_MARKER = "<!-- NIKI_TODO_START -->"
TODO_END_MARKER = "<!-- NIKI_TODO_END -->"

# Regex for finding TODOs
# Supports: TODO: msg, FIXME: msg, TODO(user): msg
# Groups: 1=Type, 2=User(optional), 3=Message
TODO_REGEX = re.compile(r'\b(TODO|FIXME|HACK|NOTE)(\((.*?)\))?:\s*(.*)', re.IGNORECASE)

def scan_file_for_todos(file_path: Path, root: Path):
    """
    Scans a single file for TODO comments.
    Returns a list of dicts: {type, user, msg, line, file}
    """
    todos = []
    lines = io.read_lines_safe(file_path)
    for i, line in enumerate(lines):
        match = TODO_REGEX.search(line)
        if match:
            tag_type = match.group(1).upper()
            user = match.group(3) # group 2 is the outer parens
            msg = match.group(4).strip()
            
            todos.append({
                'type': tag_type,
                'user': user,
                'msg': msg,
                'line': i + 1,
                'file_path': file_path,
                'file': file_path.relative_to(root)
            })
    return todos

def scan_project_todos(root: Path):
    """
    Recursively scans the project for TODOs.
    """
    all_todos = []
    
    for file_path in scanner.walk_project_files(root):
        # Skip the _NEXT.md file itself to avoid self-reference loops!
        if file_path.name == "_NEXT.md":
            continue
            
        file_todos = scan_file_for_todos(file_path, root)
        all_todos.extend(file_todos)
            
    return all_todos

def generate_todo_md(todos, root: Path):
    """
    Generates Markdown list from todo list.
    """
    lines = []
    if not todos:
        lines.append("*   *(No TODOs found in code)*")
        return lines

    # Group by Type? Or just list them? 
    # Let's list them, maybe grouped by Type priority: FIXME > TODO > HACK > NOTE
    
    priority_order = {'FIXME': 0, 'TODO': 1, 'HACK': 2, 'NOTE': 3}
    todos.sort(key=lambda x: (priority_order.get(x['type'], 99), str(x['file']), x['line']))
    
    for item in todos:
        # Format: * **TYPE** `path/to/file:Line`: Message
        type_badge = f"**{item['type']}**"
        if item['type'] == 'FIXME':
            type_badge = f"🔴 {type_badge}"
        elif item['type'] == 'TODO':
            type_badge = f"🟡 {type_badge}"
        elif item['type'] == 'HACK':
            type_badge = f"🚧 {type_badge}"
        else:
            type_badge = f"🔵 {type_badge}"
            
        file_link = utils.make_file_link(item['file_path'], root, item['line'])
        
        user_str = f"({item['user']}) " if item['user'] else ""
        
        line = f"*   {type_badge} {user_str}`{file_link}`: {item['msg']}"
        lines.append(line)
        
    return lines

import os

def update_next_md(root: Path):
    """
    Updates _NEXT.md with scanned TODOs.
    """
    next_md_path = root / "_NEXT.md"
    if not next_md_path.exists():
        console.warning("_NEXT.md not found. Creating it...")
        next_md_path.write_text("# PROJECT ROADMAP\n\n## @TODO\n<!-- NIKI_TODO_START -->\n<!-- NIKI_TODO_END -->\n", encoding='utf-8')
        
    content = next_md_path.read_text(encoding='utf-8')
    
    # Check if markers exist
    if TODO_START_MARKER not in content:
        # Append to end if not found
        console.info("Adding TODO section to _NEXT.md")
        content += f"\n\n## @CODE_DEBT\n> Auto-generated from code comments.\n\n{TODO_START_MARKER}\n{TODO_END_MARKER}\n"
        
    todos = scan_project_todos(root)
    new_lines = generate_todo_md(todos, root)
    new_content_block = "\n".join(new_lines)
    
    # Replace content between markers
    pattern = re.compile(f"{re.escape(TODO_START_MARKER)}.*?{re.escape(TODO_END_MARKER)}", re.DOTALL)
    
    # Use a function for replacement to avoid backslash escaping issues in the content
    def repl_func(match):
        return f"{TODO_START_MARKER}\n{new_content_block}\n{TODO_END_MARKER}"
    
    new_full_content = pattern.sub(repl_func, content)
    
    next_md_path.write_text(new_full_content, encoding='utf-8')
    console.success(f"Updated _NEXT.md with {len(todos)} tasks from code.")

def cmd_todo(root: Path, action: str):
    if action == "update":
        update_next_md(root)
    else:
        console.error(f"Unknown todo action: {action}")
