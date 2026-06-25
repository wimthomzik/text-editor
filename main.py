import argparse
from pathlib import Path

def main():
    
    # TODO Pull out as function and commit
    # Handle command line arguments (argv) -> path: Optional(Path)
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", nargs="?", default=None)
    args = parser.parse_args()
    file_path = Path(args.file_path).absolute() if args.file_path is not None else None

    # Pass path to io_file object to get a representation of the file usable for the state -> file buffer
     # 1. no argument -> create temp buffer in mem
        # 2. one argument
            # a) valid filepath -> open & load file
            # b) invalid filepath -> create temp buffer in mem (safe filepath in case of :wq)
    
    # Create state object and init it with the file buffer from above
        
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
