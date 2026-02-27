"""
Command: Watch Mode.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig
from ndoc.daemon import start_watch_mode

@ndoc_command(name="watch", help="Start DAEMON mode to auto-update docs on file changes", group="Core")
def run(config: ProjectConfig) -> bool:
    """
    Start file system watcher.
    """
    start_watch_mode(config)
    # watch mode blocks, so we return True when it exits cleanly
    return True
