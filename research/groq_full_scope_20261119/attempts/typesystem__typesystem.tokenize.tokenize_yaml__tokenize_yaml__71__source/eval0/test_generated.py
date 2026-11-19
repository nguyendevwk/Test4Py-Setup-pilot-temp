import pytest
from typesystem.tokenize.tokenize_yaml import tokenize_yaml
from typesystem.base import ParseError, Position
from typesystem.tokenize.tokens import DictToken, ListToken, ScalarToken

def test_tokenize_yaml_normal_mapping():
    yaml_content = """
    name: Alice
    age: 30
    hobbies:
      - reading
      - hiking
    """
    token = tokenize_yaml(yaml_content)
    assert isinstance(token, DictToken)
    assert token.mapping == {
        "name": ScalarToken("Alice", 8, 12, content=yaml_content),
        "age": ScalarToken(30, 20, 22, content=yaml_content),
        "hobbies": ListToken(
            [
                ScalarToken("reading", 35, 42, content=yaml_content),
                ScalarToken("hiking", 47, 53, content=yaml_content),
            ],
            28,
            55,
            content=yaml_content,
        ),
    }

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

def test_tokenize_yaml_parse_error_raises():
    bad_yaml = "key: [unclosed list"
    with pytest.raises(ParseError) as excinfo:
        tokenize_yaml(bad_yaml)
    err = excinfo.value
    assert err.code == "parse_error"
    assert "unclosed list" in err.text
    assert isinstance(err.position, Position)
    # Position should point to the start of the error (index of '[')
    assert err.position.char_index == bad_yaml.index("[")
