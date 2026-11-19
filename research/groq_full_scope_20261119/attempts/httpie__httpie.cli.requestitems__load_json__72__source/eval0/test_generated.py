import pytest
from httpie.cli.requestitems import load_json
from httpie.exceptions import ParseError

# Simple stand‑in for KeyValueArg with an `orig` attribute
class DummyArg:
    def __init__(self, orig):
        self.orig = orig

def test_load_json_parses_dict():
    arg = DummyArg("foo=bar")
    json_str = '{"a": 1, "b": 2}'
    result = load_json(arg, json_str)
    assert isinstance(result, dict)
    assert result == {"a": 1, "b": 2}

def test_load_json_parses_array():
    arg = DummyArg("data")
    json_str = '[1, 2, 3]'
    result = load_json(arg, json_str)
    assert isinstance(result, list)
    assert result == [1, 2, 3]

def test_load_json_raises_parse_error_on_invalid_json():
    arg = DummyArg("invalid")
    invalid_str = '{"missing_end": true'
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, invalid_str)
    assert str(arg.orig) in str(excinfo.value)
    assert "missing_end" in str(excinfo.value)
