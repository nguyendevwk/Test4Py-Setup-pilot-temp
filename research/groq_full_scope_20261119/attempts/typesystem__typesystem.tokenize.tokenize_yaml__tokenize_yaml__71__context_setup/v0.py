import pytest
from typesystem.tokenize.tokenize_yaml import tokenize_yaml, ParseError, Position
from typesystem.tokenize.tokens import ScalarToken, DictToken, ListToken

def test_tokenize_yaml_basic_structure():
    yaml_text = """
    name: John
    age: 30
    hobbies:
      - reading
      - hiking
    """
    token = tokenize_yaml(yaml_text)
    assert isinstance(token, DictToken)
    assert token.mapping["name"] == "John"
    assert token.mapping["age"] == 30
    hobbies = token.mapping["hobbies"]
    assert isinstance(hobbies, ListToken)
    assert hobbies.value == ["reading", "hiking"]
    # Verify positions are non-negative and within bounds
    assert 0 <= token.start <= token.end < len(yaml_text)
    for key, val in token.mapping.items():
        if isinstance(val, ScalarToken):
            assert 0 <= val.start <= val.end < len(yaml_text)

def test_tokenize_yaml_empty_content_raises():
    with pytest.raises(ParseError) as excinfo:
        tokenize_yaml("")
    err = excinfo.value
    assert err.code == "no_content"
    assert err.text == "No content."
    assert isinstance(err.position, Position)
    assert err.position.line_no == 1
    assert err.position.column_no == 1
    assert err.position.char_index == 0

def test_tokenize_yaml_invalid_syntax_raises():
    bad_yaml = "key: [unclosed list"
    with pytest.raises(ParseError) as excinfo:
        tokenize_yaml(bad_yaml)
    err = excinfo.value
    assert err.code == "parse_error"
    assert "did not find expected" in err.text or "while parsing a flow sequence" in err.text
    # Position should point to the problematic character
    assert isinstance(err.position, Position)
    assert err.position.line_no == 1
    assert err.position.column_no > 0
    assert err.position.char_index > 0
