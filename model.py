from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

   
class TextBuffer(ABC):
    
    @abstractmethod
    def delete_character(self, position: int) -> "TextBuffer":
        pass
    
    @abstractmethod
    def insert_character(self, position: int, character: str) -> "TextBuffer":
        pass

@dataclass(frozen=True) 
class TupleBuffer(TextBuffer):
    
    buffer : tuple[str, ...] = ()
    
    def delete_character(self, position: int) -> "TupleBuffer":
        return TupleBuffer(self.buffer[:position] + self.buffer[position + 1:])
    
    def insert_character(self, position: int, character: str) -> "TupleBuffer":
        return TupleBuffer(self.buffer[:position] + (character,) + self.buffer[position:])
        
class Mode(Enum):
    NORMAL = 1
    INSERT = 2
    
@dataclass(frozen=True)
class EditorModel:
    
    document: TextBuffer
    cursor_pos: int = 0
    mode: Mode = Mode.NORMAL
        
    