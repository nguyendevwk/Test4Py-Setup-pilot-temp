import pytest
from typesystem.tokenize.tokenize_yaml import tokenize_yaml
from typesystem.base import ParseError, Position
from typesystem.tokenize.tokens import DictToken, ListToken, ScalarToken

def test_tokenize_yaml_normal_mapping():
    yaml_text = """
    name: Alice
    age: 30
    hobbies:
      - reading
      - hiking
    """
    token = tokenize_yaml(yaml_text)
    assert isinstance(token, DictToken)
    assert token.mapping == {"name": "Alice", "age": 30, "hobbies": ["reading", "hiking"]}
    # Check that positions are integers and start <= end
    assert isinstance(token.start, int)
    assert isinstance(token.end, int)
    assert token.start <= token.end

def test_tokenize_yaml_empty_string_raises():
    with pytest.raises(ParseError) as excinfo:
        tokenize_yaml("")
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    assert isinstance(err.position, Position)
    assert err.position.line_no == 1
    assert err.position.column_no == 1
    assert err.position.char_index == 0

def test_tokenize_yaml_parse_error():
    bad_yaml = "key: [unclosed list"
    with pytest.raises(ParseError) as excinfo:
        tokenize_yaml(bad_yaml)
    err = excinfo.value
    assert err.code == "parse_error"
    assert "unclosed list" in err.text
    # Position should point to the error location
    assert isinstance(err.position, Position)
    assert err.position.line_no == 1
    assert err.position.column_no > 0
    assert err.position.char_index > 0
