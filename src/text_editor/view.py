from text_editor.model import EditorModel, Mode, ScreenPosition
import curses
from math import ceil

def line_offsets(line_lengths: list[int], width: int) -> list[int]:
    """Returns n+1 y-positions: offsets[i] = start y of line i;
    offsets[n] = total height.
    
    Precondition: width >= 1.
    """
    assert width >= 1, f"width must be positive, got {width}"
    
    offsets = []
    total_height = 0
    for length in line_lengths:
        offsets.append(total_height)
        total_height += max(1, ceil(length / width))
    offsets.append(total_height)
    return offsets
    
def to_screen_position(line_start_y: int, column: int, width: int) -> ScreenPosition:
    return ScreenPosition(line_start_y + (column // width), column % width)

class View:
    
    # Could do document view, commandline view
    
    def __init__(self, stdscr: "curses.window"):
        self.stdscr = stdscr
    
    def draw(self, model: EditorModel) -> None:
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        offsets = line_offsets([len(model.document.get_line(i)) for i in range(model.document.line_count())], width)
        
        for i in range(model.document.line_count()):
            self.stdscr.addstr(offsets[i], 0, model.document.get_line(i))
            
        if model.mode == Mode.COMMAND_LINE:
            sub_window = self.stdscr.subwin(height - 1, 0)
            sub_window.addstr(0, 0, model.cmdline.line)
            self.stdscr.move(height - 1, model.cmdline.column)
        else:
            cursor_screen_pos = to_screen_position(offsets[model.cursor.line], model.cursor.column, width)
            self.stdscr.move(cursor_screen_pos.y, cursor_screen_pos.x)
            
        self.stdscr.refresh()