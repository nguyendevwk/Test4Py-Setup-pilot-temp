import pytest
from flutes.iterator import split_by

def test_split_by_criterion_basic():
    """Splits a range by a numeric criterion."""
    result = list(split_by(range(10), criterion=lambda x: x % 3 == 0))
    assert result == [[1, 2], [4, 5], [7, 8]]
    # Ensure no empty segments are included by default
    assert all(len(seg) > 0 for seg in result)

def test_split_by_separator_with_empty_segments(tmp_path):
    """Splits a string by a separator and includes empty segments."""
    text = " Split by: "
    # Use a separator that appears at the start and end
    result = list(split_by(text, empty_segments=True, separator=' '))
    # Expected: empty before first space, words, empty after last space
    assert result == [[], ['S', 'p', 'l', 'i', 't'], ['b', 'y', ':'], []]
    # Verify that the number of segments matches the number of separators + 1
    assert len(result) == text.count(' ') + 1

def test_split_by_invalid_arguments():
    """Raises ValueError when neither or both arguments are provided."""
    with pytest.raises(ValueError):
        list(split_by([1, 2, 3]))  # neither criterion nor separator
    with pytest.raises(ValueError):
        list(split_by([1, 2, 3], criterion=lambda x: x > 0, separator='x'))  # both provided
