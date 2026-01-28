import sys
import subprocess
import shutil
from pathlib import Path
from . import console

def get_project_root():
    """Returns the current working directory as the project root."""
    # When installed as a package, we assume niki is run from the project root.
    return Path.cwd()

def run_command(cmd, cwd=None, shell=True, env=None, fail_exit=True):
    """Executes a shell command."""
    console.cmd(cmd)
    try:
        subprocess.check_call(cmd, cwd=cwd, shell=shell, env=env)
    except subprocess.CalledProcessError as e:
        console.error(f"Command failed: {e}")
        if fail_exit:
            sys.exit(1)
        else:
            raise e

def find_flatc():
    """Finds the flatc executable."""
    flatc = shutil.which("flatc")
    if flatc:
        return flatc
    # Windows fallback check or additional paths could be added here
    return None

def ensure_directory(path):
    """Ensures a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)
