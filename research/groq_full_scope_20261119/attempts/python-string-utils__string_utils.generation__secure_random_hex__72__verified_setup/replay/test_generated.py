import re
import os
import binascii
import pytest
from string_utils.generation import secure_random_hex

def test_secure_random_hex_length_and_characters():
    """The function should return a hex string of length 2*byte_count containing only hex digits."""
    byte_count = 10
    result = secure_random_hex(byte_count)
    assert isinstance(result, str)
    assert len(result) == 2 * byte_count
    assert re.fullmatch(r'[0-9a-f]{%d}' % (2 * byte_count), result)

def test_secure_random_hex_minimum_byte_count():
    """The function should work for the minimum allowed byte_count of 1."""
    result = secure_random_hex(1)
    assert isinstance(result, str)
    assert len(result) == 2
    assert re.fullmatch(r'[0-9a-f]{2}', result)

def test_secure_random_hex_invalid_input_raises_value_error():
    """The function should raise ValueError for non‑positive or non‑int byte_count."""
    with pytest.raises(ValueError):
        secure_random_hex(0)
    with pytest.raises(ValueError):
        secure_random_hex(-5)
    with pytest.raises(ValueError):
        secure_random_hex(3.14)
    with pytest.raises(ValueError):
        secure_random_hex("10")
