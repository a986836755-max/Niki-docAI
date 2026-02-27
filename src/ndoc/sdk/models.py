"""
Core Data Models (Entities & Components)
"""
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, List, Any, Set
from pydantic import BaseModel, Field
from ndoc.models.symbol import Symbol

# --- Entity ---
class EntityType(str, Enum):
    FILE = "file"
    MODULE = "module"
    SYMBOL = "symbol"

class Entity(BaseModel):
    """
    Base Entity in ECS.
    Ideally just an ID, but we keep some basic metadata for convenience.
    """
    id: str = Field(..., description="Unique Identifier (e.g. file path or symbol signature)")
    type: EntityType
    name: str
    path: Path

# --- Components ---
class Component(BaseModel):
    """Base class for all components"""
    pass

class SyntaxComponent(Component):
    """Stores raw source code and AST info"""
    language: str
    content: str
    # We don't store raw AST object here to keep it serializable.
    # Instead, we might store a hash or a handle.
    ast_digest: Optional[str] = None 

class MetaComponent(Component):
    """Stores metadata like tags, TODOs, docstrings"""
    tags: Set[str] = Field(default_factory=set)
    todos: List[Dict[str, Any]] = Field(default_factory=list)
    docstring: Optional[str] = None
    
class MemoryComponent(Component):
    """Stores extracted memories (@DECISION, @LESSON, etc.)"""
    memories: List[Dict[str, Any]] = Field(default_factory=list)
    decisions: List[Dict[str, Any]] = Field(default_factory=list)
    lessons: List[Dict[str, Any]] = Field(default_factory=list)
    intents: List[str] = Field(default_factory=list)

    
class GraphComponent(Component):
    """Stores dependency relationships"""
    imports: List[str] = Field(default_factory=list) # List of Entity IDs this entity imports
    imported_by: List[str] = Field(default_factory=list) # List of Entity IDs that import this entity

class VectorComponent(Component):
    """Stores embedding vectors"""
    embedding: Optional[List[float]] = None
    model_version: str = "v1"

class SymbolComponent(Component):
    """Stores extracted code symbols (classes, functions, etc.)"""
    symbols: List[Symbol] = Field(default_factory=list)

