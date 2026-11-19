import pytest
from typesystem.tokenize.tokenize_json import tokenize_json, ParseError, Position
from typesystem.tokenize.tokens import DictToken, ListToken, ScalarToken, Token

def test_tokenize_json_valid_dict():
    """Tokenize a simple JSON object and verify the returned token type and structure."""
    json_str = '{"key": "value", "num": 42}'
    token = tokenize_json(json_str)
    assert isinstance(token, Token)
    assert isinstance(token, DictToken)
    # The token should contain two key-value pairs
    assert len(token) == 2
    # Verify that the keys are ScalarTokens and values are ScalarTokens or appropriate types
    for key_token, value_token in token.items():
        assert isinstance(key_token, ScalarToken)
        assert isinstance(value_token, ScalarToken)
    # Check that the original JSON string is preserved in the token's raw representation
    assert token.raw == json_str

def test_tokenize_json_empty_string_raises():
    """An empty string should raise a ParseError with code 'no_content'."""
    with pytest.raises(ParseError) as excinfo:
        tokenize_json("")
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    # Position should be at the start of the input
    assert isinstance(err.position, Position)
    assert err.position.line_no == 1
    assert err.position.column_no == 1
    assert err.position.char_index == 0

def test_tokenize_json_malformed_raises():
    """Malformed JSON should raise a ParseError with code 'parse_error'."""
    malformed = '{"incomplete": true'
    with pytest.raises(ParseError) as excinfo:
        tokenize_json(malformed)
    err = excinfo.value
    assert err.code == "parse_error"
    # The error message should contain the JSONDecodeError message
    assert "Expecting" in err.text or "Expecting" in err.text
    # Position should reflect the location of the error
    assert isinstance(err.position, Position)
    # The column and line numbers should be greater than zero
    assert err.position.line_no > 0
    assert err.position.column_no > 0
    assert err.position.char_index >= 0
