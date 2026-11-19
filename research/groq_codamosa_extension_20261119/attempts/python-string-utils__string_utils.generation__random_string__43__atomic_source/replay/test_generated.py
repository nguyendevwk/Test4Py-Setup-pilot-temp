import string
import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Normal case: generated string has correct length and only allowed characters."""
    size = 15
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set(string.ascii_letters + string.digits)
    assert set(result).issubset(allowed)

def test_random_string_boundary_size_one():
    """Boundary case: size=1 returns a single allowed character."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in string.ascii_letters + string.digits

def test_random_string_invalid_size_raises_value_error():
    """Error case: non‑positive or non‑int size raises ValueError."""
    for bad_size in [0, -5, 3.14, "10"]:
        with pytest.raises(ValueError, match="size must be >= 1"):
            random_string(bad_size)
