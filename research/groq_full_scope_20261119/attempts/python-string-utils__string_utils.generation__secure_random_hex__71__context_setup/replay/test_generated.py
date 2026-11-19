import os
import binascii
import pytest
from string_utils.generation import secure_random_hex

def test_secure_random_hex_length_and_characters():
    """The function should return a hex string of length 2 * byte_count."""
    byte_count = 16
    hex_str = secure_random_hex(byte_count)
    assert isinstance(hex_str, str)
    assert len(hex_str) == 2 * byte_count
    # All characters must be valid hexadecimal digits
    assert all(c in "0123456789abcdef" for c in hex_str)

def test_secure_random_hex_boundary_value():
    """The function should work for the smallest valid byte_count (1)."""
    hex_str = secure_random_hex(1)
    assert len(hex_str) == 2
    # The string should be a valid hex representation of a single byte
    byte_value = int(hex_str, 16)
    assert 0 <= byte_value <= 255

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
