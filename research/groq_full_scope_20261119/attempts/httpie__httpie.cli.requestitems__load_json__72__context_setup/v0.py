import pytest
from types import SimpleNamespace
from httpie.cli.requestitems import load_json, ParseError

# Helper to create a minimal KeyValueArg-like object
def make_arg(orig: str):
    return SimpleNamespace(orig=orig)

def test_load_json_valid_json_returns_expected_structure(tmp_path):
    # Arrange: a simple JSON string
    json_str = '{"name":"Alice","age":30,"hobbies":["reading","cycling"]}'
    arg = make_arg("data")
    # Act: load the JSON
    result = load_json(arg, json_str)
    # Assert: the result is a dict with expected keys and values
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["hobbies"] == ["reading", "cycling"]

def test_load_json_empty_string_raises_parse_error(tmp_path):
    # Arrange: empty JSON string
    json_str = ""
    arg = make_arg("empty")
    # Act & Assert: loading should raise ParseError with the original argument in the message
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, json_str)
    assert "empty" in str(excinfo.value)

def test_load_json_invalid_json_raises_parse_error(tmp_path):
    # Arrange: malformed JSON string
    json_str = "{invalid json}"
    arg = make_arg("bad")
    # Act & Assert: loading should raise ParseError with the original argument in the message
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, json_str)
    assert "bad" in str(excinfo.value)
