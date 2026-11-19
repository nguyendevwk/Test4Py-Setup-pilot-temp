import pytest
from semantic_release.helpers import get_number_from_str

def test_get_number_from_str_decimal_and_default():
    # Normal decimal extraction
    assert get_number_from_str("version 42 is good") == 42
    # No match returns default
    assert get_number_from_str("no digits here", default=0) == 0
    # Default is used when no number and default not overridden
    assert get_number_from_str("abc", default=-1) == -1

def test_get_number_from_str_hex_interpretation():
    # Hex number with interpret_hex=True
    assert get_number_from_str("0x1A3F", interpret_hex=True) == 6719
    # Hex number with interpret_hex=False falls back to decimal pattern
    assert get_number_from_str("0x1A3F", interpret_hex=False) == -1
    # Mixed string with hex and decimal; decimal takes precedence when interpret_hex=False
    assert get_number_from_str("value 0x10 and 20", interpret_hex=False) == 20
    # Mixed string with hex and decimal; hex takes precedence when interpret_hex=True
    assert get_number_from_str("value 0x10 and 20", interpret_hex=True) == 16

def test_get_number_from_str_boundary_and_negative():
    # Very large number
    large_num = 10**20
    assert get_number_from_str(f"big number {large_num}") == large_num
    # Negative number handling
    assert get_number_from_str("-5 is negative") == -5
    # Hex negative representation (not typical, but test robustness)
    assert get_number_from_str("-0xF", interpret_hex=True) == 15
