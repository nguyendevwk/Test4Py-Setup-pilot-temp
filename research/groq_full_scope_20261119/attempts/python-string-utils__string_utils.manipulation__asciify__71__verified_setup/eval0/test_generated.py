import pytest
from string_utils.manipulation import asciify
from string_utils.errors import InvalidInputError

def test_asciify_basic_conversion():
    # Normal case: mixed accented characters should be transliterated
    input_str = "Café Münster – 123"
    expected = "Cafe Munster - 123"
    result = asciify(input_str)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_asciify_empty_string():
    # Boundary case: empty string should return empty string without error
    result = asciify("")
    assert result == "", "Empty string should remain empty after asciify"

def test_asciify_invalid_input_type():
    # Error case: passing a non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        asciify(12345)  # non-string input
