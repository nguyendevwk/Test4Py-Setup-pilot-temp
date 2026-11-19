import pytest
from httpie.cli.requestitems import load_json
from httpie.exceptions import ParseError

# Dummy KeyValueArg with only the attributes used by load_json
class DummyArg:
    def __init__(self, orig):
        self.orig = orig

def test_load_json_valid_json():
    """load_json should return a Python object for valid JSON."""
    arg = DummyArg(orig="--data")
    json_str = '{"key": "value", "list": [1, 2, 3]}'
    result = load_json(arg, json_str)
    assert isinstance(result, dict)
    assert result["key"] == "value"
    assert result["list"] == [1, 2, 3]

def test_load_json_invalid_json_raises_parse_error():
    """load_json should raise ParseError with the original argument string."""
    arg = DummyArg(orig="--data")
    invalid_json = '{"key": "value",}'  # trailing comma makes it invalid
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, invalid_json)
    assert str(excinfo.value).startswith(f'{arg.orig!r}:')
    assert "trailing" in str(excinfo.value).lower()

def test_load_json_empty_string_raises_parse_error():
    """An empty string should be treated as invalid JSON and raise ParseError."""
    arg = DummyArg(orig="--data")
    empty_str = ""
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, empty_str)
    assert str(excinfo.value).startswith(f'{arg.orig!r}:')
    assert "empty" in str(excinfo.value).lower()
