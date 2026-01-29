import json
from pathlib import Path
from ndoc.core import console

VSCODE_DIR = ".vscode"
TASKS_FILE = "tasks.json"

TASKS_CONTENT = {
    "version": "2.0.0",
    "tasks": [
        {
            "label": "ndoc: watch",
            "type": "shell",
            "command": "ndoc watch",
            "isBackground": True,
            "problemMatcher": {
                "owner": "ndoc",
                "fileLocation": ["relative", "${workspaceFolder}"],
                "pattern": {
                    "regexp": "^\\[(!RULE:.*)\\] (.*):(\\d+) - (.*)$",
                    "code": 1,
                    "file": 2,
                    "line": 3,
                    "message": 4
                },
                "background": {
                    "activeOnStart": True,
                    "beginsPattern": "Niki-docAI Watch Daemon",
                    "endsPattern": "Watching:.*"
                }
            },
            "presentation": {
                "reveal": "silent",
                "panel": "dedicated"
            },
            "runOptions": {
                "runOn": "folderOpen"
            }
        },
        {
            "label": "ndoc: verify",
            "type": "shell",
            "command": "ndoc verify",
            "problemMatcher": {
                 "owner": "ndoc",
                 "fileLocation": ["relative", "${workspaceFolder}"],
                 "pattern": {
                    "regexp": "^\\[(!RULE:.*)\\] (.*):(\\d+) - (.*)$",
                    "code": 1,
                    "file": 2,
                    "line": 3,
                    "message": 4
                }
            },
            "group": {
                "kind": "build",
                "isDefault": True
            }
        }
    ]
}

def install_vscode_config(root: Path):
    """
    Creates .vscode/tasks.json for IDE integration.
    """
    vscode_path = root / VSCODE_DIR
    vscode_path.mkdir(exist_ok=True)
    
    tasks_path = vscode_path / TASKS_FILE
    
    # Don't overwrite if exists? Or merge?
    # For now, let's just write/overwrite to ensure latest config
    try:
        with open(tasks_path, 'w', encoding='utf-8') as f:
            json.dump(TASKS_CONTENT, f, indent=4)
        console.success(f"Generated {tasks_path}")
        console.info("VS Code integration enabled. 'ndoc watch' will run on folder open.")
    except Exception as e:
        console.error(f"Failed to generate VS Code config: {e}")

def cmd_ide(root: Path, action: str):
    if action == "install":
        install_vscode_config(root)
    else:
        console.error(f"Unknown ide action: {action}")
