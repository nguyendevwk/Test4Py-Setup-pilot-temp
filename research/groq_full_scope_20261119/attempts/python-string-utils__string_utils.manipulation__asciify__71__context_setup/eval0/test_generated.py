import pytest
from string_utils.manipulation import asciify
from string_utils.errors import InvalidInputError

def test_asciify_basic_conversion():
    # Normal case: mixed accented characters
    original = "Café Münster – 123"
    expected = "Cafe Munster - 123"
    result = asciify(original)
    assert result == expected
    # Ensure no non-ascii characters remain
    assert all(ord(c) < 128 for c in result)

def test_asciify_empty_string():
    # Boundary case: empty input should return empty output
    assert asciify("") == ""

def test_asciify_invalid_input_type():
    # Error case: passing a non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        asciify(42)
