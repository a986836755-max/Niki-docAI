"""
Atoms: Hippocampus (Observation Buffer & Heatmap).
原子能力：海马体（观察者缓冲区 & 热力图）。
负责记录短期内的文件活动，并计算标签的活跃度（热度）。
"""

import time
from typing import Dict, List, Tuple, Deque
from dataclasses import dataclass, field
from collections import deque, defaultdict
from enum import Enum
from pathlib import Path

class ActionType(Enum):
    OPEN = 1
    EDIT = 5  # Higher weight
    SAVE = 2
    CLOSE = 0

@dataclass
class Observation:
    file_path: str
    action: ActionType
    timestamp: float = field(default_factory=time.time)

@dataclass
class Hippocampus:
    """
    Short-term memory buffer.
    Stores recent observations and calculates heat.
    """
    buffer: Deque[Observation] = field(default_factory=lambda: deque(maxlen=100))
    # Decay factor: heat *= decay ^ (time_delta / time_unit)
    decay_rate: float = 0.95 # Retain 95% heat per minute
    
    def record(self, file_path: str, action: ActionType):
        """Record a new observation."""
        obs = Observation(str(Path(file_path).resolve()), action)
        self.buffer.append(obs)
        
    def get_file_heat(self, now: float = None) -> Dict[str, float]:
        """
        Calculate heat for each file based on observations.
        Heat = Sum(ActionWeight * Decay)
        """
        if now is None:
            now = time.time()
            
        heat: Dict[str, float] = defaultdict(float)
        
        for obs in self.buffer:
            age_seconds = now - obs.timestamp
            if age_seconds < 0: age_seconds = 0
            
            # Simple linear decay for demo, or exponential
            # Let's use exponential decay: value * (0.5 ^ (age / half_life))
            # Half-life = 1 hour (3600s)
            decay = 0.5 ** (age_seconds / 3600.0)
            
            # Optimization: Skip negligible contributions
            if decay * obs.action.value < 0.1:
                continue
                
            heat[obs.file_path] += obs.action.value * decay
            
        return dict(heat)

    def get_tag_heat(self, file_tags_map: Dict[str, List[str]], now: float = None) -> Dict[str, float]:
        """
        Project file heat to tags.
        file_tags_map: {file_path: [tag_names]}
        """
        file_heat = self.get_file_heat(now)
        tag_heat: Dict[str, float] = defaultdict(float)
        
        for file_path, heat in file_heat.items():
            tags = file_tags_map.get(file_path, [])
            for tag in tags:
                tag_heat[tag] += heat
                
        return dict(tag_heat)
