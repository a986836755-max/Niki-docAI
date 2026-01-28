import os
import re
from pathlib import Path
from niki.core import console
from niki.core import config
from . import link

def fix_formatting(file_path):
    """
    Applies standard formatting to a markdown file:
    1. Trims trailing whitespace from lines.
    2. Ensures exactly one newline at the end of the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        console.warning(f"Skipping binary or non-utf8 file: {file_path}")
        return False

    new_lines = []
    changed = False

    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            if line != "\n":
                new_lines.append("\n")
                changed = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(stripped + "\n")
            if (stripped + "\n") != line:
                changed = True

    content = "".join(new_lines)
    content = content.rstrip()
    if content:
        content += "\n"
        
    if content != "".join(lines):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    
    return False

def cmd_fix(root):
    """
    Main entry point for 'niki fix'.
    """
    console.step("Running Auto-Fixer on Documentation...")
    
    # 1. Format Fixes
    console.log("Applying formatting rules (trailing whitespace, EOF newline)...")
    
    # Helper to check ignore
    def is_ignored(path):
        for part in path.parts:
            if part in config.IGNORE_DIRS:
                return True
        return False

    md_files = []
    for path in root.rglob("*.md"):
        if is_ignored(path.relative_to(root)):
            continue
        md_files.append(path)
        
    fixed_count = 0
    for md_file in md_files:
        if fix_formatting(md_file):
            console.log(f"  Fixed formatting: {md_file.relative_to(root)}")
            fixed_count += 1
            
    if fixed_count > 0:
        console.success(f"Formatted {fixed_count} files.")
    else:
        console.info("No formatting issues found.")

    # 2. Run Linker
    console.step("Running Glossary Linker...")
    link.cmd_link(root)
    
    console.success("Auto-Fix Complete.")
