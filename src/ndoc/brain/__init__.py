"""
Brain: Intelligence Layer.
智能层：状态、索引、记忆与推理。
"""
from .cache import FileCache
from .index import SemanticIndex, build_index, calculate_distance
from .checker import check_file, check_all, Violation
from .hippocampus import Hippocampus, ActionType
from .llm import LLMClient
