from pathlib import Path
from typing import Dict, Any
from . import io

def get_template(name: str) -> str:
    """Load template from ndoc/templates directory."""
    # Assuming this file is in src/ndoc/core/templates.py
    # Templates are in src/ndoc/templates/
    template_path = Path(__file__).parent.parent / "templates" / name
    if template_path.exists():
        return io.read_text(template_path)
    return ""

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

