import pytest
from string_utils.manipulation import strip_margin
from string_utils.errors import InvalidInputError

def test_strip_margin_basic_multiline():
    """Normal case: remove leading margin markers from a simple multiline string."""
    input_str = """\
        |line 1
        |line 2
        |line 3"""
    # The function should strip the leading '|' and any preceding whitespace.
    expected = "line 1\nline 2\nline 3"
    assert strip_margin(input_str) == expected

def test_strip_margin_boundary_empty_and_single_line():
    """Boundary case: empty string and single line without margin."""
    # Empty string should return empty string.
    assert strip_margin("") == ""
    # Single line without margin should remain unchanged.
    single_line = "no margin"
    assert strip_margin(single_line) == single_line

def test_strip_margin_invalid_input_raises_error():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        strip_margin(123)  # passing an integer instead of a string
