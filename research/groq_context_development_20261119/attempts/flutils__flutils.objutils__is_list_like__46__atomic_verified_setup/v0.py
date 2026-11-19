import pytest
from collections import deque, UserList, KeysView, ValuesView
from flutils.objutils import is_list_like


def test_is_list_like_with_various_list_like_objects():
    """Verify that known list‑like objects return True."""
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like(set([1, 2])) is True
    assert is_list_like(frozenset([1, 2])) is True
    assert is_list_like((1, 2, 3)) is True
    assert is_list_like(deque([1, 2, 3])) is True
    assert is_list_like(UserList([1, 2, 3])) is True
    assert is_list_like(iter([1, 2, 3])) is True
    assert is_list_like(dict(a=1).keys()) is True
    assert is_list_like(dict(a=1).values()) is True


def test_is_list_like_boundary_empty_tuple_and_deque():
    """Check boundary cases: empty tuple and empty deque."""
    assert is_list_like(()) is True
    assert is_list_like(deque()) is True


def test_is_list_like_non_list_like_objects():
    """Ensure that non‑list‑like objects return False."""
    assert is_list_like(None) is False
    assert is_list_like(True) is False
    assert is_list_like(b"bytes") is False
    assert is_list_like(42) is False
    assert is_list_like("string") is False
    assert is_list_like(3.14) is False
