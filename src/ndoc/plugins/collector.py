"""
Standard File Collector Plugin.
"""
from pathlib import Path
from typing import List
from ndoc.sdk.interfaces import SensorPlugin
from ndoc.sdk.models import Entity, EntityType

class FileCollectorPlugin(SensorPlugin):
    """
    Standard plugin to collect file entities from disk.
    """
    def ndoc_collect_entities(self, root_path: str) -> List[Entity]:
        root = Path(root_path).resolve()
        # Ensure root is absolute and exists
        if not root.exists():
            print(f"[ERROR] Collector: Root path does not exist: {root}")
            return []
            
        entities = []
        
        # Simple recursive walk for now (can use ignore patterns later)
        # TODO: Integrate with existing ignore logic
        print(f"[DEBUG] Collector scanning: {root}")
        
        # Use simple os.walk or Path.rglob
        # Note: In Pilot, rglob failed silently or returned empty?
        # Let's try os.walk for robustness
        import os
        count = 0
        
        # Debug: Print root type
        # print(f"Root type: {type(root)}")
        
        try:
            # Walk from root (absolute path)
            for dirpath, dirnames, filenames in os.walk(str(root)):
                # Filter directories
                # IMPORTANT: Don't just check startswith('.').
                # We must allow normal directories.
                # Standard practice: skip hidden dirs (.git, .vscode, etc)
                # But 'src', 'ndoc' should be allowed.
                # The issue might be if some dirs are skipped incorrectly.
                
                # Exclude hidden directories in-place
                # Original logic: dirnames[:] = [d for d in dirnames if not d.startswith('.')]
                # But this filters out .ndoc which might be intended?
                # Actually, .ndoc is usually hidden config.
                
                # The issue with os.walk is that modifying dirnames in-place affects recursion.
                # If we filter too aggressively, we skip subtrees.
                
                # Let's use list comprehension for clarity and robustness
                # Keep only dirs that:
                # 1. Do not start with '.' OR are literally '.' (current dir)
                # 2. Are not in the blacklist
                
                allowed_dirs = []
                for d in dirnames:
                    is_hidden = d.startswith('.') and d != '.'
                    is_blacklisted = d in ['__pycache__', 'node_modules', 'dist', 'build', 'venv', 'env', 'site-packages']
                    
                    if not is_hidden and not is_blacklisted:
                        allowed_dirs.append(d)
                        
                # Update dirnames in-place to affect os.walk recursion
                dirnames[:] = allowed_dirs
                
                for filename in filenames:
                    if filename.startswith('.'): continue
                    
                    # Construct full path
                    path = Path(dirpath) / filename
                    
                    # Basic ID strategy: Relative Path string
                    try:
                        rel_path = path.relative_to(root)
                        # Normalize to POSIX for consistency across OS
                        entity_id = rel_path.as_posix()
                        
                        entity = Entity(
                            id=entity_id,
                            type=EntityType.FILE,
                            name=path.name,
                            path=path
                        )
                        entities.append(entity)
                        count += 1
                    except ValueError:
                        pass
        except Exception as e:
            print(f"[ERROR] Collector failed: {e}")
            
        print(f"[DEBUG] Collector found {count} files")
        # FORCE RETURN
        return entities
                
        return entities
