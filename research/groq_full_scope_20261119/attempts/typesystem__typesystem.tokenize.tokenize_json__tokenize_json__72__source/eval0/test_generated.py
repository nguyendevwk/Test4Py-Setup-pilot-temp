import pytest
from typesystem.tokenize.tokenize_json import tokenize_json, ParseError
from typesystem.tokenize.tokens import DictToken, ListToken, ScalarToken, Token

def test_tokenize_json_valid_object():
    json_str = '{"name": "Alice", "age": 30, "hobbies": ["reading", "hiking"]}'
    token = tokenize_json(json_str)
    assert isinstance(token, Token)
    assert isinstance(token, DictToken)
    assert set(token.children.keys()) == {"name", "age", "hobbies"}
    assert isinstance(token.children["name"], ScalarToken)
    assert token.children["name"].value == "Alice"
    assert isinstance(token.children["age"], ScalarToken)
    assert token.children["age"].value == 30
    assert isinstance(token.children["hobbies"], ListToken)
    assert [item.value for item in token.children["hobbies"].children] == ["reading", "hiking"]

def test_tokenize_json_empty_string_raises():
    with pytest.raises(ParseError) as excinfo:
        tokenize_json("")
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    assert err.position.column_no == 1
    assert err.position.line_no == 1
    assert err.position.char_index == 0

def test_tokenize_json_invalid_syntax_raises():
    bad_json = '{"missing_end": true'
    with pytest.raises(ParseError) as excinfo:
        tokenize_json(bad_json)
    err = excinfo.value
    assert err.code == "parse_error"
    assert "Expecting" in err.text or "Expecting value" in err.text
    # Position should reflect the location of the error
    assert err.position.column_no > 0
    assert err.position.line_no > 0
    assert err.position.char_index >= 0
