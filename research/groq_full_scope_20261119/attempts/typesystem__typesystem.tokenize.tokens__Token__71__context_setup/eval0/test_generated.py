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


def test_string_property_and_position(tmp_path):
    content = "abc\ndef\n"
    # Token covering 'bcd' (indices 1-3)
    token = DummyToken(value="bcd", start_index=1, end_index=3, content=content)

    # string property should slice correctly
    assert token.string == "bcd"

    # start position should be line 1, column 2 (index 1)
    assert token.start == Position(line_no=1, column_no=2, index=1)

    # end position should be line 1, column 4 (index 3)
    assert token.end == Position(line_no=1, column_no=4, index=3)


def test_equality_and_repr(tmp_path):
    content = "xyz"
    token_a = DummyToken(value="x", start_index=0, end_index=0, content=content)
    token_b = DummyToken(value="x", start_index=0, end_index=0, content=content)
    token_c = DummyToken(value="y", start_index=1, end_index=1, content=content)

    # Equality should compare value and indices
    assert token_a == token_b
    assert token_a != token_c

    # __repr__ should include class name and string
    assert repr(token_a) == "DummyToken('x')"


def test_position_calculation_across_lines(tmp_path):
    content = "line1\nline2\nline3"
    # Token covering 'e2' in 'line2' (indices 6-7)
    token = DummyToken(value="e2", start_index=6, end_index=7, content=content)

    # start position should be line 2, column 2 (index 6)
    assert token.start == Position(line_no=2, column_no=2, index=6)

    # end position should be line 2, column 3 (index 7)
    assert token.end == Position(line_no=2, column_no=3, index=7)
