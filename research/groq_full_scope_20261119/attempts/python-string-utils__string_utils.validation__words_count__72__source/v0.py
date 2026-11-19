import pytest
from string_utils.validation import words_count
from string_utils.errors import InvalidInputError

def test_words_count_basic():
    """Normal case: simple sentence with spaces."""
    assert words_count("hello world") == 2
    assert words_count("one,two,three.stop") == 4
    assert words_count("  leading and trailing  ") == 4

def test_words_count_boundary():
    """Boundary case: empty string and string with only punctuation."""
    assert words_count("") == 0
    assert words_count("!@#$%^&*()") == 0
    assert words_count("a") == 1
    assert words_count("a b c") == 3

def test_words_count_error():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        words_count(123)
    with pytest.raises(InvalidInputError):
        words_count(None)
    with pytest.raises(InvalidInputError):
        words_count(['list', 'of', 'strings'])
