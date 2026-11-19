import os
import binascii
import pytest
from string_utils.generation import secure_random_hex

def test_secure_random_hex_length_and_characters():
    """The returned string should be twice the byte count and contain only hex digits."""
    byte_count = 16
    hex_str = secure_random_hex(byte_count)
    assert isinstance(hex_str, str)
    assert len(hex_str) == byte_count * 2
    # All characters must be valid hex digits
    assert all(c in "0123456789abcdef" for c in hex_str)

def test_secure_random_hex_randomness():
    """Multiple calls should produce different results, indicating randomness."""
    byte_count = 8
    results = {secure_random_hex(byte_count) for _ in range(10)}
    # With 8 bytes there are 2^64 possible values; collisions are astronomically unlikely
    assert len(results) > 1
    # Ensure each result is unique
    assert len(results) == 10

def test_secure_random_hex_invalid_input():
    """Providing a non‑positive or non‑int byte_count should raise ValueError."""
    with pytest.raises(ValueError):
        secure_random_hex(0)
    with pytest.raises(ValueError):
        secure_random_hex(-5)
    with pytest.raises(ValueError):
        secure_random_hex(3.14)
    with pytest.raises(ValueError):
        secure_random_hex("10")
