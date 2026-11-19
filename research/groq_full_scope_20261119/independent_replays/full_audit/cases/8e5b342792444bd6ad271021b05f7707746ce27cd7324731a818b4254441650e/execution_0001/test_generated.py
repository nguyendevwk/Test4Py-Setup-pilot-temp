import pytest
from string_utils.generation import roman_range

def test_roman_range_ascending():
    """Verify ascending range produces correct Roman numerals."""
    expected = ["I", "II", "III", "IV", "V", "VI", "VII"]
    result = list(roman_range(7))
    assert result == expected, f"Expected {expected}, got {result}"

def test_roman_range_descending():
    """Verify descending range produces correct Roman numerals."""
    expected = ["VII", "VI", "V", "IV", "III", "II", "I"]
    result = list(roman_range(start=7, stop=1, step=-1))
    assert result == expected, f"Expected {expected}, got {result}"

def test_roman_range_invalid_configuration():
    """Verify that an invalid start/stop/step raises OverflowError."""
    with pytest.raises(OverflowError):
        list(roman_range(start=5, stop=10, step=-1))
