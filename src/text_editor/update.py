from text_editor.model import EditorModel, Cursor, Lifecycle, Mode, TextBuffer, CommandLine
from text_editor.events import Event, Char, Escape, Backspace, Enter, Arrow, Direction
from dataclasses import replace
from text_editor.effects import Effect

DIRECTION_KEYS = {'h': Direction.LEFT, 'j': Direction.DOWN, 'k': Direction.UP, 'l': Direction.RIGHT}

def _clamp(value: int, minimum: int, maximum: int):
    """Constrain value to [minimum, maximum].

    Precondition: minimum <= maximum (caller's responsibility; asserted).
    """
    assert minimum <= maximum, f"clamp bounds inverted: {minimum} > {maximum}"
    return max(minimum, min(value, maximum))


def move_cursor(cursor: Cursor, direction: Direction, buffer: TextBuffer) -> Cursor:
    """Move cursor one step in direction, returning an always-legal Cursor.

    Column is clamped to the target line's length; line to the buffer's
    bounds. Vertical moves preserve the column where possible, clamping
    down onto shorter lines.
    """
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

# TODO: add tests for new Mode
def update(model: EditorModel, event: Event) -> tuple[EditorModel, Effect]:
    """Pure transition: (model, event) -> new model. Total over all events.

    The trust boundary. Turns untrusted low-level events into legal state
    transitions; owns all policy (mode meaning, ±1 offsets, quit derivation,
    bounds via move_cursor/backspace_cursor). Never performs effects.
    Unhandled (event, mode) raises — a forgotten handler is a bug, fail loud.
    """
    
    if model.mode is Mode.COMMAND_LINE:
        match event:
            case Escape():
                return replace(model, mode=Mode.NORMAL, cmdline=CommandLine()), None
            case Backspace():
                if model.cmdline.column == 0:
                    return replace(model, mode=Mode.NORMAL, cmdline=CommandLine()), None
                return replace(model, cmdline=model.cmdline.delete_character()), None
            case Char(char):
                return replace(model, cmdline=model.cmdline.insert_text(char)), None
            case Arrow():
                if event.direction == Direction.LEFT:
                    return replace(model, cmdline=model.cmdline.move_left()), None
                elif event.direction == Direction.RIGHT:
                    return replace(model, cmdline=model.cmdline.move_right()), None
            case Enter():
                if model.cmdline.line == ":q":
                    return replace(model, lifecycle=Lifecycle.QUIT, cmdline=CommandLine()), None
                elif model.cmdline.line == ":wq":
                    return replace(model, lifecycle=Lifecycle.QUIT, cmdline=CommandLine()), Effect.WRITE
                elif model.cmdline.line == ":w":
                    return replace(model, mode=Mode.NORMAL, cmdline=CommandLine()), Effect.WRITE
                else:
                    # TODO: Have to add error message or something here
                    return replace(model, mode=Mode.NORMAL, cmdline=CommandLine()), None
                    
            case _:
                raise ValueError(f"unhandled event: {event} in mode {model.mode}")
    elif model.mode is Mode.NORMAL:
        match event:
            case Arrow():
                return replace(model, cursor=move_cursor(model.cursor, event.direction, model.document)), None
            case Char(char):
                if char == 'i':
                    return replace(model, mode=Mode.INSERT), None
                elif char == ':':
                    return replace(model, mode=Mode.COMMAND_LINE), None
                elif char in DIRECTION_KEYS:
                    return replace(model, cursor=move_cursor(model.cursor, DIRECTION_KEYS[char], model.document)), None
                return model, None
            case Escape():
                # Placeholder
                return model, None
            case Enter():
                return replace(model, cursor=move_cursor(model.cursor, Direction.DOWN, model.document)), None
            case Backspace():
                return replace(model, cursor=backspace_cursor(model.cursor, model.document)), None
            case _:
                raise ValueError(f"unhandled event: {event} in mode {model.mode}")
            
    elif model.mode is Mode.INSERT:
        match event:
            case Arrow():
                return replace(model, cursor=move_cursor(model.cursor, event.direction, model.document)), None
            case Escape():
                return replace(model, mode=Mode.NORMAL), None
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
                    return model, None
                updated_cursor = backspace_cursor(model.cursor, model.document)
                if model.cursor.column == 0:
                    updated_buffer = model.document.merge_line(model.cursor.line - 1)
                else:
                    updated_buffer = model.document.delete_character(model.cursor.line, model.cursor.column - 1)
            case _:
                raise ValueError(f"unhandled event: {event} in mode {model.mode}")
        return replace(model, cursor=updated_cursor, document=updated_buffer), None
            
    raise ValueError(f"unhandled event: {event} in mode {model.mode}")