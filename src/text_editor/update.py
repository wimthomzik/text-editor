from src.text_editor.model import EditorModel, Cursor, Lifecycle
from src.text_editor.events import Event, Char, Quit, Backspace, Enter
from dataclasses import replace

# TODO: Write unit tests
def update(model: EditorModel, event: Event) -> EditorModel:
    match event:
        case Char(char):
            updated_buffer = model.document.insert_text(model.cursor.line, model.cursor.column, char)
            updated_cursor = Cursor(model.cursor.line, model.cursor.column + 1)
            return replace(model, cursor=updated_cursor, document=updated_buffer)
        case Enter():
            updated_buffer = model.document.split_line(model.cursor.line, model.cursor.column)
            # TODO: column in new line must be adjusted to intend of original line
            updated_cursor = Cursor(model.cursor.line + 1, 0)
            return replace(model, cursor=updated_cursor, document=updated_buffer)
        case Backspace():
            # TODO Test Backspace policy: delete the char before the cursor
            if model.cursor.column == 0 and model.cursor.line == 0:
                return model
            elif model.cursor.column == 0:
                upper_line_length = len(model.document.get_line(model.cursor.line - 1))
                updated_buffer = model.document.merge_line(model.cursor.line - 1)
                updated_cursor = Cursor(model.cursor.line - 1, upper_line_length)
            else: 
                updated_buffer = model.document.delete_character(model.cursor.line, model.cursor.column - 1)
                updated_cursor = Cursor(model.cursor.line, model.cursor.column - 1)
            return replace(model, cursor=updated_cursor, document=updated_buffer)
        case Quit():
            return replace(model, lifecycle=Lifecycle.QUIT)
                
        