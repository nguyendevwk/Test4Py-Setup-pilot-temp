import os
import binascii
import pytest
from string_utils.generation import secure_random_hex

def test_secure_random_hex_length_and_hex_chars():
    """The function should return a hex string of length 2 * byte_count."""
    byte_count = 10
    result = secure_random_hex(byte_count)
    assert isinstance(result, str)
    assert len(result) == 2 * byte_count
    # All characters must be valid hex digits
    assert all(c in "0123456789abcdef" for c in result)

def test_secure_random_hex_minimum_byte_count():
    """When byte_count is 1, the result should be a 2-character hex string."""
    result = secure_random_hex(1)
    assert isinstance(result, str)
    assert len(result) == 2
    assert all(c in "0123456789abcdef" for c in result)

def test_secure_random_hex_invalid_input_raises_value_error():
    """The function should raise ValueError for non-positive or non-integer inputs."""
    with pytest.raises(ValueError):
        secure_random_hex(0)
    with pytest.raises(ValueError):
        secure_random_hex(-5)
    with pytest.raises(ValueError):
        secure_random_hex(3.14)
    with pytest.raises(ValueError):
        secure_random_hex("10")
