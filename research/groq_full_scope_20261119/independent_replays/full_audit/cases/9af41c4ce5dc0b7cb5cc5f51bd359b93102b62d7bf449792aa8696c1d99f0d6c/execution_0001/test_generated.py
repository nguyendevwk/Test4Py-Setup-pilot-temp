import pytest
from flutes.iterator import split_by

def test_split_by_criterion_basic():
    """Splits a range by a numeric criterion."""
    result = list(split_by(range(10), criterion=lambda x: x % 3 == 0))
    assert result == [[1, 2], [4, 5], [7, 8]]

def test_split_by_separator_empty_segments():
    """Includes empty segments when two separators are adjacent."""
    text = " Split by: "
    # separator is a space, empty_segments=True
    result = list(split_by(text, empty_segments=True, separator=' '))
    # Expected: leading empty, words split by spaces, trailing empty
    assert result == [[], ['S', 'p', 'l', 'i', 't'], ['b', 'y', ':'], []]

def test_split_by_invalid_arguments():
    """Raises ValueError when neither or both arguments are provided."""
    with pytest.raises(ValueError):
        # Neither criterion nor separator
        list(split_by([1, 2, 3]))
    with pytest.raises(ValueError):
        # Both criterion and separator
        list(split_by([1, 2, 3], criterion=lambda x: x > 1, separator=2))
