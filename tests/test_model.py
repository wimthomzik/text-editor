from text_editor.model import TupleBuffer

# insert_text — inserts text into a line at column

def test_insert_at_beginning_of_line():
    buf = TupleBuffer()
    new_buf = buf.insert_text(0, 0, 'A')
    assert new_buf.buffer[0] == 'A'
    assert len(new_buf.buffer) == 1

def test_insert_at_end_of_line():
    buf = TupleBuffer(('A',))
    new_buf = buf.insert_text(0, len(buf.buffer[0]), 'A')
    assert new_buf.buffer[0] == 'AA'
    assert len(new_buf.buffer) == 1
    
def test_insert_in_middle_of_line():
    buf = TupleBuffer(('AC',))
    new_buf = buf.insert_text(0, 1, 'B')
    assert new_buf.buffer[0] == 'ABC'
    assert len(new_buf.buffer) == 1
    
def test_insert_multi_character_text():
    buf = TupleBuffer(('',))
    new_buf = buf.insert_text(0, 0, 'ABC')
    assert new_buf.buffer[0] == 'ABC'
    assert len(new_buf.buffer) == 1
    
def test_insert_empty_string_leaves_buffer_unchanged():
    buf = TupleBuffer(('',))
    new_buf = buf.insert_text(0, 0, '')
    assert new_buf.buffer[0] == ''
    assert len(new_buf.buffer) == 1
    
def test_insert_on_middle_line_leaves_other_lines_untouched():
    buf = TupleBuffer(('A', '', 'C'))
    new_buf = buf.insert_text(1, 0, 'B')
    assert new_buf.buffer == ('A', 'B', 'C') 
    assert len(new_buf.buffer) == 3
    
def test_insert_does_not_mutate_original_buffer():
    buf = TupleBuffer(('A', '', 'C'))
    buf.insert_text(1, 0, 'B')
    assert buf.buffer == ('A', '', 'C') 
    
# split_line — splits one line into two at the column

def test_split_line_at_beginning():
    buf = TupleBuffer(('ABC',))
    new_buf = buf.split_line(0, 0)
    assert new_buf.buffer == ('', 'ABC')
    assert len(new_buf.buffer) == 2

def test_split_line_at_end():
    buf = TupleBuffer(('ABC',))
    new_buf = buf.split_line(0, 3)
    assert new_buf.buffer == ('ABC', '')
    assert len(new_buf.buffer) == 2

def test_split_line_in_middle():
    buf = TupleBuffer(('ABC',))
    new_buf = buf.split_line(0, 1)
    assert new_buf.buffer == ('A', 'BC')
    assert len(new_buf.buffer) == 2

def test_split_middle_line_leaves_other_lines_untouched():
    buf = TupleBuffer(('A', 'BC', 'D'))
    new_buf = buf.split_line(1, 1)
    assert new_buf.buffer == ('A', 'B', 'C', 'D')
    assert len(new_buf.buffer) == 4

def test_split_line_does_not_mutate_original_buffer():
    buf = TupleBuffer(('ABC',))
    buf.split_line(0, 1)
    assert buf.buffer == ('ABC',)
    
# delete_character — removes the character at the column

def test_delete_first_character():
    buf = TupleBuffer(('ABC',))
    new_buf = buf.delete_character(0, 0)
    assert new_buf.buffer == ('BC',)
    assert len(new_buf.buffer) == 1

def test_delete_last_character():
    buf = TupleBuffer(('ABC',))
    new_buf = buf.delete_character(0, 2)
    assert new_buf.buffer == ('AB',)
    assert len(new_buf.buffer) == 1

def test_delete_middle_character():
    buf = TupleBuffer(('ABC',))
    new_buf = buf.delete_character(0, 1)
    assert new_buf.buffer == ('AC',)
    assert len(new_buf.buffer) == 1

def test_delete_only_character_leaves_empty_line():
    buf = TupleBuffer(('A',))
    new_buf = buf.delete_character(0, 0)
    assert new_buf.buffer == ('',)
    assert len(new_buf.buffer) == 1

def test_delete_on_middle_line_leaves_other_lines_untouched():
    buf = TupleBuffer(('A', 'BXC', 'D'))
    new_buf = buf.delete_character(1, 1)
    assert new_buf.buffer == ('A', 'BC', 'D')
    assert len(new_buf.buffer) == 3

def test_delete_does_not_mutate_original_buffer():
    buf = TupleBuffer(('ABC',))
    buf.delete_character(0, 1)
    assert buf.buffer == ('ABC',)