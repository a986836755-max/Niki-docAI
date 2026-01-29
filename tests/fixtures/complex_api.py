
import typing
from dataclasses import dataclass

@dataclass
class User:
    """
    A user class.
    """
    name: str
    age: int = 18
    _internal: bool = False

    def __init__(self, name: str):
        self.name = name

    @property
    def is_adult(self) -> bool:
        return self.age >= 18

    async def fetch_data(self) -> dict:
        """Fetch data asynchronously."""
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(name=data['name'])

class Database:
    connection_string: str = "localhost:5432"
    
    def connect(self):
        pass

def global_func(x: int, y: int) -> int:
    return x + y

async def global_async_func():
    pass
