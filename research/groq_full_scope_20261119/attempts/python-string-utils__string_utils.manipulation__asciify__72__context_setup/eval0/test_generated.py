import pytest
from string_utils.manipulation import asciify
from string_utils.errors import InvalidInputError

def test_asciify_removes_accents_and_non_ascii():
    # Input contains various accented and non‑ASCII characters
    original = "Café Münster – 123"
    # Expected: accents removed, dash replaced by space, numbers preserved
    expected = "Cafe Munster  123"
    result = asciify(original)
    assert result == expected
    # Ensure no non‑ASCII characters remain
    assert all(ord(ch) < 128 for ch in result)

def test_asciify_empty_string_returns_empty():
    # Empty string should be handled gracefully
    result = asciify("")
    assert result == ""
    # No characters, so length is zero
    assert len(result) == 0

def test_asciify_invalid_input_raises_error():
    # Passing a non‑string (e.g., integer) should raise InvalidInputError
    with pytest.raises(InvalidInputError) as excinfo:
        asciify(42)
    # The exception message should contain the invalid input
    assert "42" in str(excinfo.value)
