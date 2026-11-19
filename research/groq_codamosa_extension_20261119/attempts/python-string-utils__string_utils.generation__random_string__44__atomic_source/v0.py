import string
import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Verify that the returned string has the requested length and only contains allowed characters."""
    size = 15
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set(string.ascii_letters + string.digits)
    assert set(result).issubset(allowed), "Result contains disallowed characters"

def test_random_string_boundary_one():
    """Boundary test: size of 1 should return a single allowed character."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in string.ascii_letters + string.digits

def test_random_string_invalid_size_raises():
    """Error test: non‑positive or non‑int sizes should raise ValueError."""
    for bad in (0, -5, 3.5, "10"):
        with pytest.raises(ValueError, match="size must be >= 1"):
            random_string(bad)
