import pytest
from string_utils.validation import contains_html
from string_utils.errors import InvalidInputError

def test_contains_html_detects_tags():
    """Normal case: string contains an HTML tag."""
    text = "Hello <b>world</b>!"
    assert contains_html(text) is True

def test_contains_html_no_tags():
    """Boundary case: string has no tags, should return False."""
    text = "Just a plain sentence with no markup."
    assert contains_html(text) is False

def test_contains_html_invalid_input_raises():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        contains_html(12345)
