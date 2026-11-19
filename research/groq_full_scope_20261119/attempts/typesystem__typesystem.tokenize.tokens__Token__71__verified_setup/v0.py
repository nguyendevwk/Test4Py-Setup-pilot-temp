import pytest
from typesystem.tokenize.tokens import Token
from typesystem.base import Position


class DummyToken(Token):
    """Concrete implementation of Token for testing purposes."""

    def _get_value(self):
        return self._value

    def _get_child_token(self, key):
        raise NotImplementedError

    def _get_key_token(self, key):
        raise NotImplementedError


def test_string_and_position_basic():
    content = "abc def\nghi"
    # token covering "def" (indices 4-6)
    token = DummyToken(value="def", start_index=4, end_index=6, content=content)

    # string property should slice correctly
    assert token.string == "def"

    # start position should be line 1, column 5 (0-based index 4)
    assert token.start == Position(line_no=1, column_no=5, index=4)

    # end position should be line 1, column 7 (index 6)
    assert token.end == Position(line_no=1, column_no=7, index=6)


def test_equality_and_repr():
    content = "x y z"
    t1 = DummyToken(value=42, start_index=0, end_index=0, content=content)
    t2 = DummyToken(value=42, start_index=0, end_index=0, content=content)
    t3 = DummyToken(value=99, start_index=0, end_index=0, content=content)

    # t1 and t2 should be equal (same value and indices)
    assert t1 == t2
    # t1 and t3 should not be equal (different value)
    assert t1 != t3

    # __repr__ should include class name and string
    assert repr(t1) == "DummyToken('x')"


def test_position_across_newlines():
    content = "line1\nline2\nline3"
    # token covering "line2" (indices 6-10)
    token = DummyToken(value="line2", start_index=6, end_index=10, content=content)

    # start should be line 2, column 1
    assert token.start == Position(line_no=2, column_no=1, index=6)

    # end should be line 2, column 5
    assert token.end == Position(line_no=2, column_no=5, index=10)
