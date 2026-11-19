import pytest
from string_utils.manipulation import strip_html
from string_utils.errors import InvalidInputError

def test_strip_html_removes_tags_and_attributes():
    """Normal case: tags and attributes are removed, leaving only text."""
    input_str = 'Hello <b>world</b>! <a href="https://example.com">link</a>'
    expected = 'Hello world! link'
    result = strip_html(input_str, keep_tag_content=True)
    assert result == expected

def test_strip_html_removes_tags_and_content_when_not_kept():
    """Boundary case: when keep_tag_content is False, entire tags and their content are removed."""
    input_str = 'Start <div>middle <span>inner</span> end</div> Finish'
    expected = 'Start  Finish'
    result = strip_html(input_str, keep_tag_content=False)
    assert result == expected

def test_strip_html_invalid_input_raises_error():
    """Error case: non-string input raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        strip_html(12345)  # non-string input
