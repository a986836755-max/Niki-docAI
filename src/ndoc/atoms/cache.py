"""
Atoms: Cache Management.
原子能力：缓存管理。
"""
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

class FileCache:
    """
    Manages persistent cache for file scan results.
    """
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_file = cache_dir / "scan_cache.json"
        self.data: Dict[str, Dict[str, Any]] = {}
        self.load()

    def load(self):
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def save(self):
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        if not file_path.exists():
            return ""
        try:
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except Exception:
            return ""

    def is_changed(self, file_path: Path) -> bool:
        """Check if file content has changed compared to cache."""
        rel_path = str(file_path)
        if rel_path not in self.data:
            return True
        
        current_hash = self.get_file_hash(file_path)
        return self.data[rel_path].get('hash') != current_hash

    def update(self, file_path: Path, result: Any):
        """Update cache for a file."""
        rel_path = str(file_path)
        self.data[rel_path] = {
            'hash': self.get_file_hash(file_path),
            'result': result
        }

    def get(self, file_path: Path) -> Optional[Any]:
        """Get cached result for a file."""
        rel_path = str(file_path)
        return self.data.get(rel_path, {}).get('result')
