import pytest
from string_utils.validation import contains_html, InvalidInputError

def test_contains_html_detects_simple_tag():
    """Normal case: string contains a simple HTML tag."""
    assert contains_html("Hello <b>world</b>!") is True

def test_contains_html_no_tag_boundary():
    """Boundary case: string contains angle brackets but not a valid tag."""
    # Angle brackets without a closing slash or tag name should not be counted
    assert contains_html("Use < and > for comparison") is False

def test_contains_html_invalid_input_raises_error():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        contains_html(123)  # non-string input
