"""
Parsing: Code Analysis & Extraction.
感知层：代码解析与提取。
"""
from .ast import parse_code, extract_symbols
from .scanner import scan_file, ScanResult
from .deps import extract_dependencies
from .langs import get_lang_def
