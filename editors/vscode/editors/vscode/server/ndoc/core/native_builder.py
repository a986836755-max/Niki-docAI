"""
Native Builder: Handles local compilation of language bindings on Windows.
原生构建器：处理 Windows 环境下的语言绑定本地编译。
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional

from .logger import logger

def find_vcvars64() -> Optional[str]:
    """
    Locate vcvars64.bat using vswhere or standard paths.
    """
    # 1. Try vswhere
    vswhere = Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Microsoft Visual Studio/Installer/vswhere.exe"
    if vswhere.exists():
        try:
            output = subprocess.check_output([
                str(vswhere), 
                "-latest", 
                "-products", "*", 
                "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", 
                "-property", "installationPath"
            ], encoding="utf-8").strip()
            
            if output:
                vcvars = Path(output) / "VC/Auxiliary/Build/vcvars64.bat"
                if vcvars.exists():
                    return str(vcvars)
        except Exception as e:
            logger.warning(f"vswhere failed: {e}")

    # 2. Standard Paths (Fallback)
    years = ["2022", "2019", "2017"]
    editions = ["Enterprise", "Professional", "Community", "BuildTools"]
    root = Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Microsoft Visual Studio"
    
    for year in years:
        for edition in editions:
            bat = root / year / edition / "VC/Auxiliary/Build/vcvars64.bat"
            if bat.exists():
                return str(bat)

    return None

def ensure_dart_source(work_dir: Path) -> bool:
    """
    Ensure tree-sitter-dart source is available in work_dir.
    """
    target_dir = work_dir / "tree-sitter-dart"
    if target_dir.exists():
        # Quick check if it looks valid
        if (target_dir / "src/parser.c").exists():
            return True
        # Invalid, remove and re-clone
        try:
            shutil.rmtree(target_dir)
        except OSError:
            pass

    # Fallback: Check for local copy in project root (Development mode)
    # E:\work\appcodes\nk_doc_ai\src\ndoc\core\native_builder.py -> ../../../temp_build_dart
    # The current path is __file__. So parent(core) -> parent(ndoc) -> parent(src) -> parent(root) -> temp_build_dart
    local_dev_source = Path(__file__).resolve().parent.parent.parent.parent / "temp_build_dart" / "tree-sitter-dart"
    if local_dev_source.exists():
        logger.info(f"Using local development source from {local_dev_source}")
        try:
            # Clean target first to ensure fresh copy
            if target_dir.exists():
                shutil.rmtree(target_dir, ignore_errors=True)
                
            shutil.copytree(local_dev_source, target_dir)
            return True
        except Exception as e:
            logger.warning(f"Failed to copy local source: {e}")

    logger.info("Cloning tree-sitter-dart source...")
    try:
        # Try official repo first
        repo_url = "https://github.com/tree-sitter/tree-sitter-dart.git"
        subprocess.check_call(
            ["git", "clone", repo_url, str(target_dir), "--depth", "1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except Exception as e:
        logger.error(f"Failed to clone tree-sitter-dart: {e}")
        return False

def build_dart_dll(output_path: Path) -> bool:
    """
    Build tree_sitter_dart.dll and place it at output_path.
    """
    if sys.platform != "win32":
        return False

    vcvars = find_vcvars64()
    if not vcvars:
        logger.error("Visual Studio C++ compiler (vcvars64.bat) not found.")
        return False

    work_dir = Path(os.environ.get("TEMP", ".")) / "ndoc_build_dart"
    work_dir.mkdir(parents=True, exist_ok=True)
    
    if not ensure_dart_source(work_dir):
        return False

    src_dir = work_dir / "tree-sitter-dart"
    
    # Build Command
    # We need to run vcvars64.bat then cl
    # cl /LD src/parser.c src/scanner.c /I src /Fe:tree_sitter_dart.dll
    
    build_cmd = f'"{vcvars}" && cd /d "{src_dir}" && cl /nologo /LD src/parser.c src/scanner.c /I src /Fe:tree_sitter_dart.dll'
    
    logger.info(f"Compiling tree-sitter-dart using {vcvars}...")
    try:
        subprocess.check_call(build_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        logger.error("Compilation failed.")
        return False

    # Move DLL
    built_dll = src_dir / "tree_sitter_dart.dll"
    if built_dll.exists():
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built_dll, output_path)
        logger.info(f"Successfully compiled and installed: {output_path}")
        # Cleanup
        # try:
        #     shutil.rmtree(work_dir)
        # except:
        #     pass
        return True
    
    return False
