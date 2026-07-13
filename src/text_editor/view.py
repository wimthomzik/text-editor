from text_editor.model import EditorModel, Mode
import curses

class View:
    
    def __init__(self, stdscr: "curses.window"):
        self.stdscr = stdscr
    
    def draw(self, model: EditorModel) -> None:
        self.stdscr.clear()
        for i in range(model.document.line_count()):
            self.stdscr.addstr(i, 0, model.document.get_line(i))    
        self.stdscr.move(model.cursor.line, model.cursor.column)
        
        if model.mode == Mode.COMMAND_LINE:
            y, _ = self.stdscr.getmaxyx()
            sub_window = self.stdscr.subwin(y - 1, 0)
            sub_window.addstr(0, 0, model.cmdline.line)
            self.stdscr.move(y - 1, model.cmdline.column)
            
        self.stdscr.refresh()