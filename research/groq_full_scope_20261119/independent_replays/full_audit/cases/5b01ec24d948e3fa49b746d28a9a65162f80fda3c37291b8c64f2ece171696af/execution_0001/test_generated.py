import pytest
from semantic_release.helpers import get_number_from_str

def test_extract_decimal_number():
    # Normal decimal extraction from a string containing a number
    assert get_number_from_str("Version 42 is released") == 42
    # If multiple numbers, the first match is returned
    assert get_number_from_str("Build 7 and 8") == 7
    # Leading zeros are handled correctly
    assert get_number_from_str("Leading zeros 0042") == 42

def test_hex_interpretation_and_negative_default():
    # When interpret_hex is True, hex numbers are parsed correctly
    assert get_number_from_str("0x1A3F", interpret_hex=True) == 6719
    # Hex numbers with uppercase letters are also parsed
    assert get_number_from_str("Hex: 0XFF", interpret_hex=True) == 255
    # If interpret_hex is False, hex pattern is ignored and default is returned
    assert get_number_from_str("0x1A3F", interpret_hex=False, default=99) == 99

def test_default_value_on_no_match():
    # When no number is found, the default value is returned
    assert get_number_from_str("No numbers here", default=0) == 0
    # Default can be negative as specified
    assert get_number_from_str("Still no numbers", default=-5) == -5
    # Even if a hex pattern exists but interpret_hex is False, default is used
    assert get_number_from_str("0xABC", interpret_hex=False, default=123) == 123
