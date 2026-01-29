import pytest
from ndoc.atoms.ast import parse_code, extract_symbols
from ndoc.models.context import Symbol

SAMPLE_CODE = """
class MyClass:
    '''Class Docstring'''
    
    def method_one(self, a, b):
        '''Method One Doc'''
        return a + b
        
    @property
    def prop_one(self):
        '''Property One Doc'''
        return 1
        
    @classmethod
    def class_method(cls):
        '''Class Method Doc'''
        pass
        
    @staticmethod
    def static_method():
        pass

def global_func(x: int) -> int:
    '''Global Func Doc'''
    return x * 2
"""

def test_extract_symbols_basic():
    tree = parse_code(SAMPLE_CODE)
    symbols = extract_symbols(tree, SAMPLE_CODE.encode('utf-8'))
    
    # Debug print
    for s in symbols:
        print(f"{s.kind} {s.name}: {s.signature}")
    
    assert len(symbols) == 6
    
    # 1. Class
    cls = symbols[0]
    assert cls.name == "MyClass"
    assert cls.kind == "class"
    
    # 2. Method
    method = symbols[1]
    assert method.name == "method_one"
    assert method.kind == "method" 
    assert method.parent == "MyClass"
    
    # 3. Property
    prop = symbols[2]
    assert prop.name == "prop_one"
    assert prop.kind == "property"
    assert prop.parent == "MyClass"
    
    # 4. Class Method
    cm = symbols[3]
    assert cm.name == "class_method"
    assert cm.kind == "classmethod"
    assert cm.parent == "MyClass"
    
    # 5. Static Method
    sm = symbols[4]
    assert sm.name == "static_method"
    assert sm.kind == "staticmethod"
    assert sm.parent == "MyClass"
    
    # 6. Global Function
    func = symbols[5]
    assert func.name == "global_func"
    assert func.kind == "function"
    assert func.parent is None

def test_extract_complex_api():
    from ndoc.atoms.io import read_text
    from pathlib import Path
    
    fixture_path = Path(__file__).parent / "fixtures" / "complex_api.py"
    if not fixture_path.exists():
        pytest.skip("complex_api.py fixture not found")
        
    content = read_text(fixture_path)
    tree = parse_code(content)
    symbols = extract_symbols(tree, content.encode('utf-8'))
    
    # Helper to find symbol
    def find_sym(name):
        return next((s for s in symbols if s.name == name), None)
        
    # Async Method
    fetch = find_sym("fetch_data")
    assert fetch is not None
    assert fetch.kind == "async_method"
    assert fetch.parent == "User"
    assert "-> dict" in fetch.signature
    
    # Async Function
    g_async = find_sym("global_async_func")
    assert g_async is not None
    assert g_async.kind == "async_function"
    assert g_async.parent is None
    
    # Class Variables
    name_var = find_sym("name")
    # Note: 'name' might be ambiguous if multiple classes have it, but in fixture User.name is unique top level? No, it's inside User.
    # But extract_symbols returns flat list. 
    # Wait, variable names are 'name', 'age', '_internal'.
    # If multiple classes have 'name', find_sym needs to check parent.
    
    def find_member(cls_name, name):
        return next((s for s in symbols if s.name == name and s.parent == cls_name), None)

    name_var = find_member("User", "name")
    assert name_var.kind == "variable"
    assert ": str" in name_var.signature
    
    age_var = find_member("User", "age")
    assert age_var.kind == "variable"
    assert "= 18" in age_var.signature
    
    # Classmethod with forward ref
    from_dict = find_member("User", "from_dict")
    assert from_dict.kind == "classmethod"
    assert '-> "User"' in from_dict.signature
