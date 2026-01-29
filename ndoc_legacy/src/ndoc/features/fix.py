import os
import re
from pathlib import Path
from ndoc.core import console
from ndoc.core import config
from ndoc.base import io, scanner
from . import link, syntax

def fix_formatting(file_path):
    """
    Applies standard formatting to a markdown file:
    1. Trims trailing whitespace from lines.
    2. Ensures exactly one newline at the end of the file.
    """
    lines = io.read_lines_safe(file_path)
    if not lines and not os.path.getsize(file_path) == 0:
        # If read failed but file is not empty, assume binary or error
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
        return io.write_text_safe(file_path, content)
    
    return False

def cmd_fix(root):
    """
    Main entry point for 'niki fix'.
    """
    console.step("Running Auto-Fixer on Documentation...")
    
    # 1. Format Fixes
    console.log("Applying formatting rules (trailing whitespace, EOF newline)...")
    
    # Use scanner to find all markdown files respecting ignores
    md_files = scanner.walk_project_files(root, extensions=['.md'])
        
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

    # 3. Syntax Auto-Discovery
    console.step("Registering New Tags...")
    syntax.cmd_audit_tags(root, auto_fix=True)
    
    console.success("Auto-Fix Complete.")
