import pytest
from typesystem.tokenize.tokens import Token
from typesystem.base import Position


class DummyToken(Token):
    """Concrete implementation of Token for testing purposes."""

    def _get_value(self):
        return self._value

    def _get_child_token(self, key):
        # For testing, simply return self regardless of key
        return self

    def _get_key_token(self, key):
        # For testing, simply return self regardless of key
        return self


def test_string_and_position(tmp_path):
    content = "abc\ndef\n"
    token = DummyToken(value=42, start_index=1, end_index=4, content=content)
    # string should slice from start_index to end_index inclusive
    assert token.string == "bcde"
    # start position: index 1 -> line 1, column 2
    assert token.start == Position(line_no=1, column_no=2, index=1)
    # end position: index 4 -> line 2, column 1
    assert token.end == Position(line_no=2, column_no=1, index=4)


def test_lookup_and_lookup_key(tmp_path):
    content = "root"
    token = DummyToken(value="root", start_index=0, end_index=3, content=content)
    # lookup should return the same token for any key
    child = token.lookup([0, 1])
    assert child is token
    # lookup_key should also return the same token
    key_token = token.lookup_key([0])
    assert key_token is token


def test_equality_and_repr(tmp_path):
    content = "xyz"
    token_a = DummyToken(value="a", start_index=0, end_index=2, content=content)
    token_b = DummyToken(value="a", start_index=0, end_index=2, content=content)
    token_c = DummyToken(value="b", start_index=0, end_index=2, content=content)
    # tokens with same value and indices are equal
    assert token_a == token_b
    # different value leads to inequality
    assert token_a != token_c
    # repr should include class name and string
    assert repr(token_a) == "DummyToken('xyz')"
