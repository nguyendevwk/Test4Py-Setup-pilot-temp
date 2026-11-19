import string
import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Normal case: string of requested length with allowed characters."""
    size = 10
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set(string.ascii_letters + string.digits)
    assert set(result).issubset(allowed), "Result contains disallowed characters"

def test_random_string_minimum_size():
    """Boundary case: minimal allowed size of 1."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in string.ascii_letters + string.digits

def test_random_string_invalid_inputs():
    """Error cases: non‑positive integers and non‑int types raise ValueError."""
    for bad in (0, -5, 3.14, "5", None):
        with pytest.raises(ValueError, match="size must be >= 1"):
            random_string(bad)
