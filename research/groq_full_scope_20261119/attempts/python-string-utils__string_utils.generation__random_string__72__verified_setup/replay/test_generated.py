import string
import re
import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Verify that the function returns a string of the requested length
    and that all characters belong to the allowed set."""
    size = 15
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set(string.ascii_letters + string.digits)
    assert all(ch in allowed for ch in result)

def test_random_string_boundary_value():
    """Check that the minimal valid size (1) returns a single allowed character."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in string.ascii_letters + string.digits

def test_random_string_invalid_input_raises_value_error():
    """Ensure that non‑positive or non‑int sizes raise ValueError."""
    with pytest.raises(ValueError):
        random_string(0)
    with pytest.raises(ValueError):
        random_string(-5)
    with pytest.raises(ValueError):
        random_string(3.5)
    with pytest.raises(ValueError):
        random_string("10")
