import pytest
from apimd.parser import code

def test_code_escapes_pipe_and_returns_backticks():
    # Input contains a pipe character, should be escaped and wrapped in backticks
    input_text = "a|b"
    result = code(input_text)
    assert result == "`a&#124;b`"
    # Ensure no raw pipe remains
    assert "|" not in result
    # Ensure backticks are present
    assert result.startswith("`") and result.endswith("`")

def test_code_with_ampersand_returns_html_code_tag():
    # Input contains an ampersand, should be wrapped in <code> tags
    input_text = "a&b"
    result = code(input_text)
    assert result == "<code>a&b</code>"
    # Ensure no backticks are used
    assert "`" not in result
    # Ensure the string starts and ends with the correct tags
    assert result.startswith("<code>") and result.endswith("</code>")

def test_code_empty_string_returns_single_space():
    # Empty input should return a single space
    result = code("")
    assert result == " "
    # The result should be exactly one character long
    assert len(result) == 1
