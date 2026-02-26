import os
import sys
import shutil
from pathlib import Path
from typing import Optional

from .capabilities import CapabilityManager
from .logger import logger

def ensure_cli_environment() -> None:
    CapabilityManager._init_local_lib()
    _ensure_cli_shim()

def _ensure_cli_shim() -> None:
    if shutil.which("ndoc"):
        return
    bin_dir = _get_user_bin_dir()
    bin_dir.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        shim = bin_dir / "ndoc.cmd"
        content = "@echo off\r\npy -m ndoc %*\r\n"
    else:
        shim = bin_dir / "ndoc"
        content = "#!/usr/bin/env sh\npython3 -m ndoc \"$@\"\n"
    _write_if_changed(shim, content)
    if os.name != "nt":
        try:
            shim.chmod(0o755)
        except Exception:
            pass
    _ensure_path(bin_dir)

def _get_user_bin_dir() -> Path:
    return Path.home() / ".ndoc" / "bin"

def _ensure_path(bin_dir: Path) -> None:
    path_value = os.environ.get("PATH", "")
    parts = path_value.split(os.pathsep) if path_value else []
    if str(bin_dir) in parts:
        return
    os.environ["PATH"] = str(bin_dir) + (os.pathsep + path_value if path_value else "")
    _persist_path(bin_dir)

def _persist_path(bin_dir: Path) -> None:
    if _is_stdio_mode():
        return
    if os.name == "nt":
        _persist_path_windows(bin_dir)
    else:
        _persist_path_unix(bin_dir)

def _persist_path_windows(bin_dir: Path) -> None:
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
        try:
            value, regtype = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            value, regtype = "", winreg.REG_EXPAND_SZ
        if str(bin_dir) not in value.split(";") if value else []:
            new_value = value + (";" if value and not value.endswith(";") else "") + str(bin_dir)
            winreg.SetValueEx(key, "Path", 0, regtype, new_value)
        winreg.CloseKey(key)
    except Exception as e:
        logger.warning(f"Failed to persist PATH for ndoc: {e}")

def _persist_path_unix(bin_dir: Path) -> None:
    profile = Path.home() / ".profile"
    line = f'\nexport PATH="$PATH:{bin_dir}"\n'
    content = ""
    if profile.exists():
        try:
            content = profile.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            content = ""
    if str(bin_dir) in content:
        return
    try:
        profile.write_text(content + line, encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to persist PATH for ndoc: {e}")

def _write_if_changed(path: Path, content: str) -> None:
    try:
        if path.exists():
            current = path.read_text(encoding="utf-8", errors="ignore")
            if current == content:
                return
    except Exception:
        pass
    path.write_text(content, encoding="utf-8")

def _is_stdio_mode() -> bool:
    args = " ".join(sys.argv)
    return "--stdio" in args or "server" in args
