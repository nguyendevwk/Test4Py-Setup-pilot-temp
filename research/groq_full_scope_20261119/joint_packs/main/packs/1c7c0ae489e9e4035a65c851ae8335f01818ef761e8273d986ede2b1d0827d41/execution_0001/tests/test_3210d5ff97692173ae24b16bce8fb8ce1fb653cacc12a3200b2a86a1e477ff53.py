import pytest
from string_utils.generation import roman_range

def test_ascending_roman_range():
    """Verify that roman_range generates correct ascending Roman numerals."""
    expected = ["I", "II", "III", "IV", "V"]
    result = list(roman_range(5))
    assert result == expected, f"Expected {expected}, got {result}"

def test_descending_roman_range():
    """Verify that roman_range generates correct descending Roman numerals."""
    expected = ["V", "IV", "III", "II", "I"]
    result = list(roman_range(start=5, stop=1, step=-1))
    assert result == expected, f"Expected {expected}, got {result}"

def test_invalid_configuration_raises():
    """roman_range should raise OverflowError for impossible step configurations."""
    with pytest.raises(OverflowError):
        list(roman_range(start=5, stop=10, step=10))
    with pytest.raises(ValueError):
        list(roman_range(stop="5"))
