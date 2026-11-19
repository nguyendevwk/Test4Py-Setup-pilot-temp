import pytest
from typesystem.tokenize.tokens import Token
from typesystem.base import Position

# Create a minimal concrete subclass for testing purposes
class DummyToken(Token):
    def _get_value(self):
        return self._value

    def _get_child_token(self, key):
        # For testing, simply return self regardless of key
        return self

    def _get_key_token(self, key):
        # For testing, simply return self regardless of key
        return self

def test_string_and_position(tmp_path):
    # Prepare a content string with multiple lines
    content = "first line\nsecond line\nthird line"
    # Create a token covering "second line" (indices 11-21)
    token = DummyToken(value="second", start_index=11, end_index=21, content=content)

    # string property should return the exact slice
    assert token.string == "second line"

    # start position should be line 2, column 1 (index 11)
    assert token.start == Position(line_no=2, column_no=1, index=11)

    # end position should be line 2, column 11 (index 21)
    assert token.end == Position(line_no=2, column_no=11, index=21)

def test_lookup_and_lookup_key(tmp_path):
    # Simple content with nested structure (not parsed, just for index demonstration)
    content = "root[child][key]"
    # Token covering the whole string
    root = DummyToken(value="root", start_index=0, end_index=len(content)-1, content=content)

    # lookup should traverse indices but return the same token in this dummy implementation
    child_token = root.lookup([1])  # pretend index 1 refers to 'child'
    assert child_token is root

    # lookup_key should also return the same token
    key_token = root.lookup_key([1, 2])  # pretend indices refer to nested key
    assert key_token is root

def test_equality_and_repr(tmp_path):
    content = "abcde"
    token_a = DummyToken(value=42, start_index=1, end_index=3, content=content)
    token_b = DummyToken(value=42, start_index=1, end_index=3, content=content)
    token_c = DummyToken(value=99, start_index=1, end_index=3, content=content)

    # Equality should compare value and indices
    assert token_a == token_b
    assert token_a != token_c

    # __repr__ should include class name and string slice
    assert repr(token_a) == "DummyToken('bcd')"
