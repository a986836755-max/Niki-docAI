import sys
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import fnmatch
from pathlib import Path
from ndoc.core import console, config, utils

# -----------------------------------------------------------------------------
# Docs Audit Logic (formerly audit_docs_sync.py)
# -----------------------------------------------------------------------------

def get_ignore_rules(ai_file):
    """
    Parses _AI.md for @CHECK_IGNORE tags.
    Returns a list of resolved Path objects or glob patterns relative to the _AI.md directory.
    """
    ignore_paths = []
    try:
        content = ai_file.read_text(encoding='utf-8')
        for line in content.splitlines():
            if line.strip().startswith(f"{config.IGNORE_TAG}:"):
                # Extract path: @CHECK_IGNORE: path/to/ignore
                path_str = line.split(':', 1)[1].strip()
                if path_str:
                    ignore_paths.append(path_str)
    except Exception as e:
        console.warning(f"Failed to parse ignore rules from {ai_file}: {e}")
    return ignore_paths

def is_ignored(file_path, ai_file):
    """
    Checks if file_path is covered by any ignore rule in ai_file.
    """
    ignore_rules = get_ignore_rules(ai_file)
    if not ignore_rules:
        return False

    rel_path = file_path.relative_to(ai_file.parent)
    str_rel_path = str(rel_path).replace(os.sep, '/')
    
    for rule in ignore_rules:
        # Normalize rule
        rule = rule.strip().replace(os.sep, '/')
        
        # 1. Directory ignore (e.g. "generated/")
        if rule.endswith('/'):
            if str_rel_path.startswith(rule):
                return True
        
        # 2. File match or glob (e.g. "foo.cpp" or "*.g.dart")
        if fnmatch.fnmatch(str_rel_path, rule):
            return True
            
        # 3. If rule is a directory but missing trailing slash, treat as directory if it matches prefix segment
        if str_rel_path.startswith(rule + '/'):
            return True

    return False

def find_nearest_ai_md(file_path, root):
    """
    Walks up the directory tree from file_path to find the nearest _AI.md.
    Returns the path to _AI.md or None.
    """
    current = file_path.parent
    
    # Stop if we go above root
    while current != root.parent:
        candidate = current / '_AI.md'
        if candidate.exists():
            return candidate

        if current == root:
            break

        current = current.parent
    return None

def strip_code_blocks(content):
    # Strip triple backtick blocks
    content = re.sub(r'```[\s\S]*?```', '', content)
    return content

def audit_hook(files, root=None):
    """
    Pre-commit hook logic.
    files: List of file paths (str) being committed.
    """
    if root is None:
        root = utils.get_project_root()

    console.log("running niki-docs-sync-audit hook...")
    changed_files = [Path(f).resolve() for f in files]

    # Filter for code files
    code_files = [f for f in changed_files if f.suffix in config.CODE_EXTENSIONS]

    # Set of changed _AI.md files
    changed_ai_mds = {f for f in changed_files if f.name == '_AI.md'}

    errors = []

    for code_file in code_files:
        # Ignore deleted files
        if not code_file.exists():
            continue

        ai_file = find_nearest_ai_md(code_file, root)

        if ai_file:
            # Check if this file is explicitly ignored by the governing _AI.md
            if is_ignored(code_file, ai_file):
                continue

            # strict rule: if code changes, the controlling _AI.md MUST change.
            if ai_file not in changed_ai_mds:
                rel_code = code_file.relative_to(root)
                rel_ai = ai_file.relative_to(root)
                errors.append(f"[Blocking] Code modified: {rel_code}, but relevant doc unchanged: {rel_ai}")
        else:
            # No _AI.md found in ancestry.
            try:
                rel_code = code_file.relative_to(root)
            except ValueError:
                rel_code = code_file # Fallback if not relative to root
            errors.append(f"[Blocking] Code modified: {rel_code}, but NO _AI.md found in any parent directory.")

    if errors:
        console.error("!!! NIKI DOCS SYNC AUDIT FAILED !!!")
        for e in errors:
            console.error(e)
        console.info("Rule: Any code change must be accompanied by an update to its controlling _AI.md.")
        return False

    console.success("Docs Sync Audit Passed.")
    return True

