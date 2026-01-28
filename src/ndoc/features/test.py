import sys
import datetime
import re
from pathlib import Path
from ndoc.core import console
from ndoc.core import utils
from ndoc.core import config

def update_doc_status(file_path):
    """
    Updates the Status Badge and Last Verified date in the given markdown file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        console.warning(f"Failed to read {file_path}: {e}")
        return False

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    new_verified_str = config.VERIFIED_TEMPLATE.format(date=today_str)
    
    # 1. Update/Insert Badge
    if config.BADGE_REGEX.search(content):
        # Update existing badge
        content = config.BADGE_REGEX.sub(config.BADGE_TEMPLATE, content)
    else:
        # Insert badge after the first header (Title)
        match = re.search(r"^# .+\n", content, re.MULTILINE)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + "\n" + config.BADGE_TEMPLATE + "\n" + content[insert_pos:]
        else:
            content = config.BADGE_TEMPLATE + "\n\n" + content

    # 2. Update/Insert Last Verified
    if config.VERIFIED_REGEX.search(content):
        content = config.VERIFIED_REGEX.sub(new_verified_str, content)
    else:
        # Insert after badge
        match = config.BADGE_REGEX.search(content)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + "\n" + new_verified_str + "\n" + content[insert_pos:]
        else:
            content += f"\n\n{new_verified_str}\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return True

def cmd_test(root, args):
    """
    Runs project tests and updates documentation status on success.
    """
    console.step("[Phase 1] Building Tests...")
    
    engine_dir = root / "engine"
    build_dir = engine_dir / "build"
    
    # Ensure build directory exists
    if not build_dir.exists():
        console.warning("Build directory not found. Running CMake configuration...")
        utils.run_command(f'cmake -B "{build_dir}" -S "{engine_dir}" -DCMAKE_BUILD_TYPE=Release', cwd=root)

    # Build unit_tests target
    try:
        utils.run_command(f'cmake --build "{build_dir}" --target unit_tests --config Release', cwd=root)
    except Exception:
        console.error("Failed to build tests.")
        sys.exit(1)

    console.step("[Phase 2] Running Tests (CTest)...")
    
    # Run CTest
    try:
        utils.run_command('ctest -C Release --output-on-failure', cwd=build_dir)
        console.success("All tests passed!")
    except Exception:
        console.error("Tests failed! Documentation status will NOT be updated.")
        sys.exit(1)

    console.step("[Phase 3] Updating Documentation Status...")
    
    # Find all _AI.md files
    target_files = list(root.rglob("_AI.md"))
    
    updated_count = 0
    for file_path in target_files:
        if any(part in config.IGNORE_DIRS for part in file_path.parts):
            continue
            
        if update_doc_status(file_path):
            console.log(f"  Verified: {file_path.relative_to(root)}")
            updated_count += 1
            
    console.success(f"Updated verification status in {updated_count} files.")
