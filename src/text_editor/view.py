from text_editor.model import EditorModel

class View:
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        
    def draw(self, model: EditorModel) -> None:
        self.stdscr.clear()
        for i in range(model.document.line_count()):
            self.stdscr.addstr(i, 0, model.document.get_line(i))    
        self.stdscr.move(model.cursor.line, model.cursor.column)
        self.stdscr.refresh()