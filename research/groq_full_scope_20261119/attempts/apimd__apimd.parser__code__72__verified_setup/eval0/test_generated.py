import pytest
from apimd.parser import code

def test_code_escapes_pipe_and_returns_backticks():
    """When the input contains a pipe but no ampersand, it should be wrapped in backticks."""
    input_text = "a|b"
    result = code(input_text)
    assert result == "`a|b`"
    # Ensure the pipe is preserved
    assert "|" in result
    # Ensure no HTML tags are present
    assert "<" not in result and ">" not in result

def test_code_wraps_with_ampersand_in_html_code_tag():
    """When the input contains an ampersand, it should be wrapped in <code> tags."""
    input_text = "a&b"
    result = code(input_text)
    assert result == "<code>a&b</code>"
    # Verify that the ampersand is not escaped
    assert "&" in result
    # Ensure backticks are not used
    assert "`" not in result

def test_code_returns_single_space_for_empty_string():
    """An empty string should return a single space character."""
    result = code("")
    assert result == " "
    assert isinstance(result, str)
    assert len(result) == 1
