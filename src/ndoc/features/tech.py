import re
import yaml
from pathlib import Path
from ndoc.core import console, config, utils

# -----------------------------------------------------------------------------
# Dependency Scanning Logic (formerly deps_scanner.py)
# -----------------------------------------------------------------------------

def scan_languages(root):
    """Scans project to identify core languages based on file extensions."""
    languages = {}
    ext_map = {
        '.cpp': 'C++', '.hpp': 'C++', '.h': 'C++', '.cc': 'C++',
        '.dart': 'Dart',
        '.py': 'Python',
        '.rs': 'Rust',
        '.lua': 'Lua',
        '.js': 'JavaScript', '.ts': 'TypeScript',
        '.c': 'C',
        '.cmake': 'CMake', 'CMakeLists.txt': 'CMake'
    }
    
    # Simple heuristic: count files
    counts = {}
    
    # Limit depth to avoid scanning huge node_modules or build dirs
    dirs_to_scan = [
        root / 'engine',
        root / 'client',
        root / 'scripts',
        root / 'tools'
    ]
    
    for d in dirs_to_scan:
        if not d.exists(): continue
        for p in d.rglob('*'):
            if p.is_file():
                ext = p.suffix.lower()
                name = p.name
                
                lang = None
                if name in ext_map: # Check full filename first (like CMakeLists.txt)
                    lang = ext_map[name]
                elif ext in ext_map:
                    lang = ext_map[ext]
                    
                if lang:
                    counts[lang] = counts.get(lang, 0) + 1

    # Filter out low noise
    for lang, count in counts.items():
        if count > 0: # Threshold can be adjusted
            languages[lang] = count
            
    return languages

def scan_build_tools(root):
    """Detects build tools based on configuration files."""
    tools = []
    
    if (root / 'engine' / 'CMakeLists.txt').exists():
        tools.append({'name': 'cmake', 'version': 'Detected', 'source': 'engine/CMakeLists.txt'})
        
    if (root / 'client' / 'pubspec.yaml').exists():
        tools.append({'name': 'flutter', 'version': 'Detected', 'source': 'client/pubspec.yaml'})
        
    # Check for others if needed (gradle, cargo, etc.)
    return tools

def scan_cmake(file_path):
    """Scans CMakeLists.txt for FetchContent_Declare versions."""
    deps = []
    if not file_path.exists():
        console.warning(f"CMake file not found: {file_path}")
        return deps

    content = file_path.read_text(encoding='utf-8')
    
    # Regex to capture library name and GIT_TAG
    pattern = re.compile(r'FetchContent_Declare\s*\(\s*([a-zA-Z0-9_]+).*?GIT_TAG\s+([^\s\)]+)', re.DOTALL | re.IGNORECASE)
    
    matches = pattern.findall(content)
    for name, tag in matches:
        deps.append({
            'name': name.lower(),
            'version': tag.strip(),
            'source': 'CMake'
        })
        
    return deps

def scan_pubspec(file_path):
    """Scans pubspec.yaml for dependency versions."""
    deps = []
    if not file_path.exists():
        console.warning(f"Pubspec file not found: {file_path}")
        return deps

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if 'environment' in data and 'sdk' in data['environment']:
            deps.append({
                'name': 'dart_sdk', 
                'version': data['environment']['sdk'],
                'source': 'Pubspec'
            })
            
        if 'dependencies' in data:
            for name, ver in data['dependencies'].items():
                version_str = "Unknown"
                if isinstance(ver, str):
                    version_str = ver
                elif isinstance(ver, dict):
                    if 'sdk' in ver:
                        version_str = f"sdk: {ver['sdk']}"
                    elif 'version' in ver:
                        version_str = ver['version']
                    elif 'path' in ver:
                        version_str = "local"
                
                deps.append({
                    'name': name,
                    'version': version_str,
                    'source': 'Pubspec'
                })
                    
    except Exception as e:
        console.warning(f"Failed to parse pubspec.yaml: {e}")
        
    return deps

