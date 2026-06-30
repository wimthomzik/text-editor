from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

@dataclass(frozen=True)
class Char:
    char: str
    
@dataclass(frozen=True)
class Escape: ...

@dataclass(frozen=True)
class Arrow():
    direction: Direction

@dataclass(frozen=True)
class Backspace: ...

@dataclass(frozen=True)
class Enter: ...

Event = Char | Backspace | Enter | Arrow | Escape