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
from ndoc.flows import map_flow, context_flow, tech_flow, todo_flow, symbols_flow, data_flow, deps_flow, archive_flow

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
            # 1. Map Flow (Structure)
            if structure_update:
                print("[Watch] Structure changed, updating Map...")
                map_flow.run(self.config)
            
            # 2. Context Flow (Incremental AI Docs)
            dirty_dirs = set()
            for p in current_dirty_paths:
                if p.exists():
                    dirty_dirs.add(p.parent)
                else:
                    # If deleted, parent needs update
                    dirty_dirs.add(p.parent)
            
            if dirty_dirs:
                print(f"[Watch] Updating Context for {len(dirty_dirs)} directories...")
                for d in dirty_dirs:
                    if self.config.scan.root_path in d.parents or d == self.config.scan.root_path:
                        print(f"  -> {d.relative_to(self.config.scan.root_path)}")
                        context_flow.update_directory(d, self.config)

            # 3. Todo Flow & Archive Flow
            print("[Watch] Syncing Todos and checking for Archive...")
            todo_flow.run(self.config)
            # Always run archive flow to handle [x] tasks in _NEXT.md
            archive_flow.run(self.config)

            # 4. Global Metadata Flows (Cached)
            print("[Watch] Updating Tech Stack, Dependencies, Symbol Index and Data Registry...")
            tech_flow.run(self.config)
            deps_flow.run(self.config)
            symbols_flow.run(self.config)
            data_flow.run(self.config)
            
            print(f"[Watch] ✅ Update complete. Waiting for changes...\n")
        except Exception as e:
            print(f"[Watch] ❌ Update failed: {e}\n")
            import traceback
            traceback.print_exc()

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
