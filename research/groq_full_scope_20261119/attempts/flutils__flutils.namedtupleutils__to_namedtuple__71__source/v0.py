import pytest
from collections import OrderedDict, namedtuple
from types import SimpleNamespace
from flutils.namedtupleutils import to_namedtuple

def test_dict_to_namedtuple_and_attribute_access():
    data = {"alpha": 1, "beta": 2}
    nt = to_namedtuple(data)
    # The result should be a NamedTuple with attributes alpha and beta
    assert isinstance(nt, tuple) and hasattr(nt, "_fields")
    assert nt._fields == ("alpha", "beta")
    assert nt.alpha == 1
    assert nt.beta == 2
    # Ensure original dict is unchanged
    assert data == {"alpha": 1, "beta": 2}

def test_nested_list_and_dict_conversion():
    nested = [1, {"x": 10, "y": [20, {"z": 30}]}]
    result = to_namedtuple(nested)
    # Top level should be a list
    assert isinstance(result, list)
    assert result[0] == 1
    # Second element should be a NamedTuple
    nt = result[1]
    assert isinstance(nt, tuple) and hasattr(nt, "_fields")
    assert nt._fields == ("x", "y")
    assert nt.x == 10
    # y should be a list with a NamedTuple inside
    assert isinstance(nt.y, list)
    assert nt.y[0] == 20
    inner_nt = nt.y[1]
    assert isinstance(inner_nt, tuple) and hasattr(inner_nt, "_fields")
    assert inner_nt._fields == ("z",)
    assert inner_nt.z == 30

def test_invalid_identifier_raises_value_error():
    # Keys starting with underscore should raise ValueError
    bad_dict = {"_private": 42, "valid": 1}
    with pytest.raises(ValueError):
        to_namedtuple(bad_dict)
