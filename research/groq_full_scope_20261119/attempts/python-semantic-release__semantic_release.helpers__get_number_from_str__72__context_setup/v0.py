import pytest
from semantic_release.helpers import get_number_from_str


def test_get_number_from_str_basic_integer():
    """Normal case: extract decimal integer from a string."""
    s = "The version is 42, please update."
    result = get_number_from_str(s)
    assert result == 42, "Should return the first decimal number found"


def test_get_number_from_str_hex_interpretation():
    """Boundary case: interpret hexadecimal when requested."""
    s = "Checksum: 0x1A3F is the value."
    # Without interpret_hex, should return default -1
    assert get_number_from_str(s) == -1
    # With interpret_hex=True, should parse hex and return absolute int
    assert get_number_from_str(s, interpret_hex=True) == 6719
    # Negative hex should still return positive absolute value
    s_neg = "Negative hex: -0xFF"
    assert get_number_from_str(s_neg, interpret_hex=True) == 255


def test_get_number_from_str_no_match_and_default():
    """Error case: no numeric pattern, default should be returned."""
    s = "No numbers here!"
    default_value = 99
    result = get_number_from_str(s, default=default_value)
    assert result == default_value, "Should return the provided default when no number is found"
