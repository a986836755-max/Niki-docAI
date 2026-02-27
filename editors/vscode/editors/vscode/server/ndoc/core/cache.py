"""
Atoms: Cache Management.
原子能力：缓存管理。
"""
import json
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

class FileCache:
    """
    Manages persistent cache for file scan results using SQLite.
    """
    def __init__(self, cache_dir: Path, db_name: str = "ndoc_cache.db"):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = cache_dir / db_name
        self._conn = None
        self._cursor = None
        self._connect()
        self._init_db()

    def _connect(self):
        """Connect to SQLite database."""
        try:
            self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False, timeout=10.0)
            # Use default journal mode to avoid I/O errors on some Windows setups
            self._conn.execute("PRAGMA journal_mode=DELETE")
            self._cursor = self._conn.cursor()
        except sqlite3.OperationalError as e:
            print(f"Cache DB error: {e}, recreating...")
            if self._conn:
                try: self._conn.close()
                except: pass
            if self.db_path.exists():
                try:
                    self.db_path.unlink()
                except Exception:
                    pass
            self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False, timeout=10.0)
            self._cursor = self._conn.cursor()

    def _init_db(self):
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_cache (
                path TEXT PRIMARY KEY,
                hash TEXT,
                data TEXT
            )
        """)
        self._conn.commit()
        
        # Clean up legacy JSON cache if exists
        json_path = self.cache_dir / "scan_cache.json"
        if json_path.exists():
            try:
                json_path.unlink()
            except Exception:
                pass

    def load(self):
        # No-op for SQLite as we query on demand
        pass

    def save(self):
        if self._conn:
            self._conn.commit()
            
    def close(self):
        if self._conn:
            self._conn.close()

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
        try:
            rel_path = str(file_path)
            
            # Use cursor directly
            if not self._cursor:
                self._connect()
                
            self._cursor.execute("SELECT hash FROM file_cache WHERE path = ?", (rel_path,))
            row = self._cursor.fetchone()
            
            if not row:
                return True
                
            cached_hash = row[0]
            # Calculate hash only if record exists
            current_hash = self.get_file_hash(file_path)
            
            return cached_hash != current_hash
        except Exception as e:
            # On any DB error, assume changed to force re-scan
            return True

    def update(self, file_path: Path, result: Any):
        """Update cache for a file."""
        rel_path = str(file_path)
        file_hash = self.get_file_hash(file_path)
        
        # Serialize result to JSON string
        try:
            json_data = json.dumps(result)
        except Exception:
            return

        self._cursor.execute("""
            INSERT OR REPLACE INTO file_cache (path, hash, data)
            VALUES (?, ?, ?)
        """, (rel_path, file_hash, json_data))

    def get(self, file_path: Path) -> Optional[Any]:
        """Get cached result for a file."""
        try:
            rel_path = str(file_path)
            if not self._cursor:
                self._connect()
                
            self._cursor.execute("SELECT data FROM file_cache WHERE path = ?", (rel_path,))
            row = self._cursor.fetchone()
            
            if row:
                try:
                    return json.loads(row[0])
                except Exception:
                    return None
            return None
        except Exception:
            return None
