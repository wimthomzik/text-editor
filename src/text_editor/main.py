import argparse
from pathlib import Path
from text_editor.model import EditorModel, TupleBuffer, TextBuffer, Lifecycle, Mode
from text_editor.update import update
from text_editor.view import View
from text_editor.input_handler import InputHandler
import curses

# argv param exists for testability: tests inject a list, prod reads sys.argv
def parse_args(argv: list[str] | None = None) -> Path | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", nargs="?", default=None)
    args = parser.parse_args(argv)
    # absolute, not resolve: don't follow symlinks
    return Path(args.file_path).absolute() if args.file_path is not None else None


# TODO: inject buffer type so main doesn't name TupleBuffer directly
#       trigger: second buffer (RopeBuffer/PieceTableBuffer)
def load_buffer_from_file(file_path: Path | None) -> TextBuffer:
    if file_path is None:
        return TupleBuffer(('',))
    try:
        # reminder: splitlines throws information of trailing new line away. handle case to set trailing new line flag
        return TupleBuffer(tuple(file_path.read_text().splitlines()))    
    except OSError:
        return TupleBuffer(('',))

def terminal_setup():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

def terminal_teardown(terminal):
    curses.nocbreak()
    terminal.keypad(False)
    curses.echo()
    curses.endwin()

def main():

    file_path = parse_args()
    buffer = load_buffer_from_file(file_path)
    editor_model = EditorModel(document=buffer, mode=Mode.NORMAL)
    terminal = terminal_setup()      
    view = View(terminal)
    input_handler = InputHandler(terminal)

    try:
        while editor_model.lifecycle is Lifecycle.RUNNING:
            
            view.draw(editor_model)            
            editor_model = update(editor_model, input_handler.next_event())
            
    finally:
            terminal_teardown(terminal)
    # post-loop: act on editor_model.lifecycle (save / discard / exit)
    
    

if __name__ == "__main__":
    main()
