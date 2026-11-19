import pytest
from string_utils.validation import words_count, InvalidInputError

def test_words_count_basic():
    # Normal sentence with spaces
    assert words_count("hello world") == 2
    # Punctuation separated words
    assert words_count("one,two,three.stop") == 4
    # Mixed alphanumerics
    assert words_count("abc123 456def") == 2

def test_words_count_boundary():
    # Empty string should return 0
    assert words_count("") == 0
    # String with only punctuation and symbols
    assert words_count("!@#$%^&*()") == 0
    # Long string with many words
    long_text = " ".join(["word"] * 1000)
    assert words_count(long_text) == 1000

def test_words_count_invalid_input():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        words_count(123)
    with pytest.raises(InvalidInputError):
        words_count(None)
    with pytest.raises(InvalidInputError):
        words_count(b"bytes")
