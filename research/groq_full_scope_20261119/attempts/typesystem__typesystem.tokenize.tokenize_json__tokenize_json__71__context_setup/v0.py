import pytest
from typesystem.tokenize.tokenize_json import tokenize_json, ParseError
from typesystem.tokenize.tokens import DictToken, ListToken, ScalarToken, Token

def test_tokenize_json_normal_object():
    json_str = '{"a": 1, "b": [true, false, null], "c": "text"}'
    token = tokenize_json(json_str)
    assert isinstance(token, DictToken)
    assert token.value == {"a": 1, "b": [True, False, None], "c": "text"}
    # Verify positions: first key starts at column 2 (after '{')
    assert token.start == 0
    assert token.end == len(json_str) - 1
    # Check nested list token
    nested_list = token.value["b"]
    assert isinstance(nested_list, list)
    # Ensure scalar tokens inside list have correct types
    assert isinstance(token.value["a"], int)
    assert isinstance(token.value["c"], str)

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
    bad_json = '{"a": 1, "b": [true, false, null], "c": "text"'  # missing closing brace
    with pytest.raises(ParseError) as excinfo:
        tokenize_json(bad_json)
    err = excinfo.value
    assert err.code == "parse_error"
    # The error message should contain the original JSONDecodeError message
    assert "Expecting" in err.text
    # Position should point to the end of the string
    assert err.position.column_no == len(bad_json) + 1
    assert err.position.line_no == 1
    assert err.position.char_index == len(bad_json)
