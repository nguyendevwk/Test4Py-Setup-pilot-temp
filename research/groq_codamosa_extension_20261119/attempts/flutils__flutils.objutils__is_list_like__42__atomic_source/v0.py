import pytest
from flutils.objutils import is_list_like

def test_is_list_like_with_various_iterables():
    # List-like objects should return True
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like((1, 2, 3)) is True
    assert is_list_like({1, 2, 3}) is True
    assert is_list_like(frozenset([1, 2, 3])) is True
    assert is_list_like(deque([1, 2, 3])) is True
    assert is_list_like(iter([1, 2, 3])) is True
    # Non list-like objects should return False
    assert is_list_like("hello") is False
    assert is_list_like(42) is False
    assert is_list_like(None) is False
    assert is_list_like(True) is False
    assert is_list_like(b"bytes") is False

def test_is_list_like_with_empty_and_singleton():
    # Empty list and empty tuple should be list-like
    assert is_list_like([]) is True
    assert is_list_like(()) is True
    # Empty set and frozenset should be list-like
    assert is_list_like(set()) is True
    assert is_list_like(frozenset()) is True
    # Single element list should be list-like
    assert is_list_like([42]) is True

def test_is_list_like_with_non_iterable_and_edge_cases():
    # Objects that are not iterable or are special types should be False
    class Dummy:
        pass
    dummy = Dummy()
    assert is_list_like(dummy) is False
    # A generator expression is an iterator and should be list-like
    assert is_list_like((x for x in range(3))) is True
    # A string is iterable but not list-like
    assert is_list_like("abc") is False
