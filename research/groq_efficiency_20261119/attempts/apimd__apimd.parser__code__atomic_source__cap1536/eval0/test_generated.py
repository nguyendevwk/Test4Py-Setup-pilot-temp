import pytest
from apimd.parser import code

def test_code_replaces_pipe_and_returns_backticks():
    # Input contains a pipe character which should be escaped
    input_text = "a|b"
    result = code(input_text)
    # The pipe should be replaced with its HTML entity and wrapped in backticks
    assert result == "`a&#124;b`"
    # Ensure no raw pipe remains
    assert "|" not in result

def test_code_wraps_ampersand_in_code_tag():
    # Input contains an ampersand which triggers <code> tags
    input_text = "a&b"
    result = code(input_text)
    # The entire string should be wrapped in <code> tags
    assert result == "<code>a&b</code>"
    # The ampersand should remain unchanged inside the tags
    assert "&" in result

def test_code_returns_single_space_for_empty_input():
    # Empty string should return a single space
    assert code("") == " "
