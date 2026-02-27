"""
Data Schema Plugin (Action).
Generates _DATA.md (Data Registry) from ECS data.
Ported from data_flow.
"""
from pathlib import Path
from typing import Dict, Any, List
from ndoc.sdk.interfaces import ActionPlugin
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType
from ndoc.core.templates import render_document
from datetime import datetime
from ndoc.parsing import scanner

class DataSchemaPlugin(ActionPlugin):
    """
    Action plugin to generate _DATA.md.
    """
    
    def ndoc_generate_docs(self, context: KernelContext):
        print("[DataSchema] Generating _DATA.md...")
        
        # 1. Scan for Data Classes / TypedDicts / Enums
        # Similar to AdrReport, we rely on scanner for now (migration strategy)
        
        definitions = []
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        
        print(f"[DataSchema] Scanning {len(files)} files for data definitions...")
        
        for f in files:
            path = f.path
            if not path.exists(): continue
            
            try:
                # Use scanner to get symbols
                # We need root path for relative paths in scanner calls?
                # Usually scanner takes (file_path, root_path)
                # Let's guess root
                root = Path.cwd()
                
                result = scanner.scan_file(path, root)
                if not result or not result.symbols: continue
                
                ext = path.suffix.lower()
                
                for sym in result.symbols:
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
                        elif sym.kind == 'enum': 
                            is_data = True
                            data_type = "enum"
                    
                    # Add more language support here (TS, Go, etc.)
                    # For Pilot, stick to Python mainly
                    
                    if is_data:
                        definitions.append({
                            "name": sym.name,
                            "type": data_type,
                            "path": f.id,
                            "line": sym.line,
                            "docstring": sym.docstring or "",
                            "fields": [] # Scanner might not extract fields yet
                        })
            except Exception:
                pass
                
        if not definitions:
            print("[DataSchema] No data definitions found.")
            return

        # 2. Render
        # Group by type? Or just list?
        # Let's group by file
        from collections import defaultdict
        grouped = defaultdict(list)
        for d in definitions:
            grouped[d['path']].append(d)
            
        lines = []
        for file_path in sorted(grouped.keys()):
            lines.append(f"## 📄 {file_path}")
            for d in grouped[file_path]:
                icon = "📦" if d['type'] == 'dataclass' else "🔢" if d['type'] == 'enum' else "📝"
                lines.append(f"### {icon} {d['name']} `({d['type']})`")
                if d['docstring']:
                    lines.append(f"> {d['docstring'].strip()}")
                lines.append("")
                # Fields would go here
            lines.append("---")
            
        content = "\n".join(lines)
        
        doc = render_document(
            "data.md.tpl",
            title="Data Registry",
            context="Data Models | Schema",
            tags="@DATA",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content=content,
            definitions_count=len(definitions)
        )
        
        # 3. Write
        try:
            root = Path.cwd()
        except Exception:
            root = Path(files[0].path).parent
            
        output_path = root / "_DATA.md"
        output_path.write_text(doc, encoding="utf-8")
        print(f"[DataSchema] Written to: {output_path}")
