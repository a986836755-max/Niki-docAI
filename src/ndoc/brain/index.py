"""
Atoms: Semantic Index (Thalamus).
原子能力：语义索引（丘脑）。
负责构建倒排索引和计算语义距离。
"""

from typing import Dict, List, Tuple, Set
from pathlib import Path
from dataclasses import dataclass, field
from ..models.symbol import Tag
from ..models.context import FileContext

@dataclass
class IndexEntry:
    tag: Tag
    source_file: str
    weight: int = 1

@dataclass
class SemanticIndex:
    # Rule ID -> Entry
    rules: Dict[str, List[IndexEntry]] = field(default_factory=dict)
    # Keyword -> Rule IDs
    keywords: Dict[str, Set[str]] = field(default_factory=dict)
    
    def save(self, path: Path):
        """Persist index to disk."""
        data = {
            "rules": {k: [vars(e) for e in v] for k, v in self.rules.items()},
            "keywords": {k: list(v) for k, v in self.keywords.items()}
        }
        # Handle nested dataclasses serialization
        for k, entries in data["rules"].items():
            for e in entries:
                if isinstance(e.get('tag'), Tag):
                    e['tag'] = vars(e['tag'])
                    
        import json
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'SemanticIndex':
        """Load index from disk."""
        if not path.exists():
            return cls()
            
        import json
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            index = cls()
            
            # Reconstruct rules
            for k, entries in data.get("rules", {}).items():
                index.rules[k] = []
                for e_dict in entries:
                    # Reconstruct Tag
                    tag_data = e_dict.get('tag')
                    if tag_data:
                        tag = Tag(**tag_data)
                        e_dict['tag'] = tag
                    index.rules[k].append(IndexEntry(**e_dict))
            
            # Reconstruct keywords
            index.keywords = {k: set(v) for k, v in data.get("keywords", {}).items()}
            
            return index
        except Exception as e:
            # print(f"⚠️ Failed to load index: {e}")
            return cls()

def build_index(files: List[FileContext]) -> SemanticIndex:
    """
    Build semantic index from scanned files.
    """
    index = SemanticIndex()
    
    for file in files:
        for tag in file.tags:
            # Index !RULE and @ADR
            if tag.name in ["!RULE", "@ADR"]:
                # Generate a simple ID if not present (using content hash or index)
                # For now, we use the tag content as key if no ID provided
                key = " ".join(tag.args)
                if not key:
                    continue
                
                entry = IndexEntry(
                    tag=tag,
                    source_file=str(file.path),
                    weight=2 if "CRITICAL" in tag.attributes else 1
                )
                
                if key not in index.rules:
                    index.rules[key] = []
                index.rules[key].append(entry)
                
                # Index keywords
                for word in key.lower().split():
                    if len(word) > 3:
                        if word not in index.keywords:
                            index.keywords[word] = set()
                        index.keywords[word].add(key)
                        
    return index

import os

def calculate_distance(source_path: str, target_path: str) -> int:
    """
    Calculate semantic distance between two file paths.
    0 = Same file
    1 = Same directory
    2 = Parent directory
    N = Directory distance
    """
    try:
        src = Path(source_path).resolve()
        tgt = Path(target_path).resolve()
        
        if src == tgt:
            return 0
        
        # Check common parent
        common = Path(os.path.commonpath([src, tgt]))
        
        # Distance = (depth of src - depth of common) + (depth of tgt - depth of common)
        # But we want hierarchical distance.
        # If target is in a parent directory of source, distance is small.
        # If target is in a sibling directory, distance is medium.
        
        src_parts = src.parts
        tgt_parts = tgt.parts
        
        # Calculate divergence point
        i = 0
        while i < len(src_parts) and i < len(tgt_parts) and src_parts[i] == tgt_parts[i]:
            i += 1
            
        # Distance logic:
        # If divergence is at the end of both (should be handled by src==tgt but resolve might differ)
        if i == len(src_parts) and i == len(tgt_parts):
            return 0
            
        # Common path length in parts is 'i'
        
        # steps_up: Levels to go UP from source to reach common ancestor
        # For a file, src_parts includes the filename.
        # e.g. src/main.py -> src (1 step up)
        # But wait, os.path.commonpath behaves differently on files vs dirs?
        # Path.parts includes filename.
        
        # If we are comparing two files in same dir:
        # src: /a/b/c.py, tgt: /a/b/d.py
        # common: /a/b
        # i will be index of 'c.py' and 'd.py' (len-1)
        # i = len(parts)-1
        
        steps_up = len(src_parts) - i 
        steps_down = len(tgt_parts) - i
        
        return steps_up + steps_down
        
    except ValueError:
        return 999 # Different drives or no common path
