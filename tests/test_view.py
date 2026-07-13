from text_editor.view import _height

def test_line_shorter_than_width():
    assert _height(35, 10) == 4
    
def test_line_shorter_than_width():
    assert _height(30, 10) == 3

def test_line_shorter_than_width():
    assert _height(0, 10) == 1