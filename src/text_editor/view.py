from text_editor.model import EditorModel, Mode
import curses
from math import ceil

def _height(line_length: int, width: int) -> int:
        return max(1, ceil(line_length / width))
    
class View:
    
    def __init__(self, stdscr: "curses.window"):
        self.stdscr = stdscr
    
    def draw(self, model: EditorModel) -> None:
        self.stdscr.clear()
        y_max, x_max = self.stdscr.getmaxyx()
        total_height = 0
        height_before_cursor_line = 0
        for i in range(model.document.line_count()):
            height = _height(len(model.document.get_line(i)), x_max)
            self.stdscr.addstr(total_height, 0, model.document.get_line(i))
            if i == model.cursor.line:
                height_before_cursor_line = total_height
            total_height += height
            
        self.stdscr.move(height_before_cursor_line + (model.cursor.column // x_max), model.cursor.column % x_max)
            
        if model.mode == Mode.COMMAND_LINE:
            sub_window = self.stdscr.subwin(y_max - 1, 0)
            sub_window.addstr(0, 0, model.cmdline.line)
            self.stdscr.move(y_max - 1, model.cmdline.column)
            
        self.stdscr.refresh()