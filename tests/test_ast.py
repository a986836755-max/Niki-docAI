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
    assert method.kind == "function" 
    
    # 3. Property
    prop = symbols[2]
    assert prop.name == "prop_one"
    assert prop.kind == "property"
    
    # 4. Class Method
    cm = symbols[3]
    assert cm.name == "class_method"
    assert cm.kind == "classmethod"
    
    # 5. Static Method
    sm = symbols[4]
    assert sm.name == "static_method"
    assert sm.kind == "staticmethod"
    
    # 6. Global Function
    func = symbols[5]
    assert func.name == "global_func"
    assert func.kind == "function"
