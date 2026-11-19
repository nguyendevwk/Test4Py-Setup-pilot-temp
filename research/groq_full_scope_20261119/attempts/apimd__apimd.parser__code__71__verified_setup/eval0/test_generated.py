import pytest
from apimd.parser import code

def test_code_escapes_pipe_and_returns_backticks():
    """When the input contains a pipe but no ampersand, it should be wrapped in backticks."""
    input_str = "a|b"
    result = code(input_str)
    assert result == "`a|b`"
    # Ensure that the pipe character is preserved inside the backticks
    assert "|" in result
    # The result should not contain any HTML tags
    assert "<" not in result and ">" not in result

def test_code_escapes_ampersand_and_returns_html():
    """When the input contains an ampersand, it should be wrapped in <code> tags."""
    input_str = "a&b"
    result = code(input_str)
    assert result == "<code>a&b</code>"
    # The ampersand should remain unchanged inside the tags
    assert "&" in result
    # The result should not contain backticks
    assert "`" not in result

def test_code_empty_input_returns_single_space():
    """An empty string should return a single space character."""
    input_str = ""
    result = code(input_str)
    assert result == " "
    # The result should be exactly one space, not empty or longer
    assert len(result) == 1
