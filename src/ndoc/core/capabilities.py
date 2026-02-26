# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: `capabilities.py` implements the "Kernel + Plugins" architecture. Do not hardcode...
# *   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
# *   **Enhanced Symbol Context**: `scanner.py` 在重建缓存符号时必须确保 `path` 属性被正确填充，否则会导致下游 CLI 工具 (如 `lsp` 指令) 在解析相对路径时崩溃。
# *   **LSP Service Hotness**: `lsp.py` 提供轻量级引用计数。该计数基于全局词频统计，虽然不是 100% 精确的定义引用，但在大规模 codebase 中能有效反映符号的“热度”和影响力。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: Capability Manager.
能力管理：负责按需加载和安装语言解析器等插件。
"""
import importlib
import subprocess
import sys
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
from tree_sitter import Language

class CapabilityManager:
    """
    Manages dynamic capabilities (e.g., tree-sitter languages).
    """
    
    # Mapping: language_name -> pypi_package_name
    # Note: Keys should match what is used in import tree_sitter_{key}
    LANGUAGE_PACKAGES = {
        "python": "tree-sitter-python",
        "javascript": "tree-sitter-javascript",
        "typescript": "tree-sitter-typescript",
        "go": "tree-sitter-go",
        "rust": "tree-sitter-rust",
        "cpp": "tree-sitter-cpp",
        "c_sharp": "tree-sitter-c-sharp",
        "java": "tree-sitter-java",
        "dart": "tree-sitter-dart",
        "json": "tree-sitter-json",
        "flatbuffers": "tree-sitter-flatbuffers",
    }
    
    # Mapping: capability_name -> pypi_package_name
    OPTIONAL_PACKAGES = {
        "chromadb": "chromadb",
    }

    _CACHE: Dict[str, Optional[Language]] = {}
    _FAILED_INSTALLS: set[str] = set() # Circuit breaker for failed installs
    
    # Local Lib Settings (Project Level)
    # We will determine this dynamically based on project root if possible, 
    # but for now we can try to infer it or use a user-local path if not in project.
    # Actually, best is to use .ndoc/lib in the current working directory or capabilities file location?
    # Let's use ~/.ndoc/lib for now as a safe user-writable location that is shared across projects,
    # OR use ./ndoc/lib if we want per-project isolation.
    # Given the user request "downloaded in the project local", we should use CWD/.ndoc/lib.
    
    # However, CWD changes. We should rely on where the code is running or pass root.
    # Since this is a class method, we don't have config instance easily.
    # Let's try to find project root or fallback to ~/.ndoc
    
    _LOCAL_LIB_DIR: Optional[Path] = None
    _TREE_SITTER_BOOTSTRAPPED: bool = False

    @classmethod
    def _get_lib_dir(cls) -> Path:
        if cls._LOCAL_LIB_DIR:
            return cls._LOCAL_LIB_DIR
            
        # [Priority 1] Project-local .ndoc/lib (if .ndoc exists in CWD)
        # This allows per-project dependency isolation.
        cwd_ndoc = Path.cwd() / ".ndoc"
        if cwd_ndoc.exists() and cwd_ndoc.is_dir():
             target_dir = cwd_ndoc / "lib"
             cls._LOCAL_LIB_DIR = target_dir
             return target_dir

        # [Priority 2] User-global .ndoc/lib (Fallback)
        # Use user home directory for stable, project-agnostic dependency storage
        # This avoids issues with CWD changes and "not found" errors.
        target_dir = Path.home() / ".ndoc" / "lib"
        cls._LOCAL_LIB_DIR = target_dir
        return target_dir

    @classmethod
    def _init_local_lib(cls):
        """Ensure local lib dir exists and is in sys.path"""
        lib_dir = cls._get_lib_dir()
        if str(lib_dir) not in sys.path:
            sys.path.insert(0, str(lib_dir)) # High priority

        if cls._TREE_SITTER_BOOTSTRAPPED:
            return
        cls._TREE_SITTER_BOOTSTRAPPED = True
            
        # [Force Upgrade Check & Reload]
        # We need to ensure the local 'tree-sitter' library is up-to-date (0.22+)
        # because the global one might be old (0.21.3) and incompatible with new language bindings.
        # This is critical for C++/Rust support.
        try:
            # Check if tree-sitter is already loaded from a global path
            if 'tree_sitter' in sys.modules:
                ts_mod = sys.modules['tree_sitter']
                if not hasattr(ts_mod, '__file__') or str(lib_dir) not in str(ts_mod.__file__):
                    # print(f"--> [Capability] Detected global tree-sitter ({ts_mod.__file__}). Forcing reload from local lib.")
                    del sys.modules['tree_sitter']
                    # Also clear submodules
                    to_remove = [m for m in sys.modules if m.startswith('tree_sitter.')]
                    for m in to_remove:
                        del sys.modules[m]

            tree_sitter_loaded = False
            try:
                import tree_sitter
                tree_sitter_loaded = True
            except Exception:
                tree_sitter_loaded = False
            # Simple version check heuristic: if Language doesn't accept 1 arg, it's old.
            # But importing might pick up the global one first if we haven't installed local yet.
            
            # We blindly check if tree-sitter exists in local lib.
            local_ts = lib_dir / "tree_sitter"
            if not local_ts.exists():
                # print("--> [Capability] Installing local tree-sitter runtime (isolation mode)...")
                cls.ensure_package("tree-sitter", auto_install=True)
                
                # Reload after install
                if 'tree_sitter' in sys.modules:
                    importlib.reload(sys.modules['tree_sitter'])
                else:
                    import tree_sitter
            elif not tree_sitter_loaded:
                import tree_sitter
        except Exception:
            pass

    # Persistent lock file settings (Use TEMP for reliability)
    _LOCK_FILE_DIR = Path(os.environ.get("TEMP", ".")) / "ndoc_locks"
    _LOCK_TTL_SECONDS = 3600 # 1 hour cooldown

    @classmethod
    def _is_locked(cls, package_name: str) -> bool:
        """Check if package installation is locked due to recent failure."""
        lock_file = cls._LOCK_FILE_DIR / f"{package_name}.lock"
        if lock_file.exists():
            try:
                # Check TTL
                mtime = lock_file.stat().st_mtime
                if time.time() - mtime < cls._LOCK_TTL_SECONDS:
                    return True
                else:
                    # Expired, remove it
                    lock_file.unlink()
            except Exception:
                pass
        return False

    @classmethod
    def _set_lock(cls, package_name: str):
        """Set a persistent lock for package installation failure."""
        try:
            cls._LOCK_FILE_DIR.mkdir(parents=True, exist_ok=True)
            lock_file = cls._LOCK_FILE_DIR / f"{package_name}.lock"
            lock_file.touch()
        except Exception as e:
            print(f"--> Warning: Failed to set install lock: {e}")

    @classmethod
    def ensure_package(cls, package_name: str, auto_install: bool = True) -> bool:
        """
        Ensure a Python package is installed.
        """
        # Ensure local lib is in path before trying import
        cls._init_local_lib()

        if package_name in cls._FAILED_INSTALLS:
            return False
            
        if cls._is_locked(package_name):
            # print(f"--> Skipping {package_name} (Recent failure locked).")
            cls._FAILED_INSTALLS.add(package_name)
            return False

        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            pass
        
        pypi_name = cls.OPTIONAL_PACKAGES.get(package_name, package_name)
        
        # Check non-interactive
        if not auto_install:
            # Silent fail in non-interactive to prevent spam
            # print(f"--> Missing optional package '{pypi_name}'. Install manually.")
            cls._FAILED_INSTALLS.add(package_name)
            return False

        print(f"--> Installing {pypi_name} to {cls._get_lib_dir()}...")
        try:
            lib_dir = cls._get_lib_dir()
            lib_dir.mkdir(parents=True, exist_ok=True)
            
            # Use --target to install to local directory
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                pypi_name, 
                "--target", str(lib_dir),
                "--quiet",
                "--no-user" # Ensure we don't try user install
            ])
            print(f"--> {pypi_name} installed successfully.")
            
            # Invalidate caches to ensure new package is found
            importlib.invalidate_caches()
            
            return True
        except Exception as e:
            print(f"--> Failed to install {pypi_name}: {e}")
            cls._FAILED_INSTALLS.add(package_name)
            cls._set_lock(package_name)
            return False

        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            pass

        # If import failed and auto_install is disabled (which it now is), just fail silently or log once.
        # cls._FAILED_INSTALLS.add(package_name) # Mark as failed so we don't spam logs
        # return False
        
        pypi_name = cls.OPTIONAL_PACKAGES.get(package_name, package_name)
        
        # Check non-interactive
        if not auto_install:
            # Silent fail in non-interactive to prevent spam
            # print(f"--> Missing optional package '{pypi_name}'. Install manually.")
            cls._FAILED_INSTALLS.add(package_name)
            return False

        # ... (Unreachable code below due to auto_install=False override) ...
        print(f"--> Installing {pypi_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pypi_name, "--quiet"])
            print(f"--> {pypi_name} installed successfully.")
            return True
        except Exception as e:
            print(f"--> Failed to install {pypi_name}: {e}")
            cls._FAILED_INSTALLS.add(package_name)
            cls._set_lock(package_name)
            return False

    @classmethod
    def ensure_languages(cls, lang_names: set[str], auto_install: bool = True):
        """
        Batch ensure languages are installed.
        """
        cls._init_local_lib()
        missing = []
        for name in lang_names:
            if name in cls._CACHE and cls._CACHE[name]:
                continue
            
            # Check if importable
            if cls._try_import(name):
                continue
            
            if name == "dart" and sys.platform == "win32":
                if not cls._has_dart_dll():
                    cls._FAILED_INSTALLS.add(name)
                    cls._set_lock(name)
                continue
                
            missing.append(name)
            
        if not missing:
            return

        # Trigger installation
        for lang in missing:
            cls.get_language(lang, auto_install=auto_install)

        print(f"--> [Capability] Auto-detected missing languages: {', '.join(missing)}")
        
        # Install logic
        packages = []
        for name in missing:
            if name == "dart" and sys.platform == "win32":
                continue
            pkg = cls.LANGUAGE_PACKAGES.get(name)
            if pkg:
                packages.append(pkg)
                
        if not packages:
            return

        if auto_install:
             print(f"--> Auto-installing missing components: {', '.join(packages)}...")
             try:
                 lib_dir = cls._get_lib_dir()
                 lib_dir.mkdir(parents=True, exist_ok=True)
                 
                 subprocess.check_call([
                     sys.executable, "-m", "pip", "install"
                 ] + packages + [
                     "--target", str(lib_dir),
                     "--quiet",
                     "--no-user",
                     "--upgrade",
                     "--ignore-installed" # Critical: Ignore global site-packages to avoid permission errors
                 ])
                 print("--> Components installed successfully.")
                 
                 # Invalidate caches
                 importlib.invalidate_caches()
                 
                 # Clear cache to force reload attempt on next access
                 cls._CACHE.clear() 
             except Exception as e:
                 print(f"--> Failed to batch install components: {e}")

    @classmethod
    def get_language(cls, lang_name: str, auto_install: bool = False, check_only: bool = False) -> Optional[Language]:
        """
        Get the tree-sitter Language object for the given language name.
        If not installed, attempts to install it (unless check_only is True).
        """
        # Ensure local lib is in path before trying import
        cls._init_local_lib()
        
        # EMERGENCY FIX: Disable auto-install override (Revert to argument value)
        # auto_install = False # Removed to restore functionality
        
        if lang_name in cls._CACHE:
            return cls._CACHE[lang_name]

        # Circuit breaker
        if lang_name in cls._FAILED_INSTALLS:
            return None
            
        # Check persistent lock
        if cls._is_locked(lang_name):
            # print(f"--> Skipping language {lang_name} (Recent failure locked).")
            cls._FAILED_INSTALLS.add(lang_name)
            return None

        package_name = cls.LANGUAGE_PACKAGES.get(lang_name)
        if not package_name:
            # Fallback for languages not in our map (or maybe already installed but we don't know the package name)
            # Try direct import just in case
            return cls._try_import(lang_name)

        # 1. Try to import
        lang = cls._try_import(lang_name)
        if lang:
            cls._CACHE[lang_name] = lang
            return lang

        if check_only:
            return None

        if lang_name == "dart" and sys.platform == "win32":
            if cls._has_dart_dll():
                lang = cls._try_import(lang_name)
                cls._CACHE[lang_name] = lang
                return lang
            cls._FAILED_INSTALLS.add(lang_name)
            cls._set_lock(lang_name)
            return None

        # 2. Install if missing
        # TODO: Use a proper logger
        # print(f"--> [Capability] Detected need for '{lang_name}' support.")
        
        if not auto_install:
            # Silent fail
            cls._FAILED_INSTALLS.add(lang_name)
            return None

        if auto_install:
            print(f"--> Installing {package_name}...")
            try:
                lib_dir = cls._get_lib_dir()
                lib_dir.mkdir(parents=True, exist_ok=True)
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package_name,
                    "--target", str(lib_dir),
                    "--quiet",
                    "--no-user",
                    "--upgrade",
                    "--ignore-installed"
                ])
                print(f"--> {package_name} installed successfully.")
                importlib.invalidate_caches()
                
                # Retry import
                lang = cls._try_import(lang_name)
                if lang:
                    cls._CACHE[lang_name] = lang
                    return lang
                else:
                    print(f"--> Failed to load {lang_name} even after installation.")
                    cls._FAILED_INSTALLS.add(lang_name)
                    cls._set_lock(lang_name)
            except subprocess.CalledProcessError as e:
                print(f"--> Failed to install {package_name}: {e}")
                cls._FAILED_INSTALLS.add(lang_name)
                cls._set_lock(lang_name)
            except Exception as e:
                print(f"--> Error during installation/loading of {lang_name}: {e}")
                cls._FAILED_INSTALLS.add(lang_name)
                cls._set_lock(lang_name)

        cls._CACHE[lang_name] = None
        return None

    @staticmethod
    def _try_import(lang_name: str) -> Optional[Language]:
        CapabilityManager._init_local_lib()
        from tree_sitter import Language as TS_Language
        # 0. Try loading custom DLL first (e.g. for Dart)
        if lang_name == 'dart':
            try:
                from pathlib import Path
                # Assuming dll is in ../parsing/langs/bin/ relative to this file?
                # This file is src/ndoc/core/capabilities.py
                # Bin is src/ndoc/parsing/langs/bin/
                # So we go up 2 levels -> parsing -> langs -> bin
                import ndoc.parsing.langs as langs_pkg
                bin_dir = Path(langs_pkg.__file__).parent / "bin"
                dll_path = bin_dir / "tree_sitter_dart.dll"
                
                if dll_path.exists():
                    try:
                        if hasattr(TS_Language, "load"):
                            return TS_Language.load(str(dll_path))
                    except Exception:
                        pass
                    try:
                        return TS_Language(str(dll_path), 'dart')
                    except Exception:
                        return None
            except Exception as e:
                print(f"--> Warning: Failed to load custom Dart DLL: {e}")

        try:
            # Dynamic import: import tree_sitter_{lang_name}
            module_name = f"tree_sitter_{lang_name}"
            module = importlib.import_module(module_name)
            
            # Helper to safely create Language
            def make_language(ptr):
                if isinstance(ptr, TS_Language):
                    return ptr
                if hasattr(ptr, "__class__") and ptr.__class__.__name__ == "Language":
                    return ptr
                if not ptr:
                    return None
                try:
                    return TS_Language(ptr, lang_name)
                except Exception:
                    try:
                        return TS_Language(ptr)
                    except Exception:
                        return None

            # Special handling for typescript (it has language_typescript and language_tsx)
            if lang_name == 'typescript':
                if hasattr(module, 'language_typescript'):
                    return make_language(module.language_typescript())
            
            # Most bindings expose a language() function
            if hasattr(module, 'language'):
                return make_language(module.language())
            else:
                # Debug info only if import succeeded but function missing
                print(f"--> Module {module_name} does not have 'language()' function.")
                return None
        except ImportError:
            return None
        except Exception as e:
            # Print error to help diagnosis
            print(f"--> Error loading {lang_name}: {e}")
            return None

    @staticmethod
    def _has_dart_dll() -> bool:
        try:
            import ndoc.parsing.langs as langs_pkg
            bin_dir = Path(langs_pkg.__file__).parent / "bin"
            return (bin_dir / "tree_sitter_dart.dll").exists()
        except Exception:
            return False
