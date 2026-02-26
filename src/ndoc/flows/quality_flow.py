"""
Flow: Quality Gates.
业务流：执行 lint 与 typecheck 命令。
"""
import subprocess
import shlex
import os
from pathlib import Path
from typing import List

from ndoc.models.config import ProjectConfig
from ..core.logger import logger

def _run_commands(label: str, commands: List[str], root_path: Path) -> bool:
    if not commands:
        logger.warning(f"{label} commands not configured in _RULES.md")
        return True
    logger.info(f"Running {label} commands ({len(commands)})")
    for cmd in commands:
        if not cmd:
            continue
        logger.info(f"[{label}] {cmd}")
        use_shell = any(op in cmd for op in ["&&", "||", "|", ">", "<"])
        try:
            if use_shell:
                result = subprocess.run(cmd, cwd=root_path, shell=True, text=True, capture_output=True)
            else:
                args = shlex.split(cmd, posix=os.name != "nt")
                result = subprocess.run(args, cwd=root_path, shell=False, text=True, capture_output=True)
        except Exception as e:
            logger.error(f"{label} failed: {cmd} ({e})")
            return False
        if result.returncode != 0:
            if result.stdout:
                logger.error(result.stdout.strip())
            if result.stderr:
                logger.error(result.stderr.strip())
            logger.error(f"{label} failed: {cmd} (exit {result.returncode})")
            return False
    logger.info(f"{label} completed")
    return True

def run_lint(config: ProjectConfig) -> bool:
    return _run_commands("lint", config.lint_commands, config.scan.root_path)

def run_typecheck(config: ProjectConfig) -> bool:
    return _run_commands("typecheck", config.typecheck_commands, config.scan.root_path)
