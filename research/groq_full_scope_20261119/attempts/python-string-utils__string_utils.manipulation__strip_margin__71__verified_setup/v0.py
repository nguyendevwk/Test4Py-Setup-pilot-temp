import pytest
from string_utils.manipulation import strip_margin
from string_utils.errors import InvalidInputError

def test_strip_margin_basic_multiline():
    raw = """\
        line 1
        line 2
        line 3"""
    expected = """\
line 1
line 2
line 3"""
    assert strip_margin(raw) == expected

def test_strip_margin_empty_and_single_line():
    # Empty string should return empty string
    assert strip_margin("") == ""
    # Single line with no margin should remain unchanged
    single = "no margin"
    assert strip_margin(single) == single

def test_strip_margin_invalid_input_raises():
    with pytest.raises(InvalidInputError):
        strip_margin(123)  # non-string input
