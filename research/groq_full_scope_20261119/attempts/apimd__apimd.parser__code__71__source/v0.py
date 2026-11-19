import pytest
from apimd.parser import code

def test_code_escapes_pipe_and_returns_backticks():
    """When the input contains a pipe but no ampersand, it should be escaped and wrapped in backticks."""
    input_str = "a|b"
    expected = "`a&#124;b`"
    assert code(input_str) == expected

def test_code_wraps_ampersand_in_html_code_tag():
    """When the input contains an ampersand, it should be wrapped in an HTML <code> tag."""
    input_str = "a&b"
    expected = "<code>a&b</code>"
    assert code(input_str) == expected

def test_code_returns_single_space_for_empty_input():
    """An empty string should return a single space."""
    assert code("") == " "
