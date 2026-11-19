import pytest
from string_utils.manipulation import strip_margin
from string_utils.errors import InvalidInputError

def test_strip_margin_basic():
    """Normal multi‑line string with tab indentation."""
    input_str = "\tline 1\n\tline 2\n\tline 3"
    expected = "line 1\nline 2\nline 3"
    assert strip_margin(input_str) == expected

def test_strip_margin_boundary_empty_and_no_tabs():
    """Boundary cases: empty string and string without tabs."""
    assert strip_margin("") == ""
    assert strip_margin("no tabs\nstill no tabs") == "no tabs\nstill no tabs"

def test_strip_margin_error_on_non_string():
    """Non‑string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        strip_margin(123)
