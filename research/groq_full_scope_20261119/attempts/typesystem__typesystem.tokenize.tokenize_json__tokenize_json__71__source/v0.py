import pytest
from typesystem.tokenize.tokenize_json import tokenize_json
from typesystem.tokenize.tokens import DictToken, ListToken, ScalarToken
from typesystem.base import ParseError

def test_tokenize_json_valid_dict():
    """Tokenize a simple JSON object and verify the returned token type."""
    json_str = '{"key": "value", "num": 42}'
    token = tokenize_json(json_str)
    assert isinstance(token, DictToken)
    # The token should contain the correct number of children
    assert len(token.children) == 2
    # Each child should be a ScalarToken with the appropriate value
    values = {child.key: child.value for child in token.children}
    assert values == {"key": "value", "num": 42}

def test_tokenize_json_empty_string_raises():
    """An empty string should raise a ParseError with the correct code."""
    with pytest.raises(ParseError) as excinfo:
        tokenize_json("")
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    # Position should be at the start of the input
    assert err.position.column_no == 1
    assert err.position.line_no == 1
    assert err.position.char_index == 0

def test_tokenize_json_invalid_json_raises():
    """Malformed JSON should raise a ParseError with parse_error code."""
    bad_json = '{"missing_end": true'
    with pytest.raises(ParseError) as excinfo:
        tokenize_json(bad_json)
    err = excinfo.value
    assert err.code == "parse_error"
    # The error message should contain the original JSONDecodeError message
    assert "Expecting" in err.text
    # Position should reflect the location of the error
    assert err.position.column_no > 0
    assert err.position.line_no > 0
    assert err.position.char_index >= 0
