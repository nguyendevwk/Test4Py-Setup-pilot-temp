import os
import binascii
import pytest
from string_utils.generation import secure_random_hex

def test_secure_random_hex_length_and_hex_output():
    # Generate a hex string for 16 bytes
    byte_count = 16
    hex_str = secure_random_hex(byte_count)
    # The length should be exactly twice the byte count
    assert len(hex_str) == byte_count * 2
    # All characters should be valid hexadecimal digits
    assert all(c in "0123456789abcdef" for c in hex_str)

def test_secure_random_hex_randomness_and_determinism():
    # Generate two hex strings with the same byte count
    byte_count = 8
    hex1 = secure_random_hex(byte_count)
    hex2 = secure_random_hex(byte_count)
    # They should not be identical (high probability)
    assert hex1 != hex2
    # Ensure that the underlying bytes are truly random by checking that
    # the decoded bytes differ
    bytes1 = binascii.unhexlify(hex1)
    bytes2 = binascii.unhexlify(hex2)
    assert bytes1 != bytes2

def test_secure_random_hex_invalid_input_raises_value_error():
    # Passing a non-integer or a non-positive integer should raise ValueError
    with pytest.raises(ValueError):
        secure_random_hex(0)
    with pytest.raises(ValueError):
        secure_random_hex(-5)
    with pytest.raises(ValueError):
        secure_random_hex(3.14)
    with pytest.raises(ValueError):
        secure_random_hex("10")
