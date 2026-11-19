import pytest
from string_utils.manipulation import strip_html
from string_utils.errors import InvalidInputError

def test_strip_html_removes_tags_and_attributes():
    """When keep_tag_content is False, tags and their attributes are removed."""
    input_str = 'Hello <b style="color:red">world</b>!'
    expected = 'Hello !'
    assert strip_html(input_str) == expected

def test_strip_html_keeps_tag_content_when_flag_set():
    """When keep_tag_content is True, only tags are removed but inner text remains."""
    input_str = 'Click <a href="https://example.com">here</a> now.'
    expected = 'Click here now.'
    assert strip_html(input_str, keep_tag_content=True) == expected

def test_strip_html_raises_on_non_string_input():
    """strip_html should raise InvalidInputError when input is not a string."""
    with pytest.raises(InvalidInputError):
        strip_html(123)  # non-string input
