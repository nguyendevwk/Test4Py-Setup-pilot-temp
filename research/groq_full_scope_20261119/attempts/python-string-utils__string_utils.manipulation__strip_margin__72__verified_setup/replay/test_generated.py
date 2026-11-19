import pytest
from string_utils.manipulation import strip_margin
from string_utils.errors import InvalidInputError

def test_strip_margin_removes_leading_tabs_and_spaces():
    raw = """\
        line 1
        line 2
        line 3"""
    expected = """\
line 1
line 2
line 3"""
    assert strip_margin(raw) == expected

def test_strip_margin_handles_empty_and_single_line_strings():
    assert strip_margin("") == ""
    assert strip_margin("no margin") == "no margin"

def test_strip_margin_raises_on_non_string_input():
    with pytest.raises(InvalidInputError):
        strip_margin(123)
