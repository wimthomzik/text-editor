from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

class TextBuffer(ABC):
    """
    Abstract line-based text buffer.

    Implementations store text as lines (no trailing newlines) and must be
    immutable: every operation returns a new buffer, never mutates self.
    Positions (line, column) are assumed in range — callers guard bounds.
    """
    
    @abstractmethod
    def delete_character(self, line: int, column: int) -> "TextBuffer":
        """Insert text within a line at column. Does not split lines."""
        ...
    
    @abstractmethod
    def insert_text(self, line: int, column: int, text: str) -> "TextBuffer":
        """Insert text into the line at column. Stays on one line; does not split."""
        ...

    
    @abstractmethod
    def split_line(self, line: int, column: int) -> "TextBuffer":
        """Split the line at column into two lines (the newline operation)"""
        ...

@dataclass(frozen=True)
class TupleBuffer(TextBuffer):
    
    """
    Immutable line-based buffer. Lines stored without trailing newlines.

    Invariants:
    - always holds at least one line (empty buffer is ('',), never ())
    - all operations transform: return a new buffer, never mutate self

    Caller's contract: positions (line, column) must be in range.
    Bounds are the model's responsibility (update()), not the buffer's.
    """
    
    buffer: tuple[str, ...] = ('',)
    
    def _replace_line(self, mod: str, line: int) -> "TupleBuffer": 
        return TupleBuffer(self.buffer[:line] + (mod,) + self.buffer[line + 1:])
    
    def delete_character(self, line: int, column: int) -> "TupleBuffer":
        current = self.buffer[line]
        modified = current[:column] + current[column + 1:]
        return self._replace_line(modified, line)
    
    def insert_text(self, line: int, column: int, text: str) -> "TupleBuffer":
        current = self.buffer[line]
        modified = current[:column] + text + current[column:]
        return self._replace_line(modified, line)
    
    # Use for inserting '\n' character
    def split_line(self, line: int, column: int) -> "TupleBuffer":
        current_line = self.buffer[line]
        head, tail = current_line[:column], current_line[column:]
        return TupleBuffer(self.buffer[:line] + (head, tail) + self.buffer[line + 1:])
        
class Mode(Enum):
    NORMAL = 1
    INSERT = 2

class Lifecycle(Enum):
    RUNNING = 1
    QUIT = 2
     
# TODO: add 'desired_column' for vertical movement (j/k).
#       when moving to a shorter line, col clamps; moving back to a longer
#       line should restore the original column, not the clamped one.
#       trigger: implementing up/down cursor motion.
@dataclass(frozen=True)
class Cursor:
    line: int = 0
    column: int = 0
    
@dataclass(frozen=True)
class EditorModel:
    
    document: TextBuffer
    cursor: Cursor = field(default_factory=Cursor)
    mode: Mode = Mode.NORMAL
    lifecycle: Lifecycle = Lifecycle.RUNNING
    
    # TODO: add 'trailing_newline: bool' — splitlines() drops whether the
    #       file ended in \n. needed to round-trip correctly on save.
    #       trigger: implementing save.
        
    