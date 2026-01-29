import re
import os
from pathlib import Path
from typing import Callable, Dict, Any
from ndoc.core import console, config, utils
from ndoc.base import io, scanner

# Generic Pattern: <!-- NIKI_AUTO_{KEY}_START --> ... <!-- NIKI_AUTO_{KEY}_END -->
# We capture the KEY in group 2.
BLOCK_PATTERN = re.compile(r'(<!-- NIKI_AUTO_([A-Z0-9_]+)_START -->)(.*?)(<!-- NIKI_AUTO_\2_END -->)', re.DOTALL)

class UniversalInjector:
    """
    The engine behind the Hybrid Document Model.
    Scans documents for injection markers and updates them with dynamic content.
    """
    # !RULE: Injectors must always preserve user content outside markers.
    def __init__(self, root: Path):
        self.root = root
        self.handlers: Dict[str, Callable[[Path], str]] = {}

    def register(self, key: str, handler: Callable[[Path], str]):
        """Register a handler for a specific block key (e.g., 'RULES')."""
        self.handlers[key] = handler

    def update_file(self, file_path: Path) -> bool:
        """
        Scans a file for blocks and updates them. 
        Returns True if changes were made.
        """
        if not file_path.exists():
            return False

        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return False

        def replacer(match):
            start_tag = match.group(1)
            key = match.group(2)
            current_content = match.group(3)
            end_tag = match.group(4)

            handler = self.handlers.get(key)
            if not handler:
                # If no handler is registered, leave it alone
                # (Or maybe log a warning?)
                return match.group(0)

            try:
                # Invoke handler to get new content
                new_inner_content = handler(self.root)
                # Normalize newlines
                new_inner_content = new_inner_content.strip()
                
                # Construct the new block
                # We ensure there are newlines around the content for readability
                return f"{start_tag}\n{new_inner_content}\n{end_tag}"
            except Exception as e:
                console.error(f"Error in handler for '{key}' in {file_path.name}: {e}")
                return match.group(0) # Fallback to original

        new_content, count = BLOCK_PATTERN.subn(replacer, content)

        if count > 0 and new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            console.success(f"Updated {file_path.name}: Refreshed {count} live zones.")
            return True
            
        return False

# --- Handlers ---

def collect_rules(root: Path) -> str:
    """
    Scans the codebase for !RULE: comments.
    Returns a Markdown list.
    """
    # Regex to find rules in comments.
    # Matches:
    #   # [!]RULE: ...
    #   // [!]RULE: ...
    #   <!-- [!]RULE: ... -->
    # Enforces that !RULE comes immediately after the comment start to avoid false positives in strings.
    rule_pattern = re.compile(r'(?:#|//|<!--)\s*!RULE:\s*(.*?)(?:\s*-->)?\s*$', re.IGNORECASE)
    rules = []

    for file_path in scanner.walk_project_files(root):
        # Skip meta files (start with _)
        if file_path.name.startswith('_') and file_path.name.endswith('.md'):
            continue
            
        lines = io.read_lines_safe(file_path)
        for i, line in enumerate(lines):
            match = rule_pattern.search(line)
            if match:
                rule_text = match.group(1).strip()
                # Store rule info
                rules.append({
                    'text': rule_text,
                    'file_path': file_path,
                    'line': i + 1
                })

    if not rules:
        return "*No rules found in code.*"

    # Sort rules by file and line
    rules.sort(key=lambda x: (str(x['file_path']), x['line']))

    lines = []
    for r in rules:
        link = utils.make_file_link(r['file_path'], root, r['line'])
        lines.append(f"*   **{r['text']}** <br> ↳ Ref: `{link}`")

    return "\n".join(lines)

