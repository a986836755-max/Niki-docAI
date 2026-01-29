"""
Daemon: Live Context Watcher.
守护进程：实时上下文监听器。

Implementation of file watching using watchdog with debounce mechanism.
"""
import time
import threading
from pathlib import Path
from typing import Callable, List, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from ndoc.models.config import ProjectConfig
from ndoc.flows import map_flow, context_flow, tech_flow

class DocChangeHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers document update with debounce.
    Supports incremental updates.
    """
    def __init__(self, config: ProjectConfig, debounce_interval: float = 2.0):
        self.config = config
        self.debounce_interval = debounce_interval
        self.last_change_time = 0.0
        self.timer: threading.Timer = None
        self.dirty_paths: Set[Path] = set()
        self.needs_structure_update = False

    def on_any_event(self, event: FileSystemEvent):
        # 1. Ignore directories (watchdog sends dir events, but we care about files mostly)
        # However, dir creation/deletion affects structure.
        
        src_path = Path(event.src_path)
        
        # 2. Ignore Meta Files (_*.md) to prevent infinite loops
        if src_path.name.startswith('_') and src_path.suffix == '.md':
            return
            
        # 3. Ignore common temporary/system files
        if any(part.startswith('.') for part in src_path.parts): # .git, .vscode, etc.
            return
        if src_path.suffix in ['.pyc', '.tmp', '.log']:
            return
        if '__pycache__' in src_path.parts:
            return

        # 4. Collect Changes
        print(f"[Watch] Detected change: {event.event_type} {src_path.name}")
        
        if event.is_directory or event.event_type in ['created', 'deleted', 'moved']:
            self.needs_structure_update = True
        
        # For modified files, we add them to dirty list
        if not event.is_directory:
            self.dirty_paths.add(src_path)
            
        self.trigger_update()

    def trigger_update(self):
        """
        Resets the timer for debounce.
        """
        if self.timer:
            self.timer.cancel()
        
        self.timer = threading.Timer(self.debounce_interval, self.run_update)
        self.timer.start()

    def run_update(self):
        """
        Execute the update flows.
        """
        print(f"\n[Watch] 🔄 Triggering update...")
        
        # Snapshot and clear state
        current_dirty_paths = list(self.dirty_paths)
        structure_update = self.needs_structure_update
        
        self.dirty_paths.clear()
        self.needs_structure_update = False
        
        try:
            # 1. Structure Update (Map Flow)
            if structure_update:
                print("[Watch] Structure changed, updating Map...")
                map_flow.run(self.config)
                # Tech flow might need update if new file types introduced
                tech_flow.run(self.config)
            
            # 2. Content Update (Context Flow)
            # We determine which directories need update
            dirty_dirs = set()
            for p in current_dirty_paths:
                if p.exists(): # Might be deleted
                    dirty_dirs.add(p.parent)
                else:
                    # If deleted, parent needs update (already covered by structure update usually, 
                    # but context doc also lists files)
                    dirty_dirs.add(p.parent)
            
            if structure_update and not dirty_dirs:
                # If only structure changed (e.g. empty dir added), context might not need update 
                # unless we want to generate _AI.md for new dir.
                # For safety, if structure changed, we might want to run full context or smart scan.
                # Let's keep it simple: Structure change -> usually implies file added/deleted -> dirty_dirs will be populated.
                pass

            if not dirty_dirs and not structure_update:
                # Check if dependency files changed
                dep_files = {'requirements.txt', 'pyproject.toml', 'package.json'}
                dep_changed = any(p.name in dep_files for p in current_dirty_paths)
                
                if dep_changed:
                    print("[Watch] Dependency file changed, updating Tech Snapshot...")
                    tech_flow.run(self.config)
                    return

                print("[Watch] No relevant changes found.")
                return

            print(f"[Watch] Updating Context for {len(dirty_dirs)} directories...")
            for d in dirty_dirs:
                # Only update if it's within project root
                if self.config.scan.root_path in d.parents or d == self.config.scan.root_path:
                    print(f"  -> {d.relative_to(self.config.scan.root_path)}")
                    context_flow.update_directory(d, self.config)
            
            print(f"[Watch] ✅ Update complete. Waiting for changes...\n")
        except Exception as e:
            print(f"[Watch] ❌ Update failed: {e}\n")

def start_watch_mode(config: ProjectConfig):
    """
    Starts the file watcher.
    This function blocks until interrupted (Ctrl+C).
    """
    event_handler = DocChangeHandler(config)
    observer = Observer()
    
    # Watch the root path recursively
    print(f"[Watch] Starting watchdog on {config.scan.root_path}")
    print(f"[Watch] Ignoring _*.md files to prevent loops.")
    
    observer.schedule(event_handler, str(config.scan.root_path), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
            # print(".", end="", flush=True) # Heartbeat
    except KeyboardInterrupt:
        observer.stop()
        print("\n[Watch] Stopping...")
    
    observer.join()
