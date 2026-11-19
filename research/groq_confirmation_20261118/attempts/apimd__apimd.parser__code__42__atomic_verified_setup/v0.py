import pytest
from apimd.parser import code

def test_code_escapes_pipe_and_returns_backticks():
    """When the input contains a pipe but no ampersand, the pipe is escaped
    and the result is wrapped in backticks."""
    input_text = "a|b"
    result = code(input_text)
    assert result == "`a&#124;b`"
    # Ensure the original pipe is replaced and backticks are present
    assert "&#124;" in result
    assert result.startswith("`") and result.endswith("`")

def test_code_returns_html_code_tag_for_ampersand():
    """If the input contains an ampersand, the function returns an HTML
    <code> tag instead of backticks."""
    input_text = "a&b"
    result = code(input_text)
    assert result == "<code>a&b</code>"
    # Verify that no backticks are present
    assert "`" not in result
    # Ensure the ampersand is preserved
    assert "&" in result

def test_code_returns_single_space_for_empty_string():
    """An empty string should return a single space character."""
    result = code("")
    assert result == " "
    # The result should be exactly one space, not empty or longer
    assert len(result) == 1
