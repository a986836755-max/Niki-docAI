from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from . import io
from ..models.config import TemplateConfig

# Global Template Configuration
_CONFIG: Optional[TemplateConfig] = None
_ENV: Optional[Environment] = None

def configure(config: TemplateConfig) -> None:
    """
    配置模板系统 (Configure template system).
    """
    global _CONFIG, _ENV
    _CONFIG = config
    
    # Initialize Jinja2 Environment
    search_paths = []
    
    # 1. Base template dir in config (if any)
    if config.base_dir and config.base_dir.exists():
        search_paths.append(str(config.base_dir))
        
    # 2. Default internal templates
    default_templates = Path(__file__).parent.parent / "templates"
    if default_templates.exists():
        search_paths.append(str(default_templates))
        
    _ENV = Environment(
        loader=FileSystemLoader(search_paths),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )

def get_template(name: str) -> str:
    """
    Load template content (Legacy support, use render_document instead).
    """
    # 1. Check Overrides
    if _CONFIG and name in _CONFIG.overrides:
        override_path = _CONFIG.overrides[name]
        if override_path.exists():
            return io.read_text(override_path) or ""
    
    # Use Jinja loader to find file
    if _ENV:
        try:
            return _ENV.loader.get_source(_ENV, name)[0]
        except Exception:
            pass
            
    return ""

def render_document(body_template_name: str, title: str, context: str, tags: str, timestamp: str, **body_kwargs) -> str:
    """
    Render a full document by composing Header + Body + Footer using Jinja2.
    """
    # Ensure environment is initialized
    if _ENV is None:
        # Fallback config
        configure(TemplateConfig())
        
    # 1. Resolve Template Names
    header_name = _CONFIG.header if _CONFIG else "components/doc_header.tpl"
    footer_name = _CONFIG.footer if _CONFIG else "components/doc_footer.tpl"
    
    # Check overrides
    if _CONFIG and body_template_name in _CONFIG.overrides:
        # If overridden by a file path, we might need to load it directly
        # But Jinja works best with loaders. 
        # For simplicity, if override is absolute path, we read it and create template from string.
        override_path = _CONFIG.overrides[body_template_name]
        if override_path.exists():
            body_tpl = _ENV.from_string(io.read_text(override_path) or "")
        else:
            return f"Error: Override template {override_path} not found."
    else:
        try:
            body_tpl = _ENV.get_template(body_template_name)
        except Exception as e:
            return f"Error: Template {body_template_name} not found: {e}"

    # 2. Render Header
    try:
        header_tpl = _ENV.get_template(header_name)
        header_content = header_tpl.render(
            title=title,
            context=context,
            tags=tags,
            timestamp=timestamp
        )
    except Exception as e:
        return f"Error: Header template {header_name} failed: {e}"
        
    # 3. Render Body
    try:
        # Pass all kwargs to body template
        body_content = body_tpl.render(**body_kwargs)
    except Exception as e:
        return f"Error: Body template {body_template_name} failed: {e}"

    # 4. Render Footer
    try:
        footer_tpl = _ENV.get_template(footer_name)
        footer_content = footer_tpl.render()
    except Exception as e:
        return f"Error: Footer template {footer_name} failed: {e}"
    
    # 5. Compose
    return f"{header_content.strip()}\n\n{body_content.strip()}\n\n{footer_content.strip()}\n"

