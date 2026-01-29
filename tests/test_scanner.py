import pytest
from pathlib import Path
from ndoc.atoms.scanner import scan_file_content

SAMPLE_CONTENT = """
# @TAG arg1 arg2
<!-- NIKI_TEST_START -->
Some Content
<!-- NIKI_TEST_END -->

class TestClass:
    '''Doc'''
    pass
"""

def test_scan_file_content_mixed():
    # Simulate a python file scan
    result = scan_file_content(SAMPLE_CONTENT, file_path=Path("test.py"))
    
    # 1. Tags (Regex)
    assert len(result.tags) == 1
    assert result.tags[0].name == "@TAG"
    assert result.tags[0].args == ["arg1", "arg2"]
    
    # 2. Sections (Regex)
    assert "TEST" in result.sections
    assert "Some Content" in result.sections["TEST"].content.strip()
    
    # 3. Symbols (AST)
    assert len(result.symbols) >= 1
    assert result.symbols[0].name == "TestClass"
    assert result.symbols[0].kind == "class"

def test_scan_file_content_text_only():
    # Simulate non-python file
    content = "# @NOTE just a note"
    result = scan_file_content(content, file_path=Path("test.txt"))
    
    assert len(result.tags) == 1
    assert result.tags[0].name == "@NOTE"
    # AST symbols should be empty for non-python files
    assert len(result.symbols) == 0
