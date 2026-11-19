import string
import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Normal case: verify length and allowed characters."""
    size = 10
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set(string.ascii_letters + string.digits)
    assert set(result).issubset(allowed)

def test_random_string_minimum_size():
    """Boundary case: size=1 should return a single allowed character."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in string.ascii_letters + string.digits

def test_random_string_invalid_inputs():
    """Error case: non‑positive or non‑int sizes raise ValueError."""
    with pytest.raises(ValueError):
        random_string(0)
    with pytest.raises(ValueError):
        random_string(-5)
    with pytest.raises(ValueError):
        random_string(3.14)
    with pytest.raises(ValueError):
        random_string("5")
