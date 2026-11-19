import pytest
from flutils.objutils import is_list_like

def test_list_and_set_are_list_like():
    # A regular list should be recognized as list-like
    assert is_list_like([1, 2, 3]) is True
    # A set is also list-like according to the specification
    assert is_list_like({1, 2, 3}) is True
    # An empty list is still list-like
    assert is_list_like([]) is True

def test_iterator_and_keys_view_are_list_like():
    # An iterator (e.g., from reversed) should be list-like
    assert is_list_like(reversed([1, 2, 3])) is True
    # KeysView from a dict is list-like
    d = {'a': 1, 'b': 2}
    assert is_list_like(d.keys()) is True
    # ValuesView from a dict is list-like
    assert is_list_like(d.values()) is True

def test_non_list_like_objects_return_false():
    # None is explicitly not list-like
    assert is_list_like(None) is False
    # Boolean values are not list-like
    assert is_list_like(True) is False
    # Strings are not list-like
    assert is_list_like("hello") is False
    # Bytes are not list-like
    assert is_list_like(b"bytes") is False
    # A dictionary is not list-like
    assert is_list_like({'x': 1}) is False