def audit_scan(root=None):
    """
    CI/Gatekeeper scan logic.
    Validates syntax of all _AI.md files.
    """
    if root is None:
        root = utils.get_project_root()
        
    console.log("running niki-docs-sync-scan...")
    ai_files = list(root.rglob('_AI.md'))

    errors = []

    for ai_file in ai_files:
        try:
            content = ai_file.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(f"Failed to read {ai_file}: {e}")
            continue

        # Check 1: Required Tags
        missing_tags = [tag for tag in config.REQUIRED_TAGS if tag not in content]
        if missing_tags:
            errors.append(f"{ai_file.relative_to(root)} missing tags: {missing_tags}")

        # Check 2: MAP Links (Basic Regex)
        clean_content = strip_code_blocks(content)
        
        # Pattern: [Link Text](path/to/file)
        links = re.findall(r'\[.*?\]\((.*?)\)', clean_content)
        for link in links:
            # Ignore external links
            if link.startswith('http') or link.startswith('#') or link.startswith('mailto'):
                continue

            # Handle anchor links (file.md#section)
            link_path = link.split('#')[0]
            if not link_path:
                continue

            # Resolve relative to the _AI.md file
            target = (ai_file.parent / link_path).resolve()

            if not target.exists():
                errors.append(f"{ai_file.relative_to(root)} has broken link: {link} (Resolved: {target})")

    if errors:
        console.error("!!! NIKI DOCS SYNC SCAN FAILED !!!")
        for e in errors:
            console.error(e)
        return False

    console.success("Docs Syntax Scan Passed.")
    return True

# -----------------------------------------------------------------------------
# Docs Update Logic (formerly update_docs.py)
# -----------------------------------------------------------------------------

def find_doxygen_executable(root_path):
    # 1. Check PATH
    if shutil.which("doxygen"):
        return "doxygen"
    
    # 2. Check local tools/ directory (Project-local fallback)
    local_doxygen = root_path / "tools" / "doxygen.exe"
    if local_doxygen.exists():
        return str(local_doxygen)
        
    return None

