from pathlib import Path
from ndoc.core import console, config

def init_meta_files(root: Path, reset: bool = False):
    """Initialize toolchain meta files."""
    meta_files = {
        "_RULES.md": getattr(config, "RULES_TEMPLATE", ""),
        "_TECH.md": getattr(config, "TECH_HEADER_TEMPLATE", getattr(config, "TECH_TEMPLATE", "")),
        "_GLOSSARY.md": getattr(config, "GLOSSARY_TEMPLATE", ""),
        "_SYNTAX.md": getattr(config, "SYNTAX_TEMPLATE", ""),
        "_MEMORY.md": getattr(config, "MEMORY_TEMPLATE", ""),
        "_MAP.md": getattr(config, "MAP_TEMPLATE", ""),
        "_ARCH.md": getattr(config, "ARCH_TEMPLATE", ""),
        "_NEXT.md": getattr(config, "NEXT_STEP_TEMPLATE", ""),
    }
    
    created_any = False
    
    for filename, template in meta_files.items():
        if not template: continue
        path = root / filename
        
        if path.exists() and not reset:
            continue
            
        if reset and path.exists():
            console.warning(f"Overwriting {filename}...")
        elif not path.exists():
            console.info(f"Auto-creating {filename}...")
            
        try:
            # Provide common context for all templates
            content = template.format(
                version=config.TOOLCHAIN_VERSION,
                mermaid_graph="graph TD;\n    root[Root] --> ...",
                module_name="Project"
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            created_any = True
        except Exception as e:
            console.error(f"Failed to write {filename}: {e}")
            
    if created_any:
        console.success("Initialization/Update Complete.")
    elif reset:
        console.success("Reset Complete.")

def check_and_auto_init(root: Path):
    """Check if meta files exist, if not, auto-initialize them."""
    # Check for a key file, e.g., _RULES.md
    if not (root / "_RULES.md").exists():
        console.info("Project not initialized. Running auto-initialization...")
        init_meta_files(root, reset=False)
