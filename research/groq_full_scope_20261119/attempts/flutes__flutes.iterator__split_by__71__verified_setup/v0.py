import pytest
from flutes.iterator import split_by

def test_split_by_criterion_basic():
    """Splits a range by a numeric criterion."""
    result = list(split_by(range(10), criterion=lambda x: x % 3 == 0))
    assert result == [[1, 2], [4, 5], [7, 8]]
    # Ensure that the original iterable is not consumed prematurely
    assert list(split_by(range(3), criterion=lambda x: x == 1)) == [[0], [2]]

def test_split_by_separator_empty_segments():
    """Splits a string by a separator and includes empty segments."""
    text = " Split by: "
    result = list(split_by(text, empty_segments=True, separator=' '))
    # The string starts and ends with a space, so we expect leading and trailing empty lists
    assert result == [[], ['S', 'p', 'l', 'i', 't'], ['b', 'y', ':'], []]
    # Verify that no characters are lost
    flattened = [c for sub in result for c in sub]
    assert flattened == list(text.strip())

def test_split_by_invalid_arguments():
    """Raises ValueError when neither or both arguments are provided."""
    with pytest.raises(ValueError):
        list(split_by([1, 2, 3]))  # neither criterion nor separator
    with pytest.raises(ValueError):
        list(split_by([1, 2, 3], criterion=lambda x: x > 0, separator='x'))  # both provided
