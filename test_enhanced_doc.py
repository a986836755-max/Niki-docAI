"""
@MODULE TestModule
This is a test module for enhanced docstring capture.
It should support multi-line docstrings and tags.
@VERSION 1.0.0
"""

# @CORE
# This is a core function.
# It has multi-line comments.
# @TAG1 arg1
# @TAG2 arg2
def test_func(a: int, b: str) -> bool:
    """
    Inner docstring for test_func.
    @INTERNAL
    """
    return True

class TestClass:
    """
    Test class docstring.
    """
    
    # Multi-line comment for field
    # with a tag.
    # @FIELD_TAG
    field: int = 10
    
    def test_method(self):
        # Comment for method
        # @METHOD_TAG
        pass
