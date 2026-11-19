import pytest
from typesystem.tokenize.tokenize_yaml import tokenize_yaml, ParseError, Position
from typesystem.tokenize.tokens import DictToken, ListToken, ScalarToken

def test_tokenize_yaml_basic_structure():
    yaml_content = """
    name: John
    age: 30
    hobbies:
      - reading
      - coding
    """
    token = tokenize_yaml(yaml_content)
    assert isinstance(token, DictToken)
    assert token.mapping["name"] == "John"
    assert token.mapping["age"] == 30
    assert isinstance(token.mapping["hobbies"], ListToken)
    assert token.mapping["hobbies"].value == ["reading", "coding"]
    # Verify positions are non-negative and within content length
    assert 0 <= token.start <= token.end < len(yaml_content)

def test_tokenize_yaml_empty_content_raises():
    with pytest.raises(ParseError) as excinfo:
        tokenize_yaml("")
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    assert isinstance(err.position, Position)
    assert err.position.line_no == 1 and err.position.column_no == 1 and err.position.char_index == 0

def test_tokenize_yaml_invalid_yaml_raises_parse_error():
    invalid_yaml = "key: [unclosed list"
    with pytest.raises(ParseError) as excinfo:
        tokenize_yaml(invalid_yaml)
    err = excinfo.value
    assert err.code == "parse_error"
    assert "unclosed list" in err.text
    # Position should point to the error location
    assert isinstance(err.position, Position)
    assert err.position.line_no == 1
    assert err.position.column_no > 0
    assert err.position.char_index > 0
