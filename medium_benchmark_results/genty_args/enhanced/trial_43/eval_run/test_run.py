import pytest
from genty.genty_args import genty_args

def test_genty_args_iteration_and_properties():
    # Arrange: create GentyArgs with mixed positional and keyword arguments
    args_obj = genty_args(1, 'two', 3.0, key1='val', key2='another', key3=5)

    # Assert: args and kwargs properties return the original values
    assert args_obj.args == (1, 'two', 3.0)
    assert args_obj.kwargs == {'key1': 'val', 'key2': 'another', 'key3': 5}

    # Act: iterate over the object to get formatted representations
    formatted = list(args_obj)

    # Expected formatted strings:
    # - Positional args: 1 -> '1', 'two' -> "'two'", 3.0 -> '3.0'
    # - Keyword args sorted by key: key1='val', key2='another', key3=5
    expected = ['1', "'two'", '3.0', "key1='val'", "key2='another'", 'key3=5']

    # Assert: iteration yields the expected formatted list
    assert formatted == expected
