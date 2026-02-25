"""
Core: Infrastructure Utilities.
核心层：基础设施工具。
"""
from .fs import FileFilter, walk_files, should_ignore
from .io import read_text, write_text, safe_io
from .capabilities import CapabilityManager
from .text_utils import clean_docstring, extract_tags_from_text
