import string
import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Verify that the returned string has the requested length and contains only allowed characters."""
    size = 15
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set(string.ascii_letters + string.digits)
    assert set(result).issubset(allowed), "String contains disallowed characters"

def test_random_string_boundary_minimum():
    """Test the boundary case where size is the minimum valid value (1)."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    allowed = set(string.ascii_letters + string.digits)
    assert result in allowed, "Single character not in allowed set"

def test_random_string_invalid_size_raises_value_error():
    """Ensure that invalid size arguments raise a ValueError."""
    for bad_size in [0, -5, 3.14, "10", None]:
        with pytest.raises(ValueError, match="size must be >= 1"):
            random_string(bad_size)
