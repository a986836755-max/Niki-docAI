"""
Atoms: Language Statistics.
语言占比统计逻辑。
"""
from pathlib import Path
from typing import Dict, Set, Counter
from .. import fs

DEFAULT_IGNORE_PATTERNS = {
    '.git', '.vscode', '.idea', '__pycache__', 
    'node_modules', 'venv', 'env', '.env', 
    'dist', 'build', 'target', 'out', 
    '.dart_tool', '.pub-cache', 
    'coverage', 'tmp', 'temp'
}

LANGUAGE_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React',
    '.tsx': 'React TS',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'Sass',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.sh': 'Shell',
    '.bat': 'Batch',
    '.ps1': 'PowerShell',
    '.rs': 'Rust',
    '.go': 'Go',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'C/C++ Header',
    '.hpp': 'C++ Header',
    '.dart': 'Dart',
    '.cmake': 'CMake',
    '.cs': 'C#',
    '.csproj': 'C# Project',
}

def detect_languages(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]:
    stats = Counter()
    total_files = 0
    ignores = list(ignore_patterns or DEFAULT_IGNORE_PATTERNS)
    
    for path in fs.walk_files(root_path, ignore_patterns=ignores):
        ext = path.suffix.lower()
        if ext in LANGUAGE_EXTENSIONS:
            lang = LANGUAGE_EXTENSIONS[ext]
            stats[lang] += 1
            total_files += 1
    
    if total_files == 0:
        return {}
        
    return {lang: round((count / total_files) * 100, 1) for lang, count in stats.most_common()}
