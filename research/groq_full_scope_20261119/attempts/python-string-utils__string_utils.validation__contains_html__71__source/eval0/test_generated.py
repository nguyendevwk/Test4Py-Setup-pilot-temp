import pytest
from string_utils.validation import contains_html
from string_utils.errors import InvalidInputError

def test_contains_html_detects_basic_tag():
    """Verify that a simple HTML tag is detected."""
    text = "Hello <b>world</b>!"
    assert contains_html(text) is True

def test_contains_html_no_tag_returns_false():
    """Verify that a string without any tags returns False."""
    text = "Just a plain sentence with no markup."
    assert contains_html(text) is False

def test_contains_html_invalid_input_raises_error():
    """Verify that non-string input raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        contains_html(12345)  # non-string input
