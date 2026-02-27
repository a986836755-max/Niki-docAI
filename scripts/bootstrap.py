"""
Niki-docAI Remote Bootstrap Script.
Use this script to install Niki-docAI from a remote repository or local source.

Usage:
    python bootstrap.py
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
import urllib.request

REPO_URL = "https://github.com/a986836755-max/Niki-docAI.git"  # Replace with actual repo URL if different

def main():
    print("🚀 Niki-docAI Bootstrapper")
    
    # 1. Check Python
    if sys.version_info < (3, 9):
        print("❌ Error: Python 3.9+ is required.")
        sys.exit(1)
        
    print(f"✅ Python {sys.version.split()[0]} detected.")

    # 2. Install from Git
    print("📦 Installing ndoc core from source...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            f"git+{REPO_URL}"
        ])
    except subprocess.CalledProcessError:
        print("❌ Failed to install package. Please check git availability and network.")
        sys.exit(1)

    # 3. Initialize Environment (Trigger shim creation)
    print("🔗 Configuring environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "ndoc", "--help"], stdout=subprocess.DEVNULL)
    except Exception:
        pass

    print("\n✅ Installation Complete!")
    print("   Run 'ndoc init' in your project root to get started.")

if __name__ == "__main__":
    main()
