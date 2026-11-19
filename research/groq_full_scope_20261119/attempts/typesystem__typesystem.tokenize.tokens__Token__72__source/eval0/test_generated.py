import pytest
from typesystem.tokenize.tokens import Token
from typesystem.base import Position


class DummyToken(Token):
    """A minimal concrete implementation of Token for testing purposes."""

    def _get_value(self):
        return self._value

    def _get_child_token(self, key):
        # For testing, simply return self regardless of key
        return self

    def _get_key_token(self, key):
        # For testing, simply return self regardless of key
        return self


def test_string_and_position():
    content = "abc def\nghi"
    token = DummyToken(value=42, start_index=4, end_index=6, content=content)
    # string should slice from start to end inclusive
    assert token.string == "def"
    # start position should be line 1, column 5 (index 4)
    assert token.start == Position(line_no=1, column_no=5, index=4)
    # end position should be line 1, column 7 (index 6)
    assert token.end == Position(line_no=1, column_no=7, index=6)


def test_lookup_and_lookup_key():
    content = "x:y:z"
    token = DummyToken(value="root", start_index=0, end_index=4, content=content)
    # lookup should traverse keys but return the same token in this dummy implementation
    child = token.lookup([1, 2])
    assert child is token
    # lookup_key should also return the same token
    key_token = token.lookup_key([1, 2])
    assert key_token is token


def test_equality_and_repr():
    content = "hello"
    t1 = DummyToken(value="hi", start_index=0, end_index=4, content=content)
    t2 = DummyToken(value="hi", start_index=0, end_index=4, content=content)
    t3 = DummyToken(value="bye", start_index=0, end_index=4, content=content)
    # t1 and t2 should be equal
    assert t1 == t2
    # t1 and t3 should not be equal
    assert t1 != t3
    # repr should include class name and string representation
    assert repr(t1) == "DummyToken('hello')"
