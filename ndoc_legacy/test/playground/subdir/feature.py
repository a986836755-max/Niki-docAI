"""
Feature module in subdirectory.
Used to test recursive scanning and graph dependencies.
"""

from ..utils import Calculator

def advanced_op():
    """
    Performs an advanced operation using the Calculator.
    """
    calc = Calculator()
    return calc.add(100, 200)
