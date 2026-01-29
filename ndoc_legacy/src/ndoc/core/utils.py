# Facade for backward compatibility
from ndoc.base import console
from ndoc.base.paths import get_project_root, ensure_directory
from ndoc.base.cmd import run_command, find_flatc
from ndoc.base.scanner import get_ignore_dirs, walk_project_files
from ndoc.base.formatter import make_file_link
