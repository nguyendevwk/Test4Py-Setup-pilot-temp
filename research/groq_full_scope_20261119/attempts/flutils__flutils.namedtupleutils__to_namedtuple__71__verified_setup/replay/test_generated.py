import pytest
from collections import OrderedDict, namedtuple
from types import SimpleNamespace
from flutils.namedtupleutils import to_namedtuple

def test_dict_to_namedtuple_and_attribute_access():
    data = {"alpha": 1, "beta": 2}
    nt = to_namedtuple(data)
    # The result should be a NamedTuple with attributes sorted alphabetically
    assert isinstance(nt, tuple) and hasattr(nt, "_fields")
    assert nt._fields == ("alpha", "beta")
    assert nt.alpha == 1
    assert nt.beta == 2
    # Original dict remains unchanged
    assert data == {"alpha": 1, "beta": 2}

def test_list_with_nested_dict_and_ordered_dict():
    nested = OrderedDict([("x", 10), ("y", 20)])
    lst = [nested, {"a": 1, "b": 2}]
    result = to_namedtuple(lst)
    # The outer list should be preserved
    assert isinstance(result, list)
    # First element is a NamedTuple preserving order
    first = result[0]
    assert isinstance(first, tuple)
    assert first._fields == ("x", "y")
    assert first.x == 10 and first.y == 20
    # Second element is a NamedTuple with sorted fields
    second = result[1]
    assert isinstance(second, tuple)
    assert second._fields == ("a", "b")
    assert second.a == 1 and second.b == 2

def test_invalid_identifier_raises_value_error():
    # Keys starting with underscore should be ignored, not raise
    data = {"_hidden": 5, "visible": 10}
    nt = to_namedtuple(data)
    assert hasattr(nt, "visible") and not hasattr(nt, "_hidden")
    # However, if a key is not a valid identifier at all, it should be ignored
    data_invalid = {"123": 7, "valid": 8}
    nt_invalid = to_namedtuple(data_invalid)
    assert hasattr(nt_invalid, "valid") and not hasattr(nt_invalid, "123")
    # Ensure that no exception is raised for invalid identifiers
    try:
        to_namedtuple({"_bad": 1, "good": 2})
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")
