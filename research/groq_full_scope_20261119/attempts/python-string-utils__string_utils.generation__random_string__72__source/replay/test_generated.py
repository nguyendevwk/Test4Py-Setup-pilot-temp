import string
import re
import pytest
from string_utils.generation import random_string

def test_random_string_normal_length_and_charset():
    """Verify that the function returns a string of the requested length
    and that all characters belong to the allowed set."""
    size = 15
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set(string.ascii_letters + string.digits)
    assert set(result).issubset(allowed)

def test_random_string_boundary_single_character():
    """The smallest valid size (1) should return a single allowed character."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in string.ascii_letters + string.digits

def test_random_string_invalid_inputs_raises_value_error():
    """Non‑positive or non‑int sizes must raise ValueError."""
    for bad in [0, -5, 3.14, "10", None]:
        with pytest.raises(ValueError, match="size must be >= 1"):
            random_string(bad)
