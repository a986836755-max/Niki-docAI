import json
import yaml
from pathlib import Path
from . import console

def read_text_safe(path: Path, encoding='utf-8', errors='replace') -> str:
    """Reads text from a file safely, handling errors."""
    try:
        return path.read_text(encoding=encoding, errors=errors)
    except Exception as e:
        console.warning(f"Failed to read file {path}: {e}")
        return ""

def read_lines_safe(path: Path, limit: int = -1, encoding='utf-8') -> list[str]:
    """Reads lines from a file safely, optionally limiting the count."""
    lines = []
    try:
        with open(path, 'r', encoding=encoding) as f:
            if limit == -1:
                lines = f.readlines()
            else:
                for _ in range(limit):
                    line = f.readline()
                    if not line: break
                    lines.append(line)
    except Exception:
        pass
    return lines

import re

def write_text_safe(path: Path, content: str, encoding='utf-8', newline=None) -> bool:
    """Writes text to a file safely."""
    try:
        with open(path, 'w', encoding=encoding, newline=newline) as f:
            f.write(content)
        return True
    except Exception as e:
        console.error(f"Failed to write file {path}: {e}")
        return False

def update_file_section(file_path: Path, marker_start: str, marker_end: str, new_content: str) -> bool:
    """
    Updates the content between two markers in a file.
    If markers are not found, returns False.
    If content is unchanged, returns True but does not write.
    """
    content = read_text_safe(file_path)
    if not content:
        return False
        
    pattern = re.compile(f"{re.escape(marker_start)}.*?{re.escape(marker_end)}", re.DOTALL)
    
    if not pattern.search(content):
        return False
        
    full_replacement = f"{marker_start}\n{new_content}\n{marker_end}"
    updated_content = pattern.sub(full_replacement, content)
    
    if updated_content != content:
        return write_text_safe(file_path, updated_content)
    
    return True

def read_yaml_safe(path: Path):
    """Reads a YAML file safely."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        console.warning(f"Failed to parse YAML {path}: {e}")
        return None

def read_json_safe(path: Path):
    """Reads a JSON file safely."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        console.warning(f"Failed to parse JSON {path}: {e}")
        return None

def write_json_safe(path: Path, data, indent=4) -> bool:
    """Writes data to a JSON file safely."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception as e:
        console.error(f"Failed to write JSON {path}: {e}")
        return False
