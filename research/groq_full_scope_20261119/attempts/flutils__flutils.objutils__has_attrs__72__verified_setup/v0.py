import pytest
from flutils.objutils import has_attrs


def test_has_attrs_all_present(tmp_path):
    """When all requested attributes exist, the function returns True."""
    d = {}
    # dict has get, keys, items, values
    assert has_attrs(d, "get", "keys", "items", "values") is True
    # UserList has append, clear, copy
    from collections import UserList
    ul = UserList([1, 2, 3])
    assert has_attrs(ul, "append", "clear", "copy") is True
    # deque has append, pop, extend
    from collections import deque
    dq = deque([1, 2, 3])
    assert has_attrs(dq, "append", "pop", "extend") is True


def test_has_attrs_missing_attribute(tmp_path):
    """If any requested attribute is missing, the function returns False."""
    d = {}
    # dict does not have 'nonexistent'
    assert has_attrs(d, "get", "nonexistent") is False
    # UserList does not have 'pop' (it has pop from list)
    from collections import UserList
    ul = UserList([1, 2, 3])
    assert has_attrs(ul, "append", "pop") is False


def test_has_attrs_invalid_attribute_name():
    """Passing a non-string attribute name raises a TypeError."""
    with pytest.raises(TypeError):
        has_attrs({}, 123)  # non-string attribute name
