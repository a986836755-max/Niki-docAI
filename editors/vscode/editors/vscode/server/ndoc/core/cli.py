"""
Core: CLI Command Registry.
核心层：动态 CLI 命令注册表。
"""
import inspect
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass

@dataclass
class CommandInfo:
    name: str
    help: str
    handler: Callable
    group: str = "General"

class CommandRegistry:
    _commands: Dict[str, CommandInfo] = {}
    
    @classmethod
    def register(cls, name: str, help: str, group: str = "General"):
        """
        Decorator to register a flow run function as a CLI command.
        """
        def decorator(func: Callable):
            cls._commands[name] = CommandInfo(name=name, help=help, handler=func, group=group)
            return func
        return decorator

    @classmethod
    def get_commands(cls) -> List[CommandInfo]:
        return list(cls._commands.values())

    @classmethod
    def get_handler(cls, name: str) -> Optional[Callable]:
        cmd = cls._commands.get(name)
        return cmd.handler if cmd else None

# Alias for easy import
ndoc_command = CommandRegistry.register
