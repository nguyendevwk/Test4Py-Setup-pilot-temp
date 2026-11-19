import pytest
from apimd.parser import code

def test_code_escapes_pipe_and_returns_backticks():
    """When the input contains a pipe but no ampersand, it should be wrapped in backticks."""
    input_text = "a|b"
    result = code(input_text)
    assert result == "`a|b`"
    # Ensure the pipe is preserved and not escaped
    assert "|" in result
    assert result.startswith("`") and result.endswith("`")

def test_code_wraps_ampersand_in_html_code_tag():
    """When the input contains an ampersand, it should be wrapped in an HTML <code> tag."""
    input_text = "a&b"
    result = code(input_text)
    assert result == "<code>a&b</code>"
    # The ampersand should remain unchanged inside the tag
    assert "&" in result
    assert result.startswith("<code>") and result.endswith("</code>")

def test_code_returns_single_space_for_empty_input():
    """When the input is an empty string, the function should return a single space."""
    input_text = ""
    result = code(input_text)
    assert result == " "
    # The result should be exactly one space character
    assert len(result) == 1 and result == " "
