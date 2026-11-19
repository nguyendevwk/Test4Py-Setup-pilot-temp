import pytest
from string_utils.validation import contains_html
from string_utils.errors import InvalidInputError

def test_contains_html_detects_simple_tag():
    """Normal case: string contains a simple HTML tag."""
    text = "Hello <b>world</b>!"
    assert contains_html(text) is True

def test_contains_html_no_tag_boundary():
    """Boundary case: string contains angle brackets but not a valid tag."""
    text = "Use < and > to denote angles, not tags."
    assert contains_html(text) is False

def test_contains_html_invalid_input_raises_error():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        contains_html(12345)
