import pytest
from flutils.namedtupleutils import to_namedtuple
from collections import OrderedDict
from types import SimpleNamespace

def test_dict_to_namedtuple_sorted_and_recursive(tmp_path):
    # Nested dict with non‑identifier key and list value
    data = {
        'b': 2,
        'a': {'c': 3, 'd': [4, 5]},
        'invalid-key': 99  # not a valid identifier
    }
    result = to_namedtuple(data)
    # Attributes should be sorted alphabetically and exclude invalid key
    assert hasattr(result, 'a')
    assert hasattr(result, 'b')
    assert not hasattr(result, 'invalid-key')
    # Recursive conversion
    assert hasattr(result.a, 'c')
    assert hasattr(result.a, 'd')
    assert isinstance(result.a.d, list)
    assert result.a.d == [4, 5]
    # Original dict unchanged
    assert data['a']['c'] == 3

def test_list_and_ordereddict_conversion(tmp_path):
    # List containing a dict and an OrderedDict
    lst = [{'x': 1}, OrderedDict([('y', 2), ('z', 3)])]
    result = to_namedtuple(lst)
    # Result should be a list with converted elements
    assert isinstance(result, list)
    assert isinstance(result[0], type)
    assert isinstance(result[1], type)
    # OrderedDict preserves order in the namedtuple
    assert result[1]._fields == ('y', 'z')
    # List elements remain separate objects
    assert result[0] is not lst[0]
    assert result[1] is not lst[1]

def test_invalid_identifier_raises(tmp_path):
    # SimpleNamespace with an attribute starting with underscore
    ns = SimpleNamespace(_private=42, public=7)
    with pytest.raises(ValueError):
        to_namedtuple(ns)
