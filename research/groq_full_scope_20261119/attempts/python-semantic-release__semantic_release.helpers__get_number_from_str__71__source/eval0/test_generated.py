import pytest
from semantic_release.helpers import get_number_from_str

def test_extract_decimal_number():
    # Normal decimal extraction from a string containing a number
    assert get_number_from_str("Version 42 is released") == 42
    # If multiple numbers, the first match is returned
    assert get_number_from_str("Build 7 and 8") == 7
    # Leading zeros are handled correctly
    assert get_number_from_str("Leading zeros 0042") == 42

def test_extract_hex_number_when_interpreted():
    # Hexadecimal extraction when interpret_hex=True
    assert get_number_from_str("0x1A3F", interpret_hex=True) == 6719
    # Mixed hex and decimal, hex takes precedence
    assert get_number_from_str("0xFF and 255", interpret_hex=True) == 255
    # Negative hex values are converted to positive
    assert get_number_from_str("-0x10", interpret_hex=True) == 16

def test_default_value_and_no_match():
    # When no number is found, default is returned
    assert get_number_from_str("No numbers here") == -1
    # Custom default can be specified
    assert get_number_from_str("No numbers", default=0) == 0
    # Hex pattern should not match if interpret_hex is False
    assert get_number_from_str("0x1A", interpret_hex=False) == -1
