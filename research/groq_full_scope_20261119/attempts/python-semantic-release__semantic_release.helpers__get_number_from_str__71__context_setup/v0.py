import pytest
from semantic_release.helpers import get_number_from_str

def test_get_number_from_str_decimal_extraction():
    # Should extract the first decimal number in the string
    assert get_number_from_str("Version 12.3.4") == 12
    assert get_number_from_str("build 001, 002, 003") == 1
    assert get_number_from_str("no numbers here") == -1

def test_get_number_from_str_hex_interpretation():
    # When interpret_hex is True, hex numbers are parsed as base 16
    assert get_number_from_str("0x1A", interpret_hex=True) == 26
    assert get_number_from_str("prefix0xFFsuffix", interpret_hex=True) == 255
    # Without interpret_hex, hex string is treated as decimal if possible
    assert get_number_from_str("0x1A", interpret_hex=False) == -1

def test_get_number_from_str_default_and_boundary():
    # Default value is returned when no number is found
    assert get_number_from_str("abc", default=42) == 42
    # Boundary: very large number
    large_num = "999999999999999999999999999999"
    assert get_number_from_str(large_num) == int(large_num)
