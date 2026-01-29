import sys
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import fnmatch
import ast
from pathlib import Path
from ndoc.core import console, config, utils
from ndoc.base.parser import extract_docstring
from ndoc.features import syntax

def init_ai_md(path_str, verbose=True, reset=False):
    """
    Creates an _AI.md file in the specified directory.
    """
    root = utils.get_project_root()
    # Handle path_str being a Path object or string
    if isinstance(path_str, Path):
        target_path = path_str
        if target_path.is_absolute():
            pass # Keep as is
        else:
            target_path = (root / target_path).resolve()
    else:
        target_path = (root / path_str).resolve()
        
    # If input is a file (ends with .md or exists as file), use its parent
    if target_path.name.lower() == '_ai.md' or (target_path.exists() and target_path.is_file()):
        target_dir = target_path.parent
    else:
        target_dir = target_path
    
    if not target_dir.exists():
        console.error(f"Directory not found: {target_dir}")
        console.info(f"Creating directory: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)
        
    ai_file = target_dir / "_AI.md"
    
    if ai_file.exists() and not reset:
        if verbose:
            console.warning(f"{ai_file} already exists.")
        return False
        
    module_name = target_dir.name
    domain_tag = f"domain.{module_name.lower()}"
    
    # Smart Description Inference
    desc_override = None
    if module_name.lower() in config.COMMON_DIR_PATTERNS:
        desc_override = config.COMMON_DIR_PATTERNS[module_name.lower()]
    
    content = config.AI_TEMPLATE.format(
        module_name=module_name,
        domain_tag=domain_tag,
        version=config.TOOLCHAIN_VERSION
    )
    
    # Apply override if found
    if desc_override:
        content = content.replace(
            "(Describe the core responsibility of this module. Why does it exist?)",
            desc_override
        )
    
    try:
        ai_file.write_text(content, encoding='utf-8')
        if reset and ai_file.exists():
             console.success(f"Reset {ai_file}")
        else:
             console.success(f"Created {ai_file}")
        return True
    except Exception as e:
        console.error(f"Failed to create {ai_file}: {e}")
        return False

def init_all_recursive(start_path=".", reset=False):
    """
    Recursively creates _AI.md in all subdirectories of start_path,
    skipping ignored directories.
    """
    root = utils.get_project_root()
    start_dir = (root / start_path).resolve()
    
    if not start_dir.exists():
        console.error(f"Directory not found: {start_dir}")
        return

    console.log(f"Scanning for directories in {start_dir}...")
    created_count = 0
    skipped_count = 0
    
    for current_path in scanner.walk_project_dirs(start_dir):
        # Try to create _AI.md
        # Pass verbose=False to avoid spamming "already exists"
        if init_ai_md(current_path, verbose=False, reset=reset):
            created_count += 1
        else:
            skipped_count += 1

        # Check for @AGGREGATE tag to stop recursion (Optimization: this logic is harder to replicate with flat generator)
        # However, scanner.walk_project_dirs uses os.walk which yields top-down. 
        # But we can't easily modify 'dirs' list of the generator.
        # So we might lose the "Stop recursion" optimization here if we use the simple generator.
        # But wait, init_all_recursive originally modified 'dirs' in place.
        # If we switch to scanner.walk_project_dirs, we lose that control.
        # Let's check if AGGREGATE tag optimization is critical.
        # It says "Stop recursing into subdirectories for this branch".
        # If we use the generator, we visit everything.
        # Maybe we should keep os.walk here OR update scanner to support pruning?
        # Supporting pruning in a generator is tricky (send()).
        
        # Let's revert to using os.walk here for now to keep the optimization, but use scanner.get_ignore_dirs()
        # to deduplicate ignore logic.
        pass
    
    # Re-implement using os.walk but with centralized ignore list
    ignore_dirs = scanner.get_ignore_dirs()
    
    for current_root, dirs, files in os.walk(start_dir):
        # Filter ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        current_path = Path(current_root)
        
        # Try to create _AI.md
        if init_ai_md(current_path, verbose=False, reset=reset):
            created_count += 1
        else:
            skipped_count += 1

        # Check for @AGGREGATE tag to stop recursion
        ai_file = current_path / "_AI.md"
        if ai_file.exists():
            try:
                content = io.read_text_safe(ai_file)
                if config.AGGREGATE_TAG in content:
                    # Stop recursing into subdirectories for this branch
                    dirs[:] = []
                    # console.info(f"  [Aggregate] Stopping recursion at {current_path.name}")
            except:
                pass
            
    console.success(f"Batch initialization complete.")
    console.info(f"  Processed: {created_count}")
    console.info(f"  Skipped (Already exists): {skipped_count}")

def update_ai_md(path_str):
    """
    Updates the _AI.md file in the specified directory with auto-generated content.
    Scans for files in the directory and populates the Inventory section.
    Supports @AGGREGATE tag for recursive scanning.
    """
    root = utils.get_project_root()
    # Handle path_str being a Path object or string
    if isinstance(path_str, Path):
        target_dir = path_str
    else:
        target_dir = (root / path_str).resolve()
        
    ai_file = target_dir / "_AI.md"
    
    if not ai_file.exists():
        return False

    try:
        content = ai_file.read_text(encoding='utf-8')
        
        # 1. Migration / Marker Check
        if config.MARKER_START not in content or config.MARKER_END not in content:
            # Check for new Tag-based header
            if "## @ARCH" in content:
                 # Insert markers after header
                 content = content.replace("## @ARCH", f"## @ARCH\n{config.MARKER_START}\n{config.MARKER_END}")
            
            # Legacy: Old default pattern (## 2. Architecture)
            elif "## 2. Architecture" in content:
                 # Try to migrate to ## @ARCH? Or just support legacy.
                 # Let's support legacy for now to avoid breaking existing files without explicit migration request.
                 # But if the user wants full token optimization, they should re-init.
                 # Here we just ensure update works.
                 content = content.replace("## 2. Architecture", f"## 2. Architecture\n{config.MARKER_START}\n{config.MARKER_END}")
            else:
                 # No place to insert
                 return False

        # 2. Scan Files
        code_files = []
        is_aggregate = config.AGGREGATE_TAG in content
        
        if is_aggregate:
            # Recursive scan for aggregated modules
            for r, ds, fs in os.walk(target_dir):
                ds[:] = [d for d in ds if d not in config.IGNORE_DIRS and not d.startswith('.')]
                for f in fs:
                    fpath = Path(r) / f
                    if fpath.suffix in config.CODE_EXTENSIONS:
                        rel = fpath.relative_to(target_dir)
                        code_files.append(str(rel).replace('\\', '/'))
        else:
            # Flat scan (default)
            for f in target_dir.iterdir():
                if f.is_file() and f.suffix in config.CODE_EXTENSIONS:
                    code_files.append(f.name)
        
        code_files.sort()
        
        # 3. Generate List
        if not code_files:
            list_md = "(No code files detected)"
        else:
            lines = []
            if is_aggregate:
                lines.append("<!-- (Aggregated View) -->")
            for fname in code_files:
                fpath = target_dir / fname
                desc = extract_docstring(fpath)
                desc_str = f": {desc}" if desc else ""
                lines.append(f"- [{fname}]({fname}){desc_str}")
            list_md = "\n".join(lines)
            
        # 4. Replace content between markers
        pattern = re.compile(
            re.escape(config.MARKER_START) + r".*?" + re.escape(config.MARKER_END),
            re.DOTALL
        )
        # Niki 3.0: Removed redundant file list. File navigation is now handled by @MAP section.
        # This section is reserved for future architecture diagrams or specialized content.
        new_section = f"{config.MARKER_START}\n<!-- (File list merged into @MAP section) -->\n{config.MARKER_END}"
        new_content = pattern.sub(new_section, content)
        
        if new_content != content:
            ai_file.write_text(new_content, encoding='utf-8')
            console.success(f"Updated {ai_file}")
            return True
            
    except Exception as e:
        console.warning(f"Failed to update {ai_file}: {e}")
        return False
        
    return True

def update_all_recursive(start_path="."):
    """
    Recursively updates _AI.md in all subdirectories.
    """
    root = utils.get_project_root()
    start_dir = (root / start_path).resolve()
    
    if not start_dir.exists():
        console.error(f"Directory not found: {start_dir}")
        return

    console.log(f"Updating _AI.md files in {start_dir}...")
    updated_count = 0
    
    for current_root, dirs, files in os.walk(start_dir):
        # Filter ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in config.IGNORE_DIRS and not d.startswith('.')]
        
        current_path = Path(current_root)
        if (current_path / "_AI.md").exists():
            if update_ai_md(current_path):
                updated_count += 1
                
    console.success(f"Batch update complete. Updated: {updated_count} files.")

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

    # Check 3: Dynamic Tag Audit (Header vs Body vs Syntax)
    # This provides the Traffic Light feedback (Red/Yellow/Blue)
    try:
        syntax.cmd_audit_tags(root)
    except Exception as e:
        errors.append(f"Tag Audit failed: {e}")

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

def parse_lightweight_docs(root_path):
    """
    Fallback parser when Doxygen is missing.
    Scans for class/struct definitions and updates _AI.md.
    """
    console.log("Running Lightweight Code Analysis (Doxygen not found)...")
    docs_map = {}
    
    # Regex for definitions
    # C++/Dart: class Name or struct Name
    # Capture group 1: kind (class/struct), group 2: Name
    def_pattern = re.compile(r'^\s*(?:abstract\s+)?(class|struct|enum)\s+(\w+)', re.MULTILINE)
    
    for file_path in scanner.walk_project_files(root_path, extensions=config.CODE_EXTENSIONS):
        # Find nearest _AI.md
        target_ai_md = find_nearest_ai_md(file_path, root_path)
        if not target_ai_md:
            continue
            
        try:
            content = io.read_text_safe(file_path)
        except Exception:
            continue
            
        matches = def_pattern.findall(content)
        if not matches:
            continue
            
        entry_lines = []
        for kind, name in matches:
            # Simple heuristic: Just list them
            entry_lines.append(f"*   **{kind} {name}** (Found in `{file_path.name}`) {config.BADGE_TEMPLATE}")
            
        if entry_lines:
            if target_ai_md not in docs_map:
                docs_map[target_ai_md] = []
            docs_map[target_ai_md].extend(entry_lines)
            
    return docs_map

def run_doxygen(root_path):
    doxyfile_path = root_path / config.DOXYFILE_PATH
    if not doxyfile_path.exists():
        # console.error(f"{doxyfile_path} not found.") # Optional: Warning
        return False
    
    doxygen_exe = find_doxygen_executable(root_path)
    if not doxygen_exe:
        return False # Fail silently to trigger fallback

    console.log(f"Running Doxygen ({doxygen_exe})...")
    # ... (rest of Doxygen logic)
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
        
        new_section_content = "## API Summary (Auto-generated)\n" + "\n".join(lines)
        
        if io.update_file_section(md_path, config.MARKER_START, config.MARKER_END, new_section_content):
            console.detail("Status", "Updated")
        else:
            # If markers not found, append
            # But wait, update_file_section returns False if markers not found OR if content unchanged (Wait, check logic)
            # logic: if not pattern.search: return False.
            # So if False, we check if we should append.
            # But wait, io.read_text_safe might fail.
            
            content = io.read_text_safe(md_path)
            if not content:
                console.error(f"Failed to read {md_path}")
                continue

            # Check if markers exist
            if config.MARKER_START in content:
                # If markers exist but update_file_section returned False, it means content was unchanged
                console.detail("Status", "No changes")
            else:
                # Markers not found, append
                new_content = content + "\n\n" + f"{config.MARKER_START}\n{new_section_content}\n{config.MARKER_END}"
                if io.write_text_safe(md_path, new_content):
                    console.detail("Status", "Updated (Appended)")
                else:
                    console.error(f"Failed to write {md_path}")

def update(root=None):
    """Main entry point for updating docs via Doxygen or Lightweight fallback."""
    if root is None:
        root = utils.get_project_root()
        
    if run_doxygen(root):
        console.log("Parsing XML and Updating _AI.md...")
        docs_map = parse_xml_docs(root)
    else:
        # Fallback
        docs_map = parse_lightweight_docs(root)
        
    if not docs_map:
        console.warning("No documentation data found to update.")
        return True

    update_ai_md_files(docs_map)
    console.success("Doc Sync Complete.")
    return True
