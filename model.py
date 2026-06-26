@dataclass(frozen=True)
class EditorModel:
    
    document: TextBuffer
    cursor_pos: int = 0
    mode: Mode = Mode.NORMAL
        
    