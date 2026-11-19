import pytest
from typesystem.tokenize.tokenize_json import tokenize_json
from typesystem.tokenize.tokens import DictToken, ListToken, ScalarToken, Token
from typesystem.base import ParseError, Position

def test_tokenize_json_valid_dict():
    """Tokenize a simple JSON object and verify the token structure."""
    json_str = '{"key": "value", "num": 42}'
    token = tokenize_json(json_str)
    assert isinstance(token, Token)
    assert isinstance(token, DictToken)
    # The dict should contain two keys
    assert set(token.children.keys()) == {"key", "num"}
    # Each child should be a ScalarToken with correct value
    assert isinstance(token.children["key"], ScalarToken)
    assert token.children["key"].value == "value"
    assert isinstance(token.children["num"], ScalarToken)
    assert token.children["num"].value == 42

def test_tokenize_json_empty_string_raises():
    """An empty string should raise a ParseError with code 'no_content'."""
    with pytest.raises(ParseError) as excinfo:
        tokenize_json("")
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    # Position should be at the start of the content
    assert err.position == Position(column_no=1, line_no=1, char_index=0)

def test_tokenize_json_invalid_json_raises():
    """Malformed JSON should raise a ParseError with code 'parse_error'."""
    bad_json = '{"missing_end": true'
    with pytest.raises(ParseError) as excinfo:
        tokenize_json(bad_json)
    err = excinfo.value
    assert err.code == "parse_error"
    # The error message should contain the JSONDecodeError message
    assert "Expecting" in err.text
    # Position should reflect the location of the error
    assert isinstance(err.position, Position)
    # For this specific input, the error is at line 1, column 22 (after the missing brace)
    assert err.position.line_no == 1
    assert err.position.column_no == 22
