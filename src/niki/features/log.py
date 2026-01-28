import datetime
import re
from pathlib import Path
from niki.core import console

def cmd_log(root, title, content, tag="Decision"):
    """
    Appends a log entry to _MEMORY.md.
    """
    memory_file = root / "_MEMORY.md"
    if not memory_file.exists():
        console.error(f"{memory_file} not found.")
        return

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # Read content
    with open(memory_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Prepare new entry
    # Ensure content ends with newline
    entry_content = content.strip()
    if entry_content:
        new_entry = f"*   **[{tag}] {title}**: {entry_content}\n"
    else:
        new_entry = f"*   **[{tag}] {title}**\n"

    # Find insertion point
    today_header = f"## {today_str}"
    
    # 1. Check if today's section exists
    header_idx = -1
    first_date_idx = -1
    
    date_pattern = re.compile(r'^## \d{4}-\d{2}-\d{2}')
    
    for i, line in enumerate(lines):
        line_strip = line.strip()
        if line_strip.startswith(today_header):
            header_idx = i
            break
        if first_date_idx == -1 and date_pattern.match(line_strip):
            first_date_idx = i
            
    if header_idx != -1:
        # Today's section exists. Append after the header.
        lines.insert(header_idx + 1, new_entry)
        
    else:
        # Today's section does not exist. Create it.
        new_section = [f"\n{today_header}\n", new_entry]
        
        if first_date_idx != -1:
            # Insert before the first existing date (maintain descending order)
            lines[first_date_idx:first_date_idx] = new_section
        else:
            # No dates found yet. Append to end.
            lines.extend(new_section)

    # Write back
    try:
        with open(memory_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
        console.success(f"Logged to _MEMORY.md: [{tag}] {title}")
    except Exception as e:
        console.error(f"Failed to write to _MEMORY.md: {e}")
