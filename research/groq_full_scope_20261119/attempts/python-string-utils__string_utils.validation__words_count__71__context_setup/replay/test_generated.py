import pytest
from string_utils.validation import words_count, InvalidInputError

def test_words_count_basic():
    # Normal case with spaces and punctuation
    assert words_count("hello world") == 2
    assert words_count("one,two,three.stop") == 4
    # Mixed alphanumeric words
    assert words_count("abc123 456def") == 2

def test_words_count_boundary():
    # Empty string and string with only punctuation
    assert words_count("") == 0
    assert words_count("! @ # % ... []") == 0
    # String with leading/trailing punctuation
    assert words_count(",start middle end,") == 3

def test_words_count_error():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        words_count(123)
    with pytest.raises(InvalidInputError):
        words_count(None)
