import pytest
from flutes.iterator import split_by

def test_split_by_criterion_basic():
    """Splits a range by a numeric criterion."""
    result = list(split_by(range(10), criterion=lambda x: x % 3 == 0))
    assert result == [[1, 2], [4, 5], [7, 8]]
    # Ensure original iterable is not consumed beyond expected
    assert result[0][0] == 1 and result[-1][-1] == 8

def test_split_by_separator_with_empty_segments():
    """Splits a string by a separator and includes empty segments."""
    text = " Split by: "
    result = list(split_by(text, empty_segments=True, separator=' '))
    # The string starts and ends with a space, so two empty segments should appear
    assert result == [[], ['S', 'p', 'l', 'i', 't'], ['b', 'y', ':'], []]
    # Verify that the middle segments contain the expected characters
    assert ''.join(result[1]) == "Split"
    assert ''.join(result[2]) == "by:"

def test_split_by_invalid_arguments_raises():
    """Providing both criterion and separator or neither should raise ValueError."""
    with pytest.raises(ValueError):
        list(split_by([1, 2, 3], criterion=lambda x: x > 1, separator='x'))
    with pytest.raises(ValueError):
        list(split_by([1, 2, 3]))
