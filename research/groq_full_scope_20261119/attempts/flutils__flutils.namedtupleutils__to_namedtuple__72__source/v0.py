import pytest
from collections import OrderedDict, namedtuple
from types import SimpleNamespace
from flutils.namedtupleutils import to_namedtuple

def test_dict_to_namedtuple_sorted_and_filtered():
    # Keys that are valid identifiers become attributes; invalid ones are ignored
    data = {"valid": 1, "_private": 2, "another": 3}
    result = to_namedtuple(data)
    # Result should be a NamedTuple with attributes sorted alphabetically
    assert hasattr(result, "valid") and result.valid == 1
    assert hasattr(result, "another") and result.another == 3
    assert not hasattr(result, "_private")
    # Order of fields in the NamedTuple should be alphabetical
    expected_fields = ("another", "valid")
    assert result._fields == expected_fields

def test_list_with_nested_dict_and_tuple():
    # Nested structures should be recursively converted
    nested = {"x": [1, {"y": 2}], "z": (3, 4)}
    result = to_namedtuple(nested)
    # Outer should be a NamedTuple
    assert isinstance(result, namedtuple("Anonymous", ("x", "z")))
    # 'x' should be a list with first element int and second a NamedTuple
    assert isinstance(result.x, list)
    assert result.x[0] == 1
    assert isinstance(result.x[1], namedtuple("Anonymous", ("y",)))
    assert result.x[1].y == 2
    # 'z' should be a tuple of ints
    assert isinstance(result.z, tuple)
    assert result.z == (3, 4)

def test_invalid_identifier_raises_value_error():
    # Keys that are not valid identifiers should raise ValueError
    invalid_data = {"1invalid": 10}
    with pytest.raises(ValueError):
        to_namedtuple(invalid_data)
