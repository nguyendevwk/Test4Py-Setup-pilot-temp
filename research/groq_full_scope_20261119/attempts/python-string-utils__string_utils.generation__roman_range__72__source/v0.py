import pytest
from string_utils.generation import roman_range

def test_roman_range_ascending():
    # Generate Roman numerals from 1 to 7 inclusive
    result = list(roman_range(7))
    assert result == ["I", "II", "III", "IV", "V", "VI", "VII"]

def test_roman_range_descending():
    # Generate Roman numerals from 7 down to 1 inclusive
    result = list(roman_range(start=7, stop=1, step=-1))
    assert result == ["VII", "VI", "V", "IV", "III", "II", "I"]

def test_roman_range_invalid_configuration():
    # Step that would skip the stop value should raise OverflowError
    with pytest.raises(OverflowError):
        list(roman_range(start=1, stop=10, step=5))
    # Negative step that would skip the stop value should raise OverflowError
    with pytest.raises(OverflowError):
        list(roman_range(start=10, stop=1, step=-3))
