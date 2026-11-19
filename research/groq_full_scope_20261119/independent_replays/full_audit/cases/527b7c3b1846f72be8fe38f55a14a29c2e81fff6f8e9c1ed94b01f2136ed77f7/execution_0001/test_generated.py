import pytest
from string_utils.manipulation import strip_html
from string_utils.errors import InvalidInputError

def test_strip_html_removes_tags_and_attributes():
    """Normal case: tags and attributes are removed, content discarded."""
    input_str = 'Hello <b>world</b>! <a href="link">click</a>'
    expected = 'Hello ! '
    assert strip_html(input_str) == expected

def test_strip_html_keeps_tag_content_when_flag_set():
    """Boundary case: keep_tag_content=True preserves inner text but removes tags."""
    input_str = 'Start <div>middle <span>inner</span> end</div> Finish'
    expected = 'Start middle inner end Finish'
    assert strip_html(input_str, keep_tag_content=True) == expected

def test_strip_html_raises_on_non_string_input():
    """Error case: passing a non-string raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        strip_html(12345)  # non-string input
