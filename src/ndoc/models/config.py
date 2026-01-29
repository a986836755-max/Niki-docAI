"""
Models: Configuration definitions.
数据模型：配置定义。
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

@dataclass
class ScanConfig:
    """
    扫描配置 (Configuration for file scanning).
    """
    root_path: Path
    # 默认忽略的目录/文件 (Default patterns to ignore)
    ignore_patterns: List[str] = field(default_factory=lambda: [
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".idea",
        ".vscode",
        "dist",
        "build",
        "ndoc_legacy" # Explicitly ignore legacy
    ])
    # 允许的文件扩展名 (Allowed extensions), Empty means all
    extensions: List[str] = field(default_factory=list)

@dataclass
class ProjectConfig:
    """
    项目全局配置 (Global Project Configuration).
    """
    scan: ScanConfig
    # 项目名称 (Project Name)
    name: str = "Project"
    # 版本 (Version)
    version: str = "0.1.0"
