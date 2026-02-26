# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: `capabilities.py` implements the "Kernel + Plugins" architecture. Do not hardcode...
# *   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
# *   **Enhanced Symbol Context**: `scanner.py` 在重建缓存符号时必须确保 `path` 属性被正确填充，否则会导致下游 CLI 工具 (如 `lsp` 指令) 在解析相对路径时崩溃。
# *   **LSP Service Hotness**: `lsp.py` 提供轻量级引用计数。该计数基于全局词频统计，虽然不是 100% 精确的定义引用，但在大规模 codebase 中能有效反映符号的“热度”和影响力。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: Text Processing Utilities.
原子能力：文本处理工具。
"""
import re
from typing import List, Optional
from ..models.context import Tag

# Tags: @TAG or !TAG
# Supports attributes: !RULE[CRITICAL]
TAG_REGEX = re.compile(
    r"(?m)^\s*(?:#+|//|<!--|>|\*)\s*([@!][a-zA-Z_]+)(?:\[(.*?)\])?(?:\s+(.*?))?(?:\s*(?:-->))?\s*$"
)

def clean_docstring(raw: str) -> str:
    """
    Clean raw comment text by removing comment markers and trimming.
    """
    if not raw:
        return ""
    
    # Handle Python triple quotes
    if raw.startswith('"""') or raw.startswith("'''"):
        if raw.endswith('"""') and len(raw) >= 6:
            return raw[3:-3].strip()
        if raw.endswith("'''") and len(raw) >= 6:
            return raw[3:-3].strip()
        # Handle cases where quotes might not be perfectly matched or multiline
        # But usually raw string literal from tree-sitter includes quotes.
    
    # Handle block comments
    if raw.startswith('/**'):
        lines = raw[3:-2].split('\n')
        cleaned = [line.strip().lstrip('*').strip() for line in lines]
        return "\n".join(cleaned).strip()
    elif raw.startswith('/*'):
        return raw[2:-2].strip()
    
    # Handle line comments
    lines = []
    for line in raw.split('\n'):
        line = line.strip()
        if line.startswith('///'):
            lines.append(line[3:].strip())
        elif line.startswith('//'):
            lines.append(line[2:].strip())
        elif line.startswith('#'):
            lines.append(line[1:].strip())
        else:
            lines.append(line)
    return "\n".join(lines).strip()

def extract_attributes(attr_str: str) -> dict:
    """
    Parse attribute string like "CONF=0.8, CRITICAL" into dict.
    Returns: {'CONF': '0.8', 'CRITICAL': True}
    """
    if not attr_str:
        return {}
    
    attrs = {}
    parts = [p.strip() for p in attr_str.split(',')]
    for part in parts:
        if '=' in part:
            key, val = part.split('=', 1)
            attrs[key.strip()] = val.strip()
        else:
            if part:
                attrs[part] = True
    return attrs

def extract_tags_from_text(text: str, line_offset: int = 0) -> List[Tag]:
    """
    Extract @TAGS from a block of text.
    Supports attributes via [ATTR] syntax.
    """
    tags = []
    if not text:
        return tags
        
    for match in TAG_REGEX.finditer(text):
        name = match.group(1)
        attr_str = match.group(2)
        args_str = match.group(3)
        raw = match.group(0).strip()
        
        # Calculate relative line number
        rel_line = text.count("\n", 0, match.start())
        
        args = [a.strip() for a in (args_str or "").split() if a.strip()]
        attributes = extract_attributes(attr_str)
        
        tags.append(Tag(
            name=name, 
            args=args, 
            line=line_offset + rel_line, 
            raw=raw,
            attributes=attributes
        ))
    return tags
