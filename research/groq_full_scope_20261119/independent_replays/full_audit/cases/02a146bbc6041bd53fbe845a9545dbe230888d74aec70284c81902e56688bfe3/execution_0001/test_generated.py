import re
import os
import binascii
import pytest

from string_utils.generation import secure_random_hex


def test_secure_random_hex_length_and_hex_chars():
    """The function should return a hex string of length 2 * byte_count."""
    byte_count = 5
    result = secure_random_hex(byte_count)
    assert isinstance(result, str)
    assert len(result) == 2 * byte_count
    assert re.fullmatch(r"[0-9a-f]+", result), "Result contains non-hex characters"


def test_secure_random_hex_minimum_byte_count():
    """The function should work for the minimum allowed byte_count of 1."""
    result = secure_random_hex(1)
    assert isinstance(result, str)
    assert len(result) == 2
    assert re.fullmatch(r"[0-9a-f]{2}", result), "Result is not a 2-char hex string"


def test_secure_random_hex_invalid_input_raises_value_error():
    """The function should raise ValueError for non-positive or non-integer inputs."""
    for invalid in (0, -3, 3.5, "10", None):
        with pytest.raises(ValueError, match="byte_count must be >= 1"):
            secure_random_hex(invalid)
