"""
Language Statistics.
"""
from pathlib import Path
from typing import Dict, Set
from ...core import fs
from ..langs import get_lang_id_by_ext

def detect_languages(root: Path, ignore_patterns: Set[str]) -> Dict[str, float]:
    """
    Detect languages in the project and return percentage.
    """
    counts = {}
    total = 0
    
    # fs.walk_files yields Path objects
    for f in fs.walk_files(root, ignore_patterns):
        # get_lang_id_by_ext returns lang_id if supported
        lang = get_lang_id_by_ext(f.suffix.lower())
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
            total += 1
            
    if total == 0:
        return {}
        
    # Calculate percentage
    stats = {lang: round((count / total) * 100, 1) for lang, count in counts.items()}
    # Sort by percentage descending
    return dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))
