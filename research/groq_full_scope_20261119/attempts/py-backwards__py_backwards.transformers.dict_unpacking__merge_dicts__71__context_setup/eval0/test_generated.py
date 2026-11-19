import pytest
from py_backwards.transformers.dict_unpacking import merge_dicts

# Test 1: Normal merging of multiple dictionaries
def test_merge_dicts_normal():
    merger = merge_dicts()
    dicts = [
        {"a": 1, "b": 2},
        {"b": 3, "c": 4},
        {"d": 5}
    ]
    result = merger(dicts)
    assert result == {"a": 1, "b": 3, "c": 4, "d": 5}
    # Ensure original dictionaries are unchanged
    assert dicts[0] == {"a": 1, "b": 2}
    assert dicts[1] == {"b": 3, "c": 4}
    assert dicts[2] == {"d": 5}

# Test 2: Boundary case with an empty list of dictionaries
def test_merge_dicts_empty_list():
    merger = merge_dicts()
    result = merger([])
    assert result == {}
    # The function should not raise an exception for an empty input
    assert isinstance(result, dict)

# Test 3: Error handling when a non-dictionary is provided
def test_merge_dicts_invalid_input():
    merger = merge_dicts()
    with pytest.raises(AttributeError):
        # A list is not a dict and does not have an update method
        merger([{"a": 1}, ["not", "a", "dict"]])
