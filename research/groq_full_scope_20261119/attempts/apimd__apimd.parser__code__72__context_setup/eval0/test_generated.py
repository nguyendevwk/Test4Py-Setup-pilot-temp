import pytest
from apimd.parser import code

def test_code_escapes_pipe_and_returns_backticks():
    # Input contains a pipe character, which should be escaped.
    input_text = "a|b"
    result = code(input_text)
    # The pipe should be replaced with its HTML entity.
    assert "&#124;" in result
    # The result should be wrapped in backticks because no ampersand is present.
    assert result.startswith("`") and result.endswith("`")

def test_code_wraps_with_code_tag_when_ampersand_present():
    # Input contains an ampersand, which triggers a <code> tag.
    input_text = "a&b"
    result = code(input_text)
    # The result should be wrapped in <code> tags.
    assert result.startswith("<code>") and result.endswith("</code>")
    # The ampersand should remain unchanged inside the tags.
    assert "&" in result

def test_code_returns_single_space_for_empty_input():
    # Empty string should return a single space.
    assert code("") == " "
