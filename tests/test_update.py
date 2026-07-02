from text_editor.update import _clamp, move_cursor, backspace_cursor, update
from text_editor.model import Cursor, TupleBuffer, EditorModel, Mode, Lifecycle
from text_editor.events import Direction, Arrow, Escape, Backspace, Char, Enter

def test_value_below_min_returns_min():
    assert _clamp(-1, 0, 1) == 0
    
def test_value_within_range_returns_value():
    assert _clamp(1, 0, 2) == 1
    
def test_value_above_max_returns_max():
    assert _clamp(2, 0, 1) == 1
    
def test_value_equals_min_returns_min():
    assert _clamp(0, 0, 1) == 0
    
def test_value_equals_max_returns_max():
    assert _clamp(1, 0, 1) == 1
    
def test_min_equals_max_returns_that_value():
    assert _clamp(-1, 0, 0) == 0
    
# LEFT
def test_left_mid_line_decrements_column():
    updated = move_cursor(cursor=Cursor(0, 1), direction=Direction.LEFT, buffer=TupleBuffer(('a',)))
    assert updated == Cursor(0,0)
    
def test_left_on_first_column_clamps_to_zero():
    updated = move_cursor(cursor=Cursor(0, 0), direction=Direction.LEFT, buffer=TupleBuffer(('a',)))
    assert updated == Cursor(0,0)

# RIGHT
def test_right_mid_line_increments_column():
    updated = move_cursor(cursor=Cursor(0, 0), direction=Direction.RIGHT, buffer=TupleBuffer(('a',)))
    assert updated == Cursor(0,1)
    
def test_right_on_last_column_clamps_to_line_length():
    updated = move_cursor(cursor=Cursor(0, 1), direction=Direction.RIGHT, buffer=TupleBuffer(('a',)))
    assert updated == Cursor(0,1)

# UP
def test_up_mid_buffer_decrements_line():
    updated = move_cursor(cursor=Cursor(1, 0), direction=Direction.UP, buffer=TupleBuffer(('a','b')))
    assert updated == Cursor(0,0)
    
def test_up_on_first_line_clamps_line_unchanged():
    updated = move_cursor(cursor=Cursor(0, 0), direction=Direction.UP, buffer=TupleBuffer(('a','b')))
    assert updated == Cursor(0,0)
    
def test_up_from_long_to_short_line_clamps_column_to_shorter_length():
    updated = move_cursor(cursor=Cursor(1, 2), direction=Direction.UP, buffer=TupleBuffer(('a','bc')))
    assert updated == Cursor(0,1)
    
def test_up_from_short_to_long_line_keeps_column():
    updated = move_cursor(cursor=Cursor(1, 1), direction=Direction.UP, buffer=TupleBuffer(('ab','c')))
    assert updated == Cursor(0,1)

# DOWN
def test_down_mid_buffer_increments_line():
    updated = move_cursor(cursor=Cursor(0, 0), direction=Direction.DOWN, buffer=TupleBuffer(('a','b')))
    assert updated == Cursor(1,0)

def test_down_on_last_line_clamps_line_unchanged():
    updated = move_cursor(cursor=Cursor(1, 0), direction=Direction.DOWN, buffer=TupleBuffer(('a','b')))
    assert updated == Cursor(1,0)

def test_down_from_long_to_short_line_clamps_column_to_shorter_length():
    updated = move_cursor(cursor=Cursor(0, 2), direction=Direction.DOWN, buffer=TupleBuffer(('bc','a')))
    assert updated == Cursor(1,1)

def test_down_from_short_to_long_line_keeps_column():
    updated = move_cursor(cursor=Cursor(0, 1), direction=Direction.DOWN, buffer=TupleBuffer(('c','ab')))
    assert updated == Cursor(1,1)
    
def test_backspace_at_top_left_returns_unchanged():
    updated = backspace_cursor(cursor=Cursor(0,0), buffer=TupleBuffer(('',)))
    assert updated == Cursor(0,0)
    
def test_backspace_at_line_start_returns_end_of_previous_line():
    updated = backspace_cursor(Cursor(1,0), TupleBuffer(('abc','x')))
    assert updated == Cursor(0,3)
    
def test_backspace_mid_line_decrements_column():
    updated = backspace_cursor(cursor=Cursor(0,1), buffer=TupleBuffer(('a',)))
    assert updated == Cursor(0,0)
    

def _model(lines, cursor, mode=Mode.NORMAL):
    return EditorModel(document=TupleBuffer(lines), cursor=cursor, mode=mode)

# ARROW
def test_arrow_moves_cursor():
    updated = update(_model(('a',), Cursor(0, 1)), Arrow(Direction.LEFT))
    assert updated.cursor == Cursor(0, 0)

# NORMAL
def test_normal_char_i_enters_insert_mode():
    updated = update(_model(('a',), Cursor(0, 0)), Char('i'))
    assert updated.mode is Mode.INSERT

def test_normal_char_q_sets_lifecycle_quit():
    updated = update(_model(('a',), Cursor(0, 0)), Char('q'))
    assert updated.lifecycle is Lifecycle.QUIT

def test_normal_char_hjkl_moves_cursor():
    updated = update(_model(('ab',), Cursor(0, 0)), Char('l'))
    assert updated.cursor == Cursor(0, 1)

def test_normal_char_other_returns_unchanged():
    model = _model(('a',), Cursor(0, 0))
    assert update(model, Char('z')) == model

def test_normal_escape_returns_unchanged():
    model = _model(('a',), Cursor(0, 0))
    assert update(model, Escape()) == model

def test_normal_enter_moves_cursor_down():
    updated = update(_model(('a', 'b'), Cursor(0, 0)), Enter())
    assert updated.cursor == Cursor(1, 0)

def test_normal_backspace_moves_cursor_left():
    updated = update(_model(('ab',), Cursor(0, 1)), Backspace())
    assert updated.cursor == Cursor(0, 0)

# INSERT
def test_insert_escape_returns_normal_mode():
    updated = update(_model(('a',), Cursor(0, 0), Mode.INSERT), Escape())
    assert updated.mode is Mode.NORMAL

def test_insert_char_inserts_and_advances_cursor():
    updated = update(_model(('',), Cursor(0, 0), Mode.INSERT), Char('x'))
    assert updated.document.get_line(0) == 'x'
    assert updated.cursor == Cursor(0, 1)

def test_insert_enter_splits_line():
    updated = update(_model(('ab',), Cursor(0, 1), Mode.INSERT), Enter())
    assert updated.document.line_count() == 2
    assert updated.cursor == Cursor(1, 0)

def test_insert_backspace_at_top_left_returns_unchanged():
    model = _model(('a',), Cursor(0, 0), Mode.INSERT)
    assert update(model, Backspace()) == model

def test_insert_backspace_at_line_start_merges_lines():
    updated = update(_model(('ab', 'c'), Cursor(1, 0), Mode.INSERT), Backspace())
    assert updated.document.get_line(0) == 'abc'
    assert updated.cursor == Cursor(0, 2)

def test_insert_backspace_mid_line_deletes_char():
    updated = update(_model(('abc',), Cursor(0, 2), Mode.INSERT), Backspace())
    assert updated.document.get_line(0) == 'ac'
    assert updated.cursor == Cursor(0, 1)