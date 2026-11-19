import pytest
from string_utils.manipulation import asciify
from string_utils.errors import InvalidInputError

def test_asciify_removes_accents_and_non_ascii():
    # Input contains various accented and non‑ASCII characters
    original = "Café Münster – 你好"
    # Expected: accents removed, non‑ASCII Chinese characters stripped
    expected = "Cafe Munster - "
    result = asciify(original)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_asciify_empty_string_returns_empty():
    # Empty string should return empty string without error
    assert asciify("") == ""

def test_asciify_raises_on_non_string_input():
    # Passing a non‑string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        asciify(12345)
