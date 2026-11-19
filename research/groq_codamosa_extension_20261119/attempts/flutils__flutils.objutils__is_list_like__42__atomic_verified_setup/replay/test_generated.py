import pytest
from collections import UserList, deque
from collections.abc import KeysView, ValuesView
from flutils.objutils import is_list_like

def test_is_list_like_with_various_list_like_objects():
    # List-like objects that should return True
    assert is_list_like([1, 2, 3]) is True
    assert is_list_like((4, 5)) is True
    assert is_list_like({6, 7}) is True
    assert is_list_like(frozenset([8, 9])) is True
    assert is_list_like(deque([10, 11])) is True
    assert is_list_like(UserList([12, 13])) is True
    assert is_list_like(iter([14, 15])) is True
    assert is_list_like({16: 'a'}.keys()) is True
    assert is_list_like({17: 'b'}.values()) is True

def test_is_list_like_with_empty_and_boundary_objects():
    # Empty containers should still be considered list-like
    assert is_list_like([]) is True
    assert is_list_like(()) is True
    assert is_list_like(set()) is True
    assert is_list_like(frozenset()) is True
    assert is_list_like(deque()) is True
    # Iterator over an empty list
    assert is_list_like(iter([])) is True

def test_is_list_like_with_non_list_like_objects():
    # Non-list-like objects should return False
    assert is_list_like(None) is False
    assert is_list_like(True) is False
    assert is_list_like(False) is False
    assert is_list_like(42) is False
    assert is_list_like(3.14) is False
    assert is_list_like("hello") is False
    assert is_list_like(b"bytes") is False
    # Dict is explicitly excluded
    assert is_list_like({"key": "value"}) is False
