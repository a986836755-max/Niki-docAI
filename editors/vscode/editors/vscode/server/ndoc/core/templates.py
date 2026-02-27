from pathlib import Path
from typing import Dict, Any
from . import io

def get_template(name: str) -> str:
    """Load template from ndoc/templates directory."""
    
    # Try multiple paths to be robust
    possible_roots = [
        # 1. Standard source layout: src/ndoc/core/templates.py -> src/ndoc/templates
        Path(__file__).parent.parent / "templates", 
        
        # 2. VSIX installed layout (sometimes flattens or nests differently)
        # e.g. server/ndoc/core/templates.py -> server/ndoc/templates
        Path(__file__).parent.parent / "templates",
        
        # 3. Absolute fallback relative to entry point?
        # If we are running from server/ndoc/entry.py, then templates is server/ndoc/templates
        # Let's try to find 'ndoc' package root
    ]
    
    # Add a dynamic search up to 3 levels
    current = Path(__file__).parent
    for _ in range(3):
        possible_roots.append(current / "templates")
        if (current / "ndoc").exists(): # We are at src root
            possible_roots.append(current / "ndoc" / "templates")
        current = current.parent

    for root in possible_roots:
        template_path = root / name
        if template_path.exists():
             try:
                 return template_path.read_text(encoding='utf-8')
             except Exception:
                 pass
                 
    # CRITICAL DEBUGGING: If still not found, return error with paths
    # This helps user report where it looked
    debug_msg = f"Error: Template {name} not found.\nSearched in:\n" + "\n".join([str(p.resolve()) for p in possible_roots])
    return debug_msg

def render_document(body_template_name: str, title: str, context: str, tags: str, timestamp: str, **body_kwargs) -> str:
    """
    Render a full document by composing Header + Body + Footer.
    
    Args:
        body_template_name: Name of the body template file (e.g., 'map.md.tpl')
        title: Document Title (e.g., 'Project Map')
        context: Context description (e.g., 'Map | Project Structure')
        tags: Tags string (e.g., '@TAGS: @MAP')
        timestamp: Last Updated timestamp string
        **body_kwargs: Arguments to fill the body template
    
    Returns:
        Full rendered document content.
    """
    # 1. Load Components
    header_tpl = get_template("components/doc_header.tpl")
    footer_tpl = get_template("components/doc_footer.tpl")
    body_tpl = get_template(body_template_name)
    
    if not body_tpl:
        return f"Error: Template {body_template_name} not found."

    # 2. Render Header
    header_content = header_tpl.format(
        title=title,
        context=context,
        tags=tags,
        timestamp=timestamp
    )
    
    # 3. Render Body
    # We use safe formatting or standard format depending on need.
    # Standard format raises KeyError if missing args, which is good for strictness.
    body_content = body_tpl.format(**body_kwargs)
    
    # 4. Compose
    # Ensure double newline separation
    return f"{header_content.strip()}\n\n{body_content.strip()}\n\n{footer_tpl.strip()}\n"