def run_doxygen(root_path):
    doxyfile_path = root_path / config.DOXYFILE_PATH
    if not doxyfile_path.exists():
        console.error(f"{doxyfile_path} not found.")
        return False
    
    doxygen_exe = find_doxygen_executable(root_path)
    if not doxygen_exe:
        console.error("'doxygen' executable not found.")
        console.info("  1. Install it and add to PATH, OR")
        console.info(f"  2. Download doxygen.exe and place it in {root_path / 'tools'}")
        return False

    console.log(f"Running Doxygen ({doxygen_exe})...")
    # Ensure build dir exists
    (root_path / "build" / "docs").mkdir(parents=True, exist_ok=True)
    
    try:
        # Run Doxygen and capture output for colorization
        process = subprocess.Popen(
            [doxygen_exe, str(doxyfile_path)],
            cwd=root_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                line = line.rstrip()
                # Regex for standard gcc-style errors/warnings
                match = re.match(r'^(.+?):(\d+):\s+(warning|error):\s+(.*)$', line)
                if match:
                    file_path = match.group(1)
                    line_num = match.group(2)
                    msg_type = match.group(3)
                    message = match.group(4)
                    
                    path_str = f"{console.CYAN}{file_path}:{line_num}{console.RESET}"
                    
                    if msg_type == 'warning':
                        type_str = f"{console.YELLOW}{console.BOLD}warning:{console.RESET}"
                    else: # error
                        type_str = f"{console.RED}{console.BOLD}error:{console.RESET}"
                        
                    print(f"{path_str}: {type_str} {message}")
                else:
                    if "warning:" in line:
                         print(f"{console.YELLOW}{line}{console.RESET}")
                    elif "error:" in line:
                         print(f"{console.RED}{line}{console.RESET}")
                    else:
                         console.log(line)

        if process.returncode != 0:
            console.error(f"Doxygen failed with exit code {process.returncode}")
            return False
            
        return True

    except Exception as e:
        console.error(f"Doxygen execution error: {e}")
        return False

def get_text_from_element(element):
    """Recursively extract text from an XML element."""
    if element is None:
        return ""
    text = element.text or ""
    for child in element:
        text += get_text_from_element(child)
        if child.tail:
            text += child.tail
    return text.strip()

def parse_xml_docs(root_path):
    xml_root = root_path / config.XML_OUTPUT_DIR
    index_file = xml_root / "index.xml"
    
    if not index_file.exists():
        console.error(f"{index_file} not found.")
        return {}

    tree = ET.parse(index_file)
    root = tree.getroot()
    
    # Map: ai_md_path -> list of markdown lines
    docs_map = {}
    
    # Iterate over compounds (classes, structs)
    for compound in root.findall("compound"):
        kind = compound.get("kind")
        if kind not in ["class", "struct"]:
            continue
            
        refid = compound.get("refid")
        name = compound.find("name").text
        
        # Parse detailed file
        detail_file = xml_root / f"{refid}.xml"
        if not detail_file.exists():
            continue
            
        detail_tree = ET.parse(detail_file)
        detail_root = detail_tree.getroot()
        compound_def = detail_root.find("compounddef")
        
        # Get Location
        location = compound_def.find("location")
        if location is None:
            continue
            
        file_path_str = location.get("file")
        if not file_path_str:
            continue
            
        full_file_path = root_path / file_path_str
        
        # Find closest _AI.md
        target_ai_md = find_nearest_ai_md(full_file_path, root_path)
        if not target_ai_md:
            continue
            
        # Extract Brief
        brief = get_text_from_element(compound_def.find("briefdescription"))
        
        # Prepare Markdown
        entry_lines = []
        entry_lines.append(f"*   **{kind.capitalize()} {name}**")
        if brief:
            entry_lines.append(f"    *   _Description_: {brief}")
            
        # Extract Public Functions
        for section in compound_def.findall("sectiondef"):
            if section.get("kind") == "public-func":
                for member in section.findall("memberdef"):
                    func_name = member.find("name").text
                    
                    # Skip standard lifecycle methods if no brief
                    if func_name in [name, f"~{name}"]:
                        continue
                        
                    func_brief = get_text_from_element(member.find("briefdescription"))
                    
                    args = member.find("argsstring").text or "()"
                    
                    if func_brief:
                        entry_lines.append(f"    *   `{func_name}{args}`: {func_brief}")
        
        if target_ai_md not in docs_map:
            docs_map[target_ai_md] = []
        docs_map[target_ai_md].extend(entry_lines)

    return docs_map

def update_ai_md_files(docs_map):
    for md_path, lines in docs_map.items():
        if not lines:
            continue
            
        console.log(f"Updating docs in {md_path}...")
        try:
            content = md_path.read_text(encoding='utf-8')
        except Exception as e:
            console.error(f"Failed to read {md_path}: {e}")
            continue
            
        # Check markers
        pattern = re.compile(f"{re.escape(config.MARKER_START)}.*?{re.escape(config.MARKER_END)}", re.DOTALL)
        
        new_section = f"{config.MARKER_START}\n## API Summary (Auto-generated)\n" + "\n".join(lines) + f"\n{config.MARKER_END}"
        
        if pattern.search(content):
            new_content = pattern.sub(new_section, content)
        else:
            # Append if not found
            new_content = content + "\n\n" + new_section
            
        if new_content != content:
            md_path.write_text(new_content, encoding='utf-8')
            console.detail("Status", "Updated")
        else:
            console.detail("Status", "No changes")

def update(root=None):
    """Main entry point for updating docs via Doxygen."""
    if root is None:
        root = utils.get_project_root()
        
    if not run_doxygen(root):
        return False
        
    console.log("Parsing XML and Updating _AI.md...")
    docs_map = parse_xml_docs(root)
    update_ai_md_files(docs_map)
    console.success("Doc Sync Complete.")
    return True
