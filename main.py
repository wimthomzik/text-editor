import argparse
from pathlib import Path
from model import EditorModel, TupleBuffer

# TODO: write tests
# Parse command line arguments for file_path and return it if present (argv argument available for testability)
def parse_args(argv: list[str] | None = None) -> Path | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", nargs="?", default=None)
    args = parser.parse_args(argv)
    return Path(args.file_path).absolute() if args.file_path is not None else None

def main():

    # Handle command line arguments (argv) -> path: Optional(Path)
    file_path = parse_args()
    print(f"filepath: {file_path}")
    
    # Get a representation of the file usable for the model
    # TODO: That is not a general implementat right? can that be abstracted for any kind of Buffer?
    # TODO: pull out the logic into module?
    if file_path is None:
        document = ()
    else:
        try:
            document = tuple(file_path.read_text())
        except OSError:
            document = ()
    
    # Create state object and init it with the file buffer from above
    editor_model = EditorModel(TupleBuffer(document))
    
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
