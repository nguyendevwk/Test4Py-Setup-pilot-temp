import pytest
from flutes.iterator import split_by

def test_split_by_criterion_basic():
    # Split numbers by divisibility by 3
    result = list(split_by(range(10), criterion=lambda x: x % 3 == 0))
    assert result == [[1, 2], [4, 5], [7, 8]]
    # Ensure that the original iterable is not modified
    assert list(range(10)) == list(range(10))

def test_split_by_separator_with_empty_segments():
    # Split a string by '.' and include empty segments
    text = " Split by: "
    result = list(split_by(text, empty_segments=True, separator='.'))
    assert result == [[], ['S', 'p', 'l', 'i', 't'], ['b', 'y', ':'], []]
    # Verify that the separator itself is not present in any sub-list
    for segment in result:
        assert '.' not in segment

def test_split_by_invalid_arguments_raises():
    # Exactly one of criterion or separator must be provided
    with pytest.raises(ValueError):
        list(split_by([1, 2, 3]))
    with pytest.raises(ValueError):
        list(split_by([1, 2, 3], criterion=lambda x: x > 0, separator='x'))
