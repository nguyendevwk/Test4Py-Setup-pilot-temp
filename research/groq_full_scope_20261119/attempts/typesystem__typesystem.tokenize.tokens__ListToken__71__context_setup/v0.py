import pytest
from typesystem.tokenize.tokens import ListToken
from typesystem.base import Position

# Simple concrete Token implementation for testing
class DummyToken:
    def __init__(self, value, start_index, end_index, content=""):
        self._value = value
        self._start_index = start_index
        self._end_index = end_index
        self._content = content

    def _get_value(self):
        return self._value

    def _get_child_token(self, key):
        raise NotImplementedError

    def _get_key_token(self, key):
        raise NotImplementedError

    @property
    def string(self):
        return self._content[self._start_index : self._end_index + 1]

    @property
    def value(self):
        return self._get_value()

    @property
    def start(self):
        return Position(self._start_index, 1, self._start_index)

    @property
    def end(self):
        return Position(self._end_index, 1, self._end_index)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.string!r})"

    def __eq__(self, other):
        return isinstance(other, DummyToken) and self._value == other._value


def test_list_token_value_and_repr():
    """ListToken should expose the underlying values and have a useful repr."""
    t1 = DummyToken("a", 0, 0)
    t2 = DummyToken("b", 2, 2)
    lt = ListToken([t1, t2], 0, 2)
    assert lt.value == ["a", "b"]
    assert repr(lt) == "ListToken('a b')"


def test_list_token_lookup_success_and_boundary():
    """lookup should return the correct child token and raise IndexError on out‑of‑range."""
    t1 = DummyToken("x", 0, 0)
    t2 = DummyToken("y", 2, 2)
    lt = ListToken([t1, t2], 0, 2)
    # Successful lookup
    assert lt.lookup([0]) is t1
    assert lt.lookup([1]) is t2
    # Boundary: last valid index
    assert lt.lookup([1]) is t2
    # Out of range should raise
    with pytest.raises(IndexError):
        lt.lookup([2])


def test_list_token_start_end_positions():
    """start and end properties should return correct Position objects."""
    t1 = DummyToken("foo", 0, 2)
    t2 = DummyToken("bar", 4, 6)
    lt = ListToken([t1, t2], 0, 6)
    assert lt.start == Position(1, 1, 0)
    assert lt.end == Position(1, 1, 6)
