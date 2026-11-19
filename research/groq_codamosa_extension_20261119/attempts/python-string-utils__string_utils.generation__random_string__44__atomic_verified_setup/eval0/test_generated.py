import string
import re
import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Verify that the function returns a string of the requested length
    and that all characters belong to the allowed set."""
    size = 15
    result = random_string(size)
    assert isinstance(result, str), "Result should be a string"
    assert len(result) == size, f"Expected length {size}, got {len(result)}"
    allowed = set(string.ascii_letters + string.digits)
    assert set(result).issubset(allowed), "Result contains disallowed characters"

def test_random_string_boundary_minimum():
    """Test the boundary case where size is 1."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in string.ascii_letters + string.digits

def test_random_string_invalid_input_raises_value_error():
    """Ensure that non-positive or non-integer sizes raise ValueError."""
    for bad in [0, -5, 3.14, "10", None]:
        with pytest.raises(ValueError):
            random_string(bad)
