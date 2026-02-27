"""
Architecture Report Plugin (Action).
Generates _ARCH.md (Architecture Overview) from ECS data.
Combines File Tree (from FileEntities) and Tech Stack (from Meta/Files).
"""
from pathlib import Path
from typing import Dict, Any, List
from ndoc.sdk.interfaces import ActionPlugin
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType
from ndoc.core.templates import render_document
from datetime import datetime
from ndoc.core import fs
from ndoc.parsing import deps

class ArchitectureReportPlugin(ActionPlugin):
    """
    Action plugin to generate _ARCH.md.
    """
    
    def ndoc_generate_docs(self, context: KernelContext):
        print("[ArchitectureReport] Generating _ARCH.md...")
        
        # 1. Build File Tree Structure
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        if not files:
            print("[ArchitectureReport] No files found.")
            return

        # Determine root
        root = context.root_path if hasattr(context, 'root_path') else Path.cwd()
        
        # 2. Identify Tech Stack
        tech_stack = set()
        extensions = set(f.path.suffix.lower() for f in files)
        
        # Simple mapping
        ext_map = {
            '.py': 'Python',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript (React)',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript (React)',
            '.rs': 'Rust',
            '.go': 'Go',
            '.java': 'Java',
            '.cs': 'C#',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.dart': 'Dart',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.toml': 'TOML',
            '.xml': 'XML',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'Sass',
            '.sh': 'Shell',
            '.bat': 'Batch',
            '.ps1': 'PowerShell'
        }
        
        for ext, lang in ext_map.items():
            if ext in extensions:
                tech_stack.add(lang)
        
        tech_content = ", ".join(sorted(tech_stack))
        
        # 3. BOM (Bill of Materials) Generation
        # We need to scan files for manifests
        bom_lines = []
        
        # Use existing parsing logic from deps.core
        # But we need to find the specific files in our entity list
        
        # Python
        req_files = [f for f in files if f.path.name == "requirements.txt"]
        py_deps = []
        for f in req_files:
            py_deps.extend(deps.core.parse_requirements_txt(f.path))
            
        pyproject_files = [f for f in files if f.path.name == "pyproject.toml"]
        for f in pyproject_files:
            py_deps.extend(deps.core.parse_pyproject_toml(f.path))
            
        if py_deps:
            bom_lines.append("### 🐍 Python (Pip)")
            for dep in sorted(list(set(py_deps))):
                bom_lines.append(f"*   `{dep}`")
            bom_lines.append("")
            
        # Node.js
        pkg_files = [f for f in files if f.path.name == "package.json"]
        js_deps = []
        for f in pkg_files:
            js_deps.extend(deps.core.parse_package_json(f.path))
            
        if js_deps:
            bom_lines.append("### 📦 Node.js (NPM)")
            for dep in sorted(list(set(js_deps))):
                bom_lines.append(f"*   `{dep}`")
            bom_lines.append("")
            
        # Dart
        pub_files = [f for f in files if f.path.name == "pubspec.yaml"]
        dart_deps = []
        for f in pub_files:
            dart_deps.extend(deps.core.parse_pubspec_yaml(f.path))
            
        if dart_deps:
            bom_lines.append("### 🎯 Dart (Pub)")
            for dep in sorted(list(set(dart_deps))):
                bom_lines.append(f"*   `{dep}`")
            bom_lines.append("")
            
        # C#
        cs_files = [f for f in files if f.path.suffix.lower() == ".csproj"]
        cs_deps = []
        for f in cs_files:
            cs_deps.extend(deps.core.parse_csproj(f.path))
            
        if cs_deps:
            bom_lines.append("### 🔷 C# (NuGet)")
            for dep in sorted(list(set(cs_deps))):
                bom_lines.append(f"*   `{dep}`")
            bom_lines.append("")
            
        # Go
        go_files = [f for f in files if f.path.name == "go.mod"]
        go_deps = []
        for f in go_files:
            go_deps.extend(deps.core.parse_go_mod(f.path))
            
        if go_deps:
            bom_lines.append("### 🐹 Go (Go Modules)")
            for dep in sorted(list(set(go_deps))):
                bom_lines.append(f"*   `{dep}`")
            bom_lines.append("")
            
        # Rust
        cargo_files = [f for f in files if f.path.name == "Cargo.toml"]
        rust_deps = []
        for f in cargo_files:
            rust_deps.extend(deps.core.parse_cargo_toml(f.path))
            
        if rust_deps:
            bom_lines.append("### 🦀 Rust (Cargo)")
            for dep in sorted(list(set(rust_deps))):
                bom_lines.append(f"*   `{dep}`")
            bom_lines.append("")
            
        if not bom_lines:
            bom_lines.append("*   *(No third-party dependencies detected)*")
            
        bom_content = "\n".join(bom_lines)
        
        # 4. Render
        # We need to render the tree content? 
        # The template might need it, but let's check what arch.md.tpl expects.
        # It seems arch.md.tpl is designed for high-level overview.
        # We'll skip tree_content here as _MAP.md covers it.
        
        doc = render_document(
            "arch.md.tpl",
            title="Architecture Overview",
            context="System Design",
            tags="@ARCH",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tech_content=f"**Languages**: {tech_content}",
            bom_content=bom_content
        )
        
        output_path = root / "_ARCH.md"
        try:
            output_path.write_text(doc, encoding="utf-8")
            print(f"[ArchitectureReport] Written to: {output_path}")
        except Exception as e:
            print(f"[ArchitectureReport] Failed to write {output_path}: {e}")
