import pytest
from string_utils.manipulation import prettify
from string_utils.errors import InvalidInputError

def test_prettify_basic_example():
    """Test that a typical unprettified string is formatted correctly."""
    raw = " unprettified string ,, like this one,will be\"prettified\" .it\\' s awesome! "
    expected = "Unprettified string, like this one, will be \"prettified\". It's awesome!"
    assert prettify(raw) == expected

def test_prettify_boundary_cases():
    """Test handling of edge cases: empty string, single word, and punctuation spacing."""
    # Empty string should return empty string
    assert prettify("") == ""
    # Single word with leading/trailing spaces
    assert prettify("   hello   ") == "Hello"
    # Multiple punctuation marks should be collapsed to single
    assert prettify("Hello!!!") == "Hello!"
    # Arithmetic spacing
    assert prettify("a+b") == "a + b"
    # Percentage formatting
    assert prettify("100 %") == "100%"

def test_prettify_invalid_input():
    """Test that non-string input raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        prettify(None)
    with pytest.raises(InvalidInputError):
        prettify(123)
