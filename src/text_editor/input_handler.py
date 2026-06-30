import curses
from text_editor.events import Char, Backspace, Enter, Escape, Arrow, Direction, Event

class InputHandler:
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        
    def next_event(self) -> Event:
        while True:
            key = self.stdscr.getch()
            match key:
                case 0x7f | 0x08:
                    return Backspace()
                case 0x0a | 0x0d:
                    return Enter()
                case 0x1b:
                    return Escape()
                case curses.KEY_UP:
                    return Arrow(Direction.UP)
                case curses.KEY_DOWN:
                    return Arrow(Direction.DOWN)
                case curses.KEY_LEFT:
                    return Arrow(Direction.LEFT)
                case curses.KEY_RIGHT:
                    return Arrow(Direction.RIGHT)
                case _ if 32 <= key <= 126:
                    return Char(chr(key))
                # anything else: key ignore, read again