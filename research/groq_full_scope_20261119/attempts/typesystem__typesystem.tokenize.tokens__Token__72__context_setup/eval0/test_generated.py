import pytest
from typesystem.tokenize.tokens import Token
from typesystem.base import Position


class DummyToken(Token):
    """Minimal concrete implementation of Token for testing."""

    def _get_value(self):
        return self._value

    def _get_child_token(self, key):
        # For testing, return self regardless of key
        return self

    def _get_key_token(self, key):
        # For testing, return self regardless of key
        return self


def test_string_and_position():
    content = "abc\ndef\n"
    token = DummyToken(value=42, start_index=1, end_index=4, content=content)
    # string should slice from start to end inclusive
    assert token.string == "bcde"
    # start position: index 1 -> line 1, column 2
    assert token.start == Position(line_no=1, column_no=2, index=1)
    # end position: index 4 -> line 2, column 1
    assert token.end == Position(line_no=2, column_no=1, index=4)


def test_lookup_chain():
    content = "root[child][grandchild]"
    root = DummyToken(value="root", start_index=0, end_index=4, content=content)
    # lookup with empty index returns root
    assert root.lookup([]) is root
    # lookup with one key returns root (our dummy implementation)
    assert root.lookup([0]) is root
    # lookup_key should also return root
    assert root.lookup_key([0]) is root


def test_equality_and_repr():
    content = "x y z"
    t1 = DummyToken(value=10, start_index=0, end_index=0, content=content)
    t2 = DummyToken(value=10, start_index=0, end_index=0, content=content)
    t3 = DummyToken(value=20, start_index=0, end_index=0, content=content)
    # t1 and t2 should be equal
    assert t1 == t2
    # t1 and t3 should not be equal
    assert t1 != t3
    # repr should include class name and string
    assert repr(t1) == "DummyToken('x')"
