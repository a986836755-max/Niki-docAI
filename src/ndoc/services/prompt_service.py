"""
Prompt Service (Kernel-as-a-Service).
Generates AI Context Prompts using ECS Kernel data.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType

class PromptService:
    def __init__(self, context: KernelContext, root_path: Path):
        self.context = context
        self.root_path = root_path

    def generate_prompt(self, target_path: Path, focus: bool = False) -> str:
        """
        Generates a context prompt for the given file.
        """
        # This service needs to aggregate information from various sources:
        # 1. File Content (from disk)
        # 2. Global Rules (from _RULES.md or Kernel)
        # 3. Domain Context (from nearest _AI.md)
        # 4. Related APIs (from Dependency Graph)
        # 5. Semantic Context (from VectorDB)
        
        # In legacy flow, this was done by helper modules in `ndoc.parsing`.
        # We should try to use Kernel data where possible, but fall back to helpers if needed.
        
        # 1. Target Code
        target_code = ""
        if target_path.exists():
            from ndoc.core import io
            target_code = io.read_text(target_path)
        else:
            return f"Error: File not found: {target_path}"

        # 2. Global Rules
        # Can we get this from Kernel? 
        # The ConfigFlow loads _RULES.md into ProjectConfig, but Kernel might not have it explicitly unless passed.
        # Let's use the legacy helper for now as it parses the markdown.
        from ndoc.parsing import rules as parsing_rules
        global_rules = parsing_rules.extract_global_rules(self.root_path)
        
        # 3. Syntax Summary
        syntax_summary = parsing_rules.extract_syntax_summary(self.root_path)
        
        # 4. Domain Context
        domain_context = parsing_rules.extract_domain_context(target_path, self.root_path)
        
        # 5. Related APIs (Imports)
        # Use Kernel Dependency Graph!
        # Find entity for target_path
        # We need relative path ID
        try:
            rel_path = str(target_path.relative_to(self.root_path))
        except ValueError:
            rel_path = str(target_path) # Should not happen if within root
            
        related_apis = ""
        # Look up in graph
        if hasattr(self.context, 'graph'):
            # Dependencies of this file
            deps = self.context.graph.get(rel_path, [])
            if deps:
                related_apis = "\n".join([f"- {d}" for d in deps])
        else:
            # Fallback to legacy extractor if graph not ready
            from ndoc.parsing.deps import api_extractor
            # We need config object? api_extractor takes config.
            # But we only have root_path.
            # Let's skip legacy fallback for now and assume Kernel works or return empty.
            pass

        # 6. Semantic Context (VectorDB)
        semantic_context = ""
        if focus:
            from ndoc.brain.vectordb import VectorDB
            db = VectorDB(self.root_path)
            if db.collection:
                query = target_code[:500]
                results = db.search(query, n_results=5)
                if results:
                    snippets = ["## Related Context (Semantic Search)"]
                    for res in results:
                        path = res.get('id', 'unknown')
                        content = res.get('document', '')
                        preview = content[:300].replace('\n', ' ') + "..."
                        snippets.append(f"### {path}\n```\n{preview}\n```")
                    semantic_context = "\n".join(snippets)

        # Render Template
        # We need to manually format or use template engine
        # Let's use f-string for simplicity or reuse template
        
        from ndoc.core.templates import get_template
        try:
            template = get_template("prompt.md.tpl")
            return template.format(
                target_file=str(rel_path),
                global_rules=global_rules,
                domain_context=domain_context,
                syntax_summary=syntax_summary,
                related_apis=related_apis,
                semantic_context=semantic_context,
                target_code=target_code
            )
        except Exception:
            # Fallback
            return f"""
# Context for {rel_path}

## Global Rules
{global_rules}

## Domain Context
{domain_context}

## Dependencies
{related_apis}

## Code
```
{target_code}
```
"""
