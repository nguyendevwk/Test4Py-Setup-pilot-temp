import pytest
from typesystem.tokenize.tokens import ListToken
from typesystem.base import Position

# A minimal concrete Token implementation for testing
class DummyToken:
    def __init__(self, value, start, end, content=""):
        self._value = value
        self._start_index = start
        self._end_index = end
        self._content = content

    def _get_value(self):
        return self._value

    def _get_child_token(self, key):
        raise NotImplementedError

    def _get_key_token(self, key):
        raise NotImplementedError

    def _get_position(self, index):
        return Position(1, index + 1, index)

    def __repr__(self):
        return f"DummyToken({self._value!r})"

    def __eq__(self, other):
        return isinstance(other, DummyToken) and self._value == other._value


def test_list_token_value_and_string():
    """ListToken should expose the list of child values via its value property."""
    children = [
        DummyToken(1, 0, 0),
        DummyToken(2, 1, 1),
        DummyToken(3, 2, 2),
    ]
    lt = ListToken(children, 0, 2, content="123")
    # value property should return a list of the underlying values
    assert lt.value == [1, 2, 3]
    # string property should reflect the content slice
    assert lt.string == "123"
    # start and end positions should be derived correctly
    assert lt.start == Position(1, 1, 0)
    assert lt.end == Position(1, 3, 2)


def test_list_token_lookup_and_equality():
    """Lookup should navigate to the correct child token and equality should compare values."""
    children = [
        DummyToken("a", 0, 0),
        DummyToken("b", 1, 1),
        DummyToken("c", 2, 2),
    ]
    lt = ListToken(children, 0, 2, content="abc")
    # lookup by index should return the corresponding child token
    assert lt.lookup([1]) == DummyToken("b", 1, 1)
    # equality compares underlying values and indices
    same_lt = ListToken(children, 0, 2, content="abc")
    assert lt == same_lt
    # different indices should not be equal
    different_lt = ListToken(children, 0, 1, content="ab")
    assert lt != different_lt


def test_list_token_out_of_range_lookup():
    """Accessing an out-of-range index should raise an IndexError."""
    children = [DummyToken(42, 0, 0)]
    lt = ListToken(children, 0, 0, content="42")
    with pytest.raises(IndexError):
        lt.lookup([1])  # no second element
