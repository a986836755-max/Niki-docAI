# Niki-DocAI Test & Demo Playground

This directory is used for testing `ndoc` capabilities and demonstrating its usage.

## Structure
- `playground/`: A sample project containing Python scripts.
    - `main.py`: Entry point with function docstrings.
    - `utils.py`: Helper module with class docstrings.

## How to Test
You can run the `ndoc` CLI in the `playground` directory to see how it generates documentation.

### 1. Initialize Documentation
Run the following command to generate `_AI.md` files:
```powershell
$env:PYTHONPATH="src"; py -m ndoc.cli docs init test/playground --all
```

### 2. Update Documentation (Auto-fill)
Run the following command to extract docstrings and fill `_AI.md`:
```powershell
$env:PYTHONPATH="src"; py -m ndoc.cli docs update test/playground --all
```

### 3. Check Results
Inspect `test/playground/_AI.md` to see the generated content and extracted docstrings.
