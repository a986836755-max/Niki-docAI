import sys
import shutil
import subprocess
from . import console

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
