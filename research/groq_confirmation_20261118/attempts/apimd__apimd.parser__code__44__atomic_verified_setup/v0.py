import pytest
from apimd.parser import code

def test_code_replaces_pipe_and_returns_backticks():
    """When the input contains a pipe character but no ampersand,
    the pipe is escaped and the result is wrapped in backticks."""
    input_text = "a|b"
    expected = "`a&#124;b`"
    assert code(input_text) == expected

def test_code_returns_code_tag_for_ampersand():
    """When the input contains an ampersand, the result is wrapped in a <code> tag."""
    input_text = "x & y"
    expected = "<code>x & y</code>"
    assert code(input_text) == expected

def test_code_returns_space_for_empty_string():
    """An empty string input should return a single space character."""
    assert code("") == " "
