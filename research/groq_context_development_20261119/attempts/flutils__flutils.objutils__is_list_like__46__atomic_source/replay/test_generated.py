import pytest
from flutils.objutils import is_list_like

def test_list_and_tuple_are_list_like():
    """Lists and tuples should be recognized as list-like."""
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like((4, 5, 6)) is True

def test_non_list_like_types_return_false():
    """Non list-like types such as bool, str, and dict should return False."""
    assert is_list_like(True) is False
    assert is_list_like("hello") is False
    assert is_list_like({"a": 1}) is False

def test_iterator_and_deque_are_list_like():
    """Iterators and deque objects should be recognized as list-like."""
    gen = (x for x in range(3))
    assert is_list_like(gen) is True
    from collections import deque
    d = deque([7, 8, 9])
    assert is_list_like(d) is True
