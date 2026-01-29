import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ndoc.core import console, utils, config
from ndoc.features import map, docs, verify, todo, graph

class NdocEventHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers ndoc updates.
    """
    def __init__(self, root: Path):
        self.root = root
        self.last_map_update = 0
        self.last_todo_update = 0
        # Cooldown in seconds to prevent spamming updates
        self.cooldown = 2.0 

    def on_modified(self, event):
        if event.is_directory:
            return
        self._process_event(event.src_path, "modified")

    def on_created(self, event):
        if event.is_directory:
            return
        self._process_event(event.src_path, "created")

    def on_deleted(self, event):
        if event.is_directory:
            return
        self._process_event(event.src_path, "deleted")

    def _process_event(self, path_str, event_type):
        path = Path(path_str)
        
        # Ignore meta files to prevent loops (except some)
        if path.name.startswith("_") and path.suffix == ".md":
            # If user edits _AI.md manually, we might want to verify?
            # But generally we ignore our own outputs
            return

        # Ignore ignored dirs
        if any(p in path.parts for p in config.IGNORE_DIRS):
            return

        console.info(f"Detected {event_type}: {path.name}")
        
        current_time = time.time()
        
        # 1. Update TODOs (Throttle)
        if current_time - self.last_todo_update > self.cooldown:
            console.log("  -> Updating TODOs...")
            todo.update_next_md(self.root)
            
            # Also update Rules (batched with TODOs for now)
            if current_time - self.last_rules_update > self.cooldown:
                console.log("  -> Updating Rules...")
                inj = injector.UniversalInjector(self.root)
                inj.register("RULES", injector.collect_rules)
                # We could register other handlers here too
                
                rules_path = self.root / "_RULES.md"
                if rules_path.exists():
                    inj.update_file(rules_path)
                self.last_rules_update = current_time

            self.last_todo_update = current_time
            
        # 2. Update Map/Graph if structure changed (Created/Deleted)
        # Or if it's a significant file
        if event_type in ["created", "deleted"] or (current_time - self.last_map_update > 5.0):
            console.log("  -> Updating Map & Graph...")
            map.update_map(self.root)
            graph.cmd_graph(self.root)
            self.last_map_update = current_time

        # 3. Verify Rules (Fast check on single file?)
        # For now, maybe just run verify on the whole project is too slow?
        # Let's just log that we saw it.
        
        # 4. Auto-init _AI.md for new directories?
        # Watchdog doesn't always give dir events reliably on all OS, 
        # but if a file is created in a new dir, we might want to check.
        if event_type == "created":
            parent_dir = path.parent
            if not (parent_dir / "_AI.md").exists():
                 console.log(f"  -> Auto-creating _AI.md for {parent_dir.name}")
                 docs.init_ai_md(parent_dir, verbose=False)


def start_watch(root: Path):
    """
    Starts the file system watcher.
    """
    console.header("Niki-docAI Watch Daemon")
    console.info(f"Watching: {root}")
    console.info("Press Ctrl+C to stop.")
    
    event_handler = NdocEventHandler(root)
    observer = Observer()
    observer.schedule(event_handler, str(root), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.info("\nStopping watch daemon...")
    
    observer.join()

def cmd_watch(root: Path):
    start_watch(root)
