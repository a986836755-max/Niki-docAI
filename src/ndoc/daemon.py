"""
Daemon: Live Context Watcher.
守护进程：实时上下文监听器。

Implementation of file watching using watchdog with debounce mechanism.
"""
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ndoc.core.logger import logger
from ndoc.models.config import ProjectConfig
from ndoc.parsing.langs import get_lang_id_by_ext
from ndoc.core import capabilities

# Legacy flows are removed. Daemon should use Kernel or specific plugins?
# Or maybe we just keep it simple for now and trigger "ndoc all" logic?
# But that's heavy.
# Daemon logic needs to be rewritten to use ECS incrementally.
# For Phase 1 cleanup, let's just remove the imports and stub the handlers to avoid crash.
# Or better, make it call the new entry point helper?

import threading
from typing import Callable, List, Set
from watchdog.events import FileSystemEvent
from ndoc.brain.hippocampus import Hippocampus, ActionType
from ndoc.interfaces import lsp

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
        self.hippocampus = Hippocampus() # Short-term memory
        # Get LSP Service instance
        self.lsp_service = lsp.get_service(config.scan.root_path)

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
        
        # Record to Hippocampus
        action = ActionType.EDIT
        if event.event_type == 'created': action = ActionType.OPEN # Approximation
        elif event.event_type == 'deleted': action = ActionType.CLOSE # Approximation
        
        self.hippocampus.record(str(src_path), action)
        
        if event.is_directory or event.event_type in ['created', 'deleted', 'moved']:
            self.needs_structure_update = True
        
        # For modified files, we add them to dirty list
        if not event.is_directory:
            # Proactive Capability Check for new files
            if event.event_type == 'created':
                # capability_flow.check_single_file(src_path)
                # Disabled capability flow in daemon for now
                pass
            
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
        
        # Log Hippocampus Heatmap
        heat_map = self.hippocampus.get_file_heat()
        if heat_map:
            top_files = sorted(heat_map.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"[Brain] 🔥 Hot files: {', '.join([Path(f).name for f, _ in top_files])}")
        
        self.dirty_paths.clear()
        self.needs_structure_update = False
        
        try:
            # 1. Map Flow (Structure)
            if structure_update:
                print("[Watch] Structure changed, updating Map...")
                # map_flow.run(self.config)
                # TODO: Trigger Kernel Map Plugin
                pass
            
            # 2. Update Context for changed files/dirs
            processed_dirs = set()
            for path in current_dirty_paths:
                # Update LSP Index
                try:
                    self.lsp_service.update_file(path)
                    self.lsp_service.invalidate_context_cache(path)
                except Exception as e:
                    logger.warning(f"Failed to update LSP for {path}: {e}")
                
                # Find nearest _AI.md parent
                d = path if path.is_dir() else path.parent
                
                # Walk up until root or found _AI.md (optimization: just update parent dir context)
                if d not in processed_dirs:
                    processed_dirs.add(d)
                    if self.config.scan.root_path in d.parents or d == self.config.scan.root_path:
                        # logger.info(f"  -> {d.relative_to(self.config.scan.root_path)}")
                        # context_flow.update_directory(d, self.config)
                        # TODO: Trigger Kernel Context Plugin for specific dir
                        pass

            logger.info("[Watch] Syncing Todos and checking for Archive...")
            # status_flow.update_next_file(self.config)
            # Always run archive flow to handle [x] tasks in _NEXT.md
            from ndoc.flows import archive_flow
            archive_flow.run(self.config)

            # 4. Global Metadata Flows (Cached)
            logger.info("[Watch] Updating Tech Stack, Dependencies, Symbol Index and Data Registry...")
            # arch_flow.run(self.config) # Replaces tech_flow and deps_flow
            # symbols_flow.run(self.config) # Deprecated
            
            # Temporary: Just trigger full update if something changed
            # This is heavy but correct for now
            # from ndoc.entry import _run_ecs_pipeline
            # _run_ecs_pipeline(self.config.scan.root_path)
            # Disabled full update in daemon to avoid blocking user typing
            # data_flow.run(self.config)
            pass
            
            logger.info(f"[Watch] ✅ Update complete. Waiting for changes...\n")
        except Exception as e:
            logger.error(f"[Watch] ❌ Update failed: {e}\n")
            import traceback
            logger.error(traceback.format_exc())

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
    
    # Run initial capability check
    # capability_flow.run(config)
    # Disabled for Phase 1 cleanup
    pass
    
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
