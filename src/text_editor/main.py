import argparse
from pathlib import Path
from text_editor.model import EditorModel, TupleBuffer, TextBuffer

# argv param exists for testability: tests inject a list, prod reads sys.argv
def parse_args(argv: list[str] | None = None) -> Path | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", nargs="?", default=None)
    args = parser.parse_args(argv)
    # absolute, not resolve: don't follow symlinks (vim-like)
    return Path(args.file_path).absolute() if args.file_path is not None else None


# TODO: inject buffer type so main doesn't name TupleBuffer directly.
#       trigger: second buffer (RopeBuffer/PieceTableBuffer) appears.
def load_buffer(file_path: Path | None) -> TextBuffer:
    if file_path is None:
        return TupleBuffer(('',))
    try:
        # reminder: splitlines throws information of trailing new line away. handle case to set trailing new line flag
        return TupleBuffer(tuple(file_path.read_text().splitlines()))    
    except OSError:
        return TupleBuffer(('',))
    

def main():

    file_path = parse_args()
    buffer = load_buffer(file_path)
    editor_model = EditorModel(buffer)
    
    # Create input_handler object
        
    # Create renderer object
        
    # Create logger object
        
    # Run event loop
    # while editor.lifecycle is Lifecycle.RUNNING:
    
        # input handler converts key strokes into events
        
        # logger logs event
        
        # state = update(state, event)
        
        # given the new  state the renderer renders the new content to screen
        
    # the io_file object handles the editors docuement depending on state lifecycle
        

if __name__ == "__main__":
    main()
