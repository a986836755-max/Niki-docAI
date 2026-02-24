"""
Atoms: Capability Manager.
能力管理：负责按需加载和安装语言解析器等插件。
"""
import importlib
import subprocess
import sys
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
    }

    _CACHE: Dict[str, Optional[Language]] = {}

    @classmethod
    def ensure_languages(cls, lang_names: set[str], auto_install: bool = True):
        """
        Batch ensure languages are installed.
        """
        missing = []
        for name in lang_names:
            if name in cls._CACHE and cls._CACHE[name]:
                continue
            
            # Check if importable
            if cls._try_import(name):
                continue
                
            missing.append(name)
            
        if not missing:
            return

        print(f"--> [Capability] Auto-detected missing languages: {', '.join(missing)}")
        
        # Install logic
        packages = []
        for name in missing:
            pkg = cls.LANGUAGE_PACKAGES.get(name)
            if pkg:
                packages.append(pkg)
                
        if not packages:
            return

        if auto_install:
             print(f"--> Auto-installing missing components: {', '.join(packages)}...")
             try:
                 subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages + ["--quiet"])
                 print("--> Components installed successfully.")
                 # Clear cache to force reload attempt on next access
                 cls._CACHE.clear() 
             except Exception as e:
                 print(f"--> Failed to batch install components: {e}")

    @classmethod
    def get_language(cls, lang_name: str, auto_install: bool = False) -> Optional[Language]:
        """
        Get the tree-sitter Language object for the given language name.
        If not installed, attempts to install it.
        """
        if lang_name in cls._CACHE:
            return cls._CACHE[lang_name]

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

        # 2. Install if missing
        # TODO: Use a proper logger
        print(f"--> [Capability] Detected need for '{lang_name}' support.")
        
        if not auto_install:
            # Simple interactive check. 
            # In a real daemon mode, this might block or need a different strategy.
            # For now, we assume CLI usage.
            try:
                response = input(f"--> Install {package_name} now? [Y/n] ").strip().lower()
                if response not in ('', 'y', 'yes'):
                    print(f"--> Skipping {lang_name} support.")
                    cls._CACHE[lang_name] = None
                    return None
            except EOFError:
                # Non-interactive environment
                print(f"--> Non-interactive mode detected. Skipping auto-install of {package_name}.")
                cls._CACHE[lang_name] = None
                return None

        print(f"--> Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--quiet"])
            print(f"--> {package_name} installed successfully.")
            
            # Retry import
            lang = cls._try_import(lang_name)
            if lang:
                cls._CACHE[lang_name] = lang
                return lang
            else:
                print(f"--> Failed to load {lang_name} even after installation.")
        except subprocess.CalledProcessError as e:
            print(f"--> Failed to install {package_name}: {e}")
        except Exception as e:
            print(f"--> Error during installation/loading of {lang_name}: {e}")

        cls._CACHE[lang_name] = None
        return None

    @staticmethod
    def _try_import(lang_name: str) -> Optional[Language]:
        try:
            # Dynamic import: import tree_sitter_{lang_name}
            module_name = f"tree_sitter_{lang_name}"
            module = importlib.import_module(module_name)
            
            # Special handling for typescript (it has language_typescript and language_tsx)
            if lang_name == 'typescript':
                if hasattr(module, 'language_typescript'):
                    return Language(module.language_typescript())
            
            # Most bindings expose a language() function
            if hasattr(module, 'language'):
                return Language(module.language())
            else:
                # Debug info only if import succeeded but function missing
                print(f"--> Module {module_name} does not have 'language()' function.")
                return None
        except ImportError:
            return None
        except Exception as e:
            # print(f"--> Error importing {lang_name}: {e}")
            return None