def get_project_details(root):
    """Aggregates detailed project info from all sources."""
    details = {
        'languages': scan_languages(root),
        'build_tools': scan_build_tools(root),
        'libs_engine': [],
        'libs_client': [],
        'versions': {} # Keep flattened versions for backward compat if needed
    }
    
    # 1. Engine (CMake)
    cmake_path = root / "engine" / "CMakeLists.txt"
    details['libs_engine'] = scan_cmake(cmake_path)
    
    # Extract CMake version
    if cmake_path.exists():
        content = cmake_path.read_text(encoding='utf-8')
        m = re.search(r'cmake_minimum_required\s*\(VERSION\s+([\d\.]+)\)', content, re.IGNORECASE)
        if m:
            # Update the cmake tool entry if exists
            for tool in details['build_tools']:
                if tool['name'] == 'cmake':
                    tool['version'] = f"{m.group(1)}+"

    # 2. Client (Pubspec)
    pubspec_path = root / "client" / "pubspec.yaml"
    details['libs_client'] = scan_pubspec(pubspec_path)
    
    return details

# -----------------------------------------------------------------------------
# Markdown Generation Logic (formerly update_tech_stack.py)
# -----------------------------------------------------------------------------

def update(root):
    """Generates _TECH.md from actual project dependencies."""
    console.step("Scanning Project Dependencies...")
    
    details = get_project_details(root)
    
    # Organize data for rendering
    # Structure: { "Category Name": [ {name, version, desc, source} ] }
    categories = {}
    
    # Helper to process items
    def process_item(key, version, source="Unknown"):
        kb_entry = config.TECH_KNOWLEDGE_BASE.get(key)
        
        display_name = key
        category = "5. Other Dependencies"
        desc = ""
        
        if kb_entry:
            display_name = kb_entry.get("name", key)
            category = kb_entry.get("category", category)
            desc = kb_entry.get("desc", "")
        else:
            # Auto-capitalize for unknown items
            display_name = key.replace('_', ' ').title()
            
        if category not in categories:
            categories[category] = []
            
        # Avoid duplicates (simple check by name)
        for existing in categories[category]:
            if existing['name'] == display_name:
                # If existing is 'Detected' or 'Unknown' and new one has specific version, update it
                if existing['version'] in ['Detected', 'Unknown'] and version not in ['Detected', 'Unknown']:
                    existing['version'] = version
                return

        categories[category].append({
            "name": display_name,
            "version": version,
            "desc": desc,
            "source": source
        })

    # 1. Process Languages
    for lang, count in details['languages'].items():
        process_item(lang.lower(), "Detected", "File Scan")
        
    # 2. Process Build Tools
    for tool in details['build_tools']:
        process_item(tool['name'], tool['version'], tool['source'])
        
    # 3. Process Engine Libs
    for lib in details['libs_engine']:
        process_item(lib['name'], lib['version'], lib['source'])
        
    # 4. Process Client Libs
    for lib in details['libs_client']:
        process_item(lib['name'], lib['version'], lib['source'])

    # Sort categories
    sorted_cats = sorted(categories.keys())
    
    # Generate Markdown
    lines = []
    
    # Header
    lines.append(config.TECH_HEADER_TEMPLATE.format(toolchain=config.TOOLCHAIN_VERSION))
    
    for cat in sorted_cats:
        lines.append(f"## {cat}")
        items = categories[cat]
        # Sort items by name
        items.sort(key=lambda x: x['name'])
        
        for item in items:
            line = f"*   **{item['name']}**: `{item['version']}`"
            if item['desc']:
                line += f" ({item['desc']})"
            # Optional: Add source info in comments or tooltip? 
            # For now, keep it clean as per original template
            lines.append(line)
        lines.append("") # Empty line after section

    content = "\n".join(lines)
    
    tech_md_path = root / "_TECH.md"
    
    # Check if changed
    if tech_md_path.exists():
        old_content = tech_md_path.read_text(encoding='utf-8')
        if old_content == content:
            console.info("_TECH.md is up to date.")
            return True
            
    tech_md_path.write_text(content, encoding='utf-8')
    console.success(f"Updated {tech_md_path.name}")
    
    # Debug output
    console.log("Generated Categories:")
    for cat in sorted_cats:
        console.log(f"  - {cat} ({len(categories[cat])} items)")
        
    return True
