import pytest
from flutils.objutils import is_list_like
from collections import UserList, deque, Counter, defaultdict
from collections.abc import Iterator, KeysView, ValuesView
from typing import Any

def test_is_list_like_with_various_iterables():
    # List-like objects should return True
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like((4, 5)) is True
    assert is_list_like({6, 7}) is True
    assert is_list_like(frozenset([8, 9])) is True
    assert is_list_like(deque([10, 11])) is True
    assert is_list_like(UserList([12, 13])) is True
    assert is_list_like(iter([14, 15])) is True
    assert is_list_like(dict.fromkeys([16, 17]).keys()) is True
    assert is_list_like(dict.fromkeys([18, 19]).values()) is True

def test_is_list_like_with_empty_and_non_iterables():
    # Empty containers are still list-like
    assert is_list_like([]) is True
    assert is_list_like(()) is True
    assert is_list_like(set()) is True
    assert is_list_like(frozenset()) is True
    assert is_list_like(deque()) is True
    # Non-iterables or non-list-like iterables should be False
    assert is_list_like(None) is False
    assert is_list_like(True) is False
    assert is_list_like(b"bytes") is False
    assert is_list_like("string") is False
    assert is_list_like(42) is False
    assert is_list_like(3.14) is False
    assert is_list_like(dict()) is False
    assert is_list_like(Counter()) is False
    assert is_list_like(defaultdict()) is False

def test_is_list_like_with_custom_objects_and_edge_cases():
    class CustomIterable:
        def __iter__(self):
            return iter([1, 2, 3])

    class CustomNonIterable:
        pass

    # Custom iterable should be considered list-like
    assert is_list_like(CustomIterable()) is True
    # Custom non-iterable should not
    assert is_list_like(CustomNonIterable()) is False
    # Ensure that passing a generator expression returns True
    assert is_list_like((x for x in range(3))) is True
    # Passing a function object should return False
    def sample_func(): pass
    assert is_list_like(sample_func) is False
