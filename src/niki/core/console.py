import sys
import os

# ANSI Colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

def success(msg):
    """Prints a success message with a green checkmark."""
    print(f"{GREEN}√ {BOLD}{msg}{RESET}")

def error(msg):
    """Prints an error message with a red cross."""
    print(f"{RED}x {BOLD}{msg}{RESET}")

def warning(msg):
    """Prints a warning message with a yellow exclamation mark."""
    print(f"{YELLOW}! {BOLD}{msg}{RESET}")

def info(msg):
    """Prints an info message with a blue 'i'."""
    print(f"{BLUE}i {BOLD}{msg}{RESET}")

def step(msg):
    """Prints a step header (cyan arrow)."""
    print(f"\n{BOLD}{CYAN}==> {msg}{RESET}")

def header(msg):
    """Prints a main header."""
    print(f"\n{BOLD}{MAGENTA}# {msg}{RESET}")

def cmd(msg):
    """Prints a command being executed (dimmed)."""
    print(f"{DIM}[$] {msg}{RESET}")

def log(msg):
    """Prints a generic log message (dimmed)."""
    print(f"{DIM}{msg}{RESET}")

def detail(key, value):
    """Prints a key-value pair detail."""
    print(f"  {DIM}{key}:{RESET} {value}")
