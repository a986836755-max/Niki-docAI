import re
from pathlib import Path
from ndoc.core import console, config
from ndoc.base import io, scanner

TAG_REGEX = re.compile(r'@TAGS:\s*(.*)')

def scan_tags_in_file(file_path: Path):
    """
    Scans a file for @TAGS: tag1 @tag2 ...
    """
    found_tags = set()
    lines = io.read_lines_safe(file_path, limit=50)
    
    for line in lines:
        match = TAG_REGEX.search(line)
        if match:
            # Extract tags: "@foo @bar" -> ["@foo", "@bar"]
            raw_tags = match.group(1).split('|') # Support "Tag | Tag" or space
            if len(raw_tags) == 1:
                raw_tags = match.group(1).split()
                
            for t in raw_tags:
                t = t.strip()
                if t.startswith('@'):
                    found_tags.add(t)
                else:
                    # Handle "Tag" without @?
                    found_tags.add(f"@{t}")
    return found_tags

def scan_project_tags(root: Path):
    """
    Scans all _AI.md and source files for custom tags.
    """
    all_tags = set()
    
    # Extensions to scan: .md + code extensions
    # config.CODE_EXTENSIONS is likely a list/set of strings like ['.py', '.cpp']
    extensions = ['.md'] + list(config.CODE_EXTENSIONS)
    
    for file_path in scanner.walk_project_files(root, extensions=extensions):
        tags = scan_tags_in_file(file_path)
        all_tags.update(tags)
                
    return all_tags

def update_syntax_md(root: Path):
    """
    Updates _SYNTAX.md with discovered tags.
    """
    syntax_file = root / "_SYNTAX.md"
    if not syntax_file.exists():
        console.warning("_SYNTAX.md not found. Skipping tag registry update.")
        return

    discovered = scan_project_tags(root)
    
    # Read existing syntax file to see what's already defined
    content = io.read_text_safe(syntax_file)
    if not content:
        # Should we proceed if empty? Maybe.
        pass
    
    # Simple check: is the tag mentioned in the file?
    # This is a bit naive but works for now.
    
    new_tags = []
    for tag in sorted(discovered):
        if tag not in content:
            new_tags.append(tag)
            
    if not new_tags:
        console.info("No new tags discovered.")
        return
        
    console.info(f"Discovered {len(new_tags)} new tags: {', '.join(new_tags)}")
    
    # Append to @DISCOVERED section
    if "## @DISCOVERED" not in content:
        content += "\n\n## @DISCOVERED\n> Auto-detected tags not yet formally defined.\n"
        
    # Append lines
    for tag in new_tags:
        content += f"\n- `{tag}`: (Auto-discovered)"
        
    io.write_text_safe(syntax_file, content)
    console.success(f"Updated _SYNTAX.md with new tags.")

def cmd_syntax(root: Path, action: str):
    if action == "update":
        update_syntax_md(root)
    else:
        console.error(f"Unknown syntax action: {action}")
