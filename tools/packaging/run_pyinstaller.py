import sys
from pathlib import Path

pkg_dir = Path(__file__).resolve().parents[2] / ".ndoc" / "packaging_lib"
sys.path.insert(0, str(pkg_dir))

from PyInstaller.__main__ import run

if __name__ == "__main__":
    run(sys.argv[1:])
