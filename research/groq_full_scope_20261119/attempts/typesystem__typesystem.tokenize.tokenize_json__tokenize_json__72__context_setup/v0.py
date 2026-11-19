import pytest
from typesystem.tokenize.tokenize_json import tokenize_json, ParseError
from typesystem.tokenize.tokens import ScalarToken, DictToken, ListToken

def test_tokenize_json_normal_object():
    json_str = '{"a": 1, "b": [true, false, null], "c": "text"}'
    token = tokenize_json(json_str)
    assert isinstance(token, DictToken)
    assert token.value == {"a": 1, "b": [True, False, None], "c": "text"}
    # Check that scalar tokens inside have correct positions
    inner_tokens = token.value
    assert isinstance(inner_tokens["b"], ListToken)
    assert inner_tokens["b"].value == [True, False, None]
    # Verify that the first scalar token (1) has correct column and line
    first_scalar = token.value["a"]
    assert isinstance(first_scalar, ScalarToken)
    assert first_scalar.value == 1
    assert first_scalar.start == 6  # column index of '1' in the string
    assert first_scalar.end == 6

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
    bad_json = '{"missing": "value",}'
    with pytest.raises(ParseError) as excinfo:
        tokenize_json(bad_json)
    err = excinfo.value
    assert err.code == "parse_error"
    # The error message should include the original JSONDecodeError message
    assert "Expecting property name enclosed in double quotes" in err.text
    # Position should reflect the comma after the last property
    assert err.position.column_no == 25
    assert err.position.line_no == 1
    assert err.position.char_index == 24
