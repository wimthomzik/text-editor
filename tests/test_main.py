from text_editor.main import parse_args, load_buffer_from_file
from text_editor.model import TupleBuffer
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
    
def test_load_buffer_none_returns_single_empty_line():
    result = load_buffer_from_file(None)
    assert result == TupleBuffer(('',))
    
def test_load_buffer_reads_lines_without_newlines(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("first\nsecond\nthird\n")
    result = load_buffer_from_file(file)
    assert result == TupleBuffer(("first", "second", "third"))

def test_load_buffer_unreadable_path_returns_single_empty_line(tmp_path):
    result = load_buffer_from_file(tmp_path)
    assert result == TupleBuffer(('',))

def test_load_buffer_nonexistent_path_returns_single_empty_line(tmp_path):
    result = load_buffer_from_file(tmp_path / "does_not_exist.txt")
    assert result == TupleBuffer(('',))