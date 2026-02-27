"""
Capability Map Plugin (Action).
Detects project languages/capabilities and generates a report or auto-installs.
"""
from typing import Set
from ndoc.sdk.interfaces import ActionPlugin
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import EntityType

class CapabilityMapPlugin(ActionPlugin):
    """
    Action plugin to detect and report capabilities.
    """
    
    def ndoc_generate_docs(self, context: KernelContext):
        # 1. Collect all extensions in the project from entities
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        
        found_exts = set()
        for f in files:
            path = f.path
            if path.suffix:
                found_exts.add(path.suffix.lower())
                
        if not found_exts:
            return

        # 2. Map extensions to languages
        try:
            from ndoc.parsing import langs
            from ndoc.core import capabilities
        except ImportError:
            print("[CapabilityMap] Core modules not found.")
            return
            
        required_languages: Set[str] = set()
        for ext in found_exts:
            lang_id = langs.get_lang_id_by_ext(ext)
            if lang_id:
                required_languages.add(lang_id)
                
        if not required_languages:
            return
            
        print(f"[CapabilityMap] Detected languages: {', '.join(required_languages)}")

        # 3. Ensure capabilities are installed
        try:
            # We assume auto_install=True for 'caps' command usage
            # If this plugin is run as part of 'all', we might want config control.
            # But for now, ensuring environment readiness is good.
            capabilities.CapabilityManager.ensure_languages(required_languages, auto_install=True)
            
            # Ensure optional packages
            capabilities.CapabilityManager.ensure_package("chromadb", auto_install=True)
            
        except Exception as e:
            print(f"[CapabilityMap] Error checking capabilities: {e}")
