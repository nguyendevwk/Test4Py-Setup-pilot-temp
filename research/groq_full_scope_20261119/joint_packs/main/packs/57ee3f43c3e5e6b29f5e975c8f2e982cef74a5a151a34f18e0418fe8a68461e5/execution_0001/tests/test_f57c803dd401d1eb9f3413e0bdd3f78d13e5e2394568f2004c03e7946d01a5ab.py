import pytest
from string_utils.manipulation import asciify
from string_utils.errors import InvalidInputError

def test_asciify_removes_non_ascii_and_normalizes():
    # Input contains accented characters and special letters
    original = "Café Münster – 123"
    # Expected: accents removed, dash replaced by space, numbers kept
    expected = "Cafe Munster  123"
    result = asciify(original)
    assert result == expected
    # Ensure no non-ascii characters remain
    assert all(ord(c) < 128 for c in result)

def test_asciify_empty_string_returns_empty():
    # Empty string should return empty string without error
    assert asciify("") == ""

def test_asciify_invalid_input_raises_error():
    # Passing a non-string (e.g., integer) should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        asciify(42)
