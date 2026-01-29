import re
import os
import sys
from pathlib import Path
from ndoc.core import console
from ndoc.core import config
from ndoc.base import io

def parse_glossary(root):
    """
    Parses _GLOSSARY.md to extract defined terms.
    Returns a dict: { "term_lower": "Original Term" }
    """
    glossary_path = root / "_GLOSSARY.md"
    if not glossary_path.exists():
        console.warning("_GLOSSARY.md not found.")
        return {}

    terms = {}
    # Regex to capture: * **Term (Optional)**: ...
    # We want the 'Term' part.
    # Case 1: * **Term**:
    # Case 2: * **Term (Cn)**:
    term_pattern = re.compile(r'^\*\s+\*\*([^\*]+)\*\*:')
    
    lines = io.read_lines_safe(glossary_path)
    for line in lines:
        line = line.strip()
        match = term_pattern.match(line)
        if match:
            raw_term = match.group(1)
            # Clean up " (Cn)" suffix if present
            clean_term = re.sub(r'\s*\(.*?\)', '', raw_term)
            terms[clean_term.lower()] = clean_term
                
    return terms

def link_terms_in_file(file_path, terms, glossary_rel_path):
    """
    Scans a file and replaces plain text terms with markdown links.
    Avoids replacing inside existing links or code blocks.
    """
    content = io.read_text_safe(file_path)
    if not content:
        return False

    # We need a robust way to ignore code blocks and existing links.
    # A simple approach is to split by code blocks and only process text parts.
    # Then split by existing links and only process text parts.
    
    # 1. Split by Code Blocks (```...```)
    parts = re.split(r'(```[\s\S]*?```)', content)
    
    new_parts = []
    for part in parts:
        if part.startswith("```"):
            new_parts.append(part)
            continue
            
        # 2. Split by Inline Code (`...`)
        inline_parts = re.split(r'(`[^`]+`)', part)
        
        new_inline_parts = []
        for inline_part in inline_parts:
            if inline_part.startswith("`"):
                new_inline_parts.append(inline_part)
                continue
                
            # 3. Split by Existing Links ([...](...))
            # This regex is basic and might miss nested brackets, but sufficient for standard md.
            link_parts = re.split(r'(\[[^\]]+\]\([^\)]+\))', inline_part)
            
            new_link_parts = []
            for link_part in link_parts:
                if link_part.startswith("[") and link_part.endswith(")"):
                    new_link_parts.append(link_part)
                    continue
                
                # 4. Perform Replacement
                # We sort terms by length descending to match longest first (e.g. "Render Entity" before "Entity")
                sorted_terms = sorted(terms.keys(), key=len, reverse=True)
                
                text = link_part
                for term_lower in sorted_terms:
                    original_term = terms[term_lower]
                    # We use word boundary \b to avoid partial matches
                    # But we must escape special chars in term
                    escaped_term = re.escape(original_term)
                    
                    # Pattern: match case-insensitive term, but capture original casing
                    # We create a regex that matches the term standalone
                    pattern = re.compile(r'\b(' + re.escape(term_lower) + r')\b', re.IGNORECASE)
                    
                    # Replacement function to preserve original casing in text but link to Glossary anchor
                    def replace_func(match):
                        matched_text = match.group(0)
                        # Anchor is usually lowercased and spaces replaced by hyphens
                        anchor = original_term.lower().replace(" ", "-")
                        # Check if matched text is already same as original term (optimization)
                        return f"[{matched_text}]({glossary_rel_path}#{anchor})"
                        
                    # Note: This simple replacement has a flaw: it replaces all occurrences.
                    # Ideally we only link the FIRST occurrence per section or paragraph to avoid noise.
                    # But for now, let's link all for maximum connectivity, or maybe limit?
                    # Let's link ALL for now as per "Semantic Web" concept.
                    
                    # Check if we are not creating double links (already handled by step 3)
                    text = pattern.sub(replace_func, text)
                    
                new_link_parts.append(text)
            
            new_inline_parts.append("".join(new_link_parts))
        
        new_parts.append("".join(new_inline_parts))
        
    new_content = "".join(new_parts)
    
    if new_content != content:
        return io.write_text_safe(file_path, new_content)
    
    return False

def cmd_link(root):
    """
    Main entry point for 'niki link'.
    """
    console.step("Linking Documentation Terms...")
    
    terms = parse_glossary(root)
    if not terms:
        console.error("No terms found in Glossary.")
        return

    console.info(f"Loaded {len(terms)} terms from Glossary.")
    
    # Target files: _AI.md files
    # We search recursively
    ai_files = list(root.rglob("_AI.md"))
    
    # Also include root meta files except Glossary itself
    # Dynamically find all _*.md files in root
    meta_files = list(root.glob("_*.md"))
    
    target_files = ai_files + [f for f in meta_files if f.exists()]
    
    updated_count = 0
    for file_path in target_files:
        # Skip Glossary itself to avoid self-links
        if file_path.name == "_GLOSSARY.md":
            continue
            
        # Calculate relative path to Glossary
        # e.g. from engine/modules/spatial/_AI.md to _GLOSSARY.md is ../../../_GLOSSARY.md
        try:
            rel_path = os.path.relpath(root / "_GLOSSARY.md", file_path.parent)
            # Ensure forward slashes for markdown links
            rel_path = rel_path.replace("\\", "/")
        except ValueError:
            rel_path = "_GLOSSARY.md" # Fallback
            
        if link_terms_in_file(file_path, terms, rel_path):
            console.log(f"  Linked terms in {file_path.relative_to(root)}")
            updated_count += 1
            
    console.success(f"Linked terms in {updated_count} files.")
