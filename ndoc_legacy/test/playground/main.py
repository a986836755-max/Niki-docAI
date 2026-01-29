"""
Main Entry Point for Demo Application.
This script demonstrates how Niki-DocAI extracts docstrings.
"""

import sys
from utils import Calculator

def main():
    """
    Main function to run the demo.
    It initializes the Calculator and performs basic operations.
    """
    print("Starting Demo...")
    calc = Calculator()
    result = calc.add(10, 5)
    print(f"10 + 5 = {result}")

if __name__ == "__main__":
    main()
