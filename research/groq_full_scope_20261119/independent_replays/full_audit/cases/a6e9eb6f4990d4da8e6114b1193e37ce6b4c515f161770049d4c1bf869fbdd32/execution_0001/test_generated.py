import pytest
from flutes.iterator import split_by

def test_split_by_criterion_basic():
    """Splits a range by a numeric criterion."""
    result = list(split_by(range(10), criterion=lambda x: x % 3 == 0))
    assert result == [[1, 2], [4, 5], [7, 8]]
    # Ensure that the original iterable is not consumed more than once
    assert list(split_by(range(10), criterion=lambda x: x % 3 == 0)) == result

def test_split_by_separator_with_empty_segments(tmp_path):
    """Splits a string by a separator and includes empty segments."""
    text = " Split by: "
    # Use a separator that appears at both ends and in the middle
    result = list(split_by(text, empty_segments=True, separator=' '))
    # Expected: empty before first space, words between spaces, empty after last space
    assert result == [[], ['S', 'p', 'l', 'i', 't'], ['b', 'y', ':'], []]
    # Verify that the function can be called again with the same arguments
    assert list(split_by(text, empty_segments=True, separator=' ')) == result

def test_split_by_invalid_arguments():
    """Raises ValueError when neither or both arguments are provided."""
    with pytest.raises(ValueError, match="Exactly one of `criterion` and `separator`"):
        list(split_by([1, 2, 3], criterion=None, separator=None))
    with pytest.raises(ValueError, match="Exactly one of `criterion` and `separator`"):
        list(split_by([1, 2, 3], criterion=lambda x: x > 0, separator='x'))
