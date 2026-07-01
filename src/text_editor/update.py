from text_editor.model import EditorModel, Cursor, Lifecycle, Mode, TextBuffer
from text_editor.events import Event, Char, Escape, Backspace, Enter, Arrow, Direction
from dataclasses import replace

DIRECTION_KEYS = {'h': Direction.LEFT, 'j': Direction.DOWN, 'k': Direction.UP, 'l': Direction.RIGHT}

def _clamp(value: int, minimum: int, maximum: int):
    return max(minimum, min(value, maximum))

def move_cursor(cursor: Cursor, direction: Direction, buffer: TextBuffer) -> Cursor:
    match direction:
        case Direction.LEFT:
            return replace(cursor, column=_clamp(cursor.column - 1, 0, len(buffer.get_line(cursor.line))))
        case Direction.RIGHT:
            return replace(cursor, column=_clamp(cursor.column + 1, 0, len(buffer.get_line(cursor.line))))
        case Direction.UP:
            new_line = _clamp(cursor.line - 1, 0, buffer.line_count() - 1)
            return replace(cursor, line=new_line, column=min(cursor.column, len(buffer.get_line(new_line))))
        case Direction.DOWN:
            new_line = _clamp(cursor.line + 1, 0, buffer.line_count() - 1)
            return replace(cursor, line=new_line, column=min(cursor.column, len(buffer.get_line(new_line))))
        case _:
            raise ValueError("Unknown direction")
            
def backspace_cursor(cursor: Cursor, buffer: TextBuffer):
    """
    Computes the cursor position after a Backspace, given the buffer
    *before* the edit is applied (delete_character / merge_line).
    """
    if cursor.column == 0 and cursor.line == 0:
        return cursor
    elif cursor.column == 0:
        return Cursor(cursor.line - 1, len(buffer.get_line(cursor.line - 1)))
    else: 
        return Cursor(cursor.line, cursor.column - 1)
    
# TODO: Write unit tests
def update(model: EditorModel, event: Event) -> EditorModel:
    if isinstance(event, Arrow):
         return replace(model, cursor=move_cursor(model.cursor, event.direction, model.document))
     
    elif model.mode is Mode.NORMAL:
        match event:
            case Char(char):
                if char == 'i':
                    return replace(model, mode=Mode.INSERT)
                elif char == 'q':
                    return replace(model, lifecycle=Lifecycle.QUIT)
                elif char in DIRECTION_KEYS:
                    return replace(model, cursor=move_cursor(model.cursor, DIRECTION_KEYS[char], model.document))
                return model
            case Escape():
                # Placeholder
                return model
            case Enter():
                return replace(model, cursor=move_cursor(model.cursor, Direction.DOWN, model.document))
            case Backspace():
                return replace(model, cursor=backspace_cursor(model.cursor, model.document))
            case _:
                raise ValueError(f"unhandled event: {event} in mode {model.mode}")
            
    elif model.mode is Mode.INSERT:
        match event:
            case Escape():
                return replace(model, mode=Mode.NORMAL)
            case Char(char):
                updated_buffer = model.document.insert_text(model.cursor.line, model.cursor.column, char)
                updated_cursor = Cursor(model.cursor.line, model.cursor.column + 1)
            case Enter():
                updated_buffer = model.document.split_line(model.cursor.line, model.cursor.column)
                updated_cursor = Cursor(model.cursor.line + 1, 0)
                # TODO: column in new line must be adjusted to intent of original line
            case Backspace():
                # TODO Test Backspace policy: delete the char before the cursor
                if model.cursor.column == 0 and model.cursor.line == 0:
                    return model
                updated_cursor = backspace_cursor(model.cursor, model.document)
                if model.cursor.column == 0:
                    updated_buffer = model.document.merge_line(model.cursor.line - 1)
                else:
                    updated_buffer = model.document.delete_character(model.cursor.line, model.cursor.column - 1)
            case _:
                raise ValueError(f"unhandled event: {event} in mode {model.mode}")
        return replace(model, cursor=updated_cursor, document=updated_buffer)
            
    raise ValueError(f"unhandled event: {event} in mode {model.mode}")