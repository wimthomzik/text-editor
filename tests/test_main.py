from text_editor.main import parse_args
from pathlib import Path

def test_returned_file_path_is_absolut():
    argv = ["text.py"] 
    file_path = parse_args(argv)
    assert file_path.is_absolute()
    
def test_filled_argv_returns_file_name():
    argv = ["text.py"] 
    file_path = parse_args(argv)
    assert file_path.name == "text.py"
    
def test_no_argv_returns_none():
    file_path = parse_args()

    assert file_path == None
    
def test_empty_argv_returns_none():
    argv = []
    file_path = parse_args(argv)
    assert file_path is None

def test_dotdot_not_collapsed():
    file_path = parse_args(["a/../text.py"])
    assert ".." in str(file_path)