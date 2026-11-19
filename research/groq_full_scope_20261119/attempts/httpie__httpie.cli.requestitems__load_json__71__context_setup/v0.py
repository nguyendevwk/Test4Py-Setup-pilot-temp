import pytest
from httpie.cli.requestitems import load_json, ParseError
from httpie.cli.argtypes import KeyValueArg

# Helper to create a minimal KeyValueArg instance with an `orig` attribute
class DummyArg:
    def __init__(self, orig: str):
        self.orig = orig

def test_load_json_valid_object():
    """load_json should parse a simple JSON object correctly."""
    arg = DummyArg("foo")
    json_str = '{"a": 1, "b": true, "c": ["x", "y"]}'
    result = load_json(arg, json_str)
    assert isinstance(result, dict)
    assert result == {"a": 1, "b": True, "c": ["x", "y"]}

def test_load_json_empty_string_error():
    """An empty string should raise ParseError with the original argument."""
    arg = DummyArg("empty")
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, "")
    assert "empty" in str(excinfo.value)
    assert "Expecting value" in str(excinfo.value)

def test_load_json_invalid_json_error():
    """Malformed JSON should raise ParseError with the original argument."""
    arg = DummyArg("malformed")
    bad_json = '{"a": 1, "b": }'  # invalid syntax
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, bad_json)
    assert "malformed" in str(excinfo.value)
    assert "Expecting" in str(excinfo.value)
