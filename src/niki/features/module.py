from pathlib import Path
from niki.core import console
from niki.core import utils
from niki.core import config

def create_module(root, name):
    base_path = root / "engine" / "modules" / name

    if base_path.exists():
        console.error(f"Module '{name}' already exists at {base_path}")
        return

    console.info(f"Creating module: {name}...")

    utils.ensure_directory(base_path / "components")
    utils.ensure_directory(base_path / "systems")
    
    # We need to access templates from config. 
    # Ensure config has these templates.
    
    readme_tmpl = getattr(config, "README_TEMPLATE", "# Module: {module_name}\n")
    ai_tmpl = getattr(config, "AI_TEMPLATE", "# {module_name} [DOMAIN:{domain_tag}]\n")
    
    with open(base_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_tmpl.format(module_name=name))
        
    with open(base_path / "_AI.md", "w", encoding="utf-8") as f:
        f.write(ai_tmpl.format(module_name=name, domain_tag=name.upper()))

    console.success(f"Module {name} created.")

def cmd_create(root, name):
    create_module(root, name)
