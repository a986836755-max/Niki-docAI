"""
Flow: Data Registry Generation.
业务流：生成数据注册中心 (_DATA.md)。
汇总展示项目中的 @dataclass, TypedDict 和 Enum。
"""
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

from ..atoms import fs, io, scanner, ast
from ..models.config import ProjectConfig
from ..models.context import Symbol

@dataclass
class DataDefinition:
    name: str
    type: str  # dataclass, enum, typeddict
    path: str
    docstring: str
    fields: List[str]

def run(config: ProjectConfig) -> bool:
    """
    执行 Data Registry Flow.
    """
    root_path = config.scan.root_path
    data_file = root_path / "_DATA.md"
    
    print(f"Generating Data Registry in {root_path}...")
    
    # 1. Collect all relevant source files
    extensions = set(config.scan.extensions) if config.scan.extensions else {'.py', '.cs', '.ts', '.js', '.go', '.rs'}
    ignore = set(config.scan.ignore_patterns) | {'.git', '__pycache__', 'venv', 'tests'}
    source_files = list(fs.walk_files(root_path, ignore_patterns=list(ignore), extensions=extensions))
    
    definitions: List[DataDefinition] = []
    
    for file_path in source_files:
        try:
            rel_path = file_path.relative_to(root_path).as_posix()
            # Use cached scanner
            scan_result = scanner.scan_file(file_path, root_path)
            
            ext = file_path.suffix.lower()
            for sym in scan_result.symbols:
                is_data = False
                data_type = sym.kind
                
                if ext == '.py':
                    if sym.kind == 'class':
                        if any('dataclass' in d for d in sym.decorators):
                            is_data = True
                            data_type = "dataclass"
                        elif any(base in ['Enum', 'IntEnum', 'StrEnum'] for base in sym.bases):
                            is_data = True
                            data_type = "enum"
                        elif 'TypedDict' in sym.bases:
                            is_data = True
                            data_type = "typeddict"
                    elif sym.kind == 'enum': # In case we capture it as enum directly
                        is_data = True
                        data_type = "enum"
                
                elif ext == '.cs':
                    # C# Data structures: struct, enum, record (if kind is record)
                    if sym.kind in ['struct', 'enum', 'record']:
                        is_data = True
                        data_type = sym.kind
                    elif sym.kind == 'class':
                        # Heuristic: if it has no methods but only properties?
                        # Or if it inherits from something?
                        # For now, let's just stick to struct/enum/record for C#
                        pass

                if is_data:
                    # Extract fields from body if possible
                    fields = []
                    lines = sym.full_content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('@') or line.startswith('class') or \
                           line.startswith('def') or line.startswith('"""') or \
                           line.startswith('[') or line.startswith('using') or \
                           line.startswith('namespace') or line.startswith('{') or line.startswith('}'):
                            continue
                        # Python fields (x: int = 1) or C# fields (public int X { get; set; }) or Enum members
                        if ':' in line or '=' in line or '{ get; set; }' in line or ';' in line or (data_type == 'enum' and (',' in line or line.strip())):
                            fields.append(line)
                    
                    definitions.append(DataDefinition(
                        name=sym.name,
                        type=data_type,
                        path=rel_path,
                        docstring=sym.docstring,
                        fields=fields[:10]
                    ))
        except Exception as e:
            print(f"Error scanning {file_path} for data: {e}")

    # 2. Generate Content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Data Registry",
        f"> @CONTEXT: Global | _DATA.md | @TAGS: @DATA @MODELS",
        f"> 最后更新 (Last Updated): {timestamp}",
        "",
        "> **Goal**: 集中展示项目中的核心数据结构 (Dataclasses, Enums, TypedDicts)。强化 \"Logic as Data\" 原则。",
        ""
    ]
    
    # Group by type
    by_type = {}
    for d in definitions:
        if d.type not in by_type:
            by_type[d.type] = []
        by_type[d.type].append(d)
    
    def get_plural(name: str) -> str:
        if name.endswith('ss'): return name + "es"
        if name.endswith('s'): return name
        return name + "s"

    for dtype, items in by_type.items():
        if not items:
            continue
        
        lines.append(f"## {get_plural(dtype.capitalize())}")
        for item in sorted(items, key=lambda x: x.name):
            first_line = item.docstring.split('\n')[0] if item.docstring else ""
            doc = f" - *{first_line}*" if first_line else ""
            lines.append(f"*   **{item.name}** ([{item.path}]({item.path})){doc}")
            if item.fields:
                lines.append("    ```python")
                for f in item.fields:
                    lines.append(f"    {f}")
                lines.append("    ```")
        lines.append("")

    if not definitions:
        lines.append("*No data structures detected yet.*")

    template = "\n".join(lines) + "\n\n---\n*Generated by Niki-docAI*"
    io.write_text(data_file, template)
    print(f"✅ Data Registry updated: {data_file.name}")
    
    return True
