import pytest
from httpie.cli.requestitems import load_json
from httpie.exceptions import ParseError

# A minimal stub for KeyValueArg that mimics the interface used by load_json
class DummyKeyValueArg:
    def __init__(self, orig):
        self.orig = orig

def test_load_json_valid_json():
    """load_json should parse a valid JSON string and return the corresponding Python object."""
    arg = DummyKeyValueArg(orig="--json")
    json_str = '{"name": "Alice", "age": 30}'
    result = load_json(arg, json_str)
    assert isinstance(result, dict)
    assert result == {"name": "Alice", "age": 30}

def test_load_json_empty_string():
    """load_json should raise ParseError when given an empty string (invalid JSON)."""
    arg = DummyKeyValueArg(orig="--json")
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, "")
    # The error message should include the original argument representation
    assert str(arg.orig) in str(excinfo.value)
    assert "Expecting value" in str(excinfo.value)

def test_load_json_invalid_json():
    """load_json should raise ParseError for malformed JSON and include the original argument."""
    arg = DummyKeyValueArg(orig="--json")
    malformed = '{"name": "Bob", "age": }'  # missing value for age
    with pytest.raises(ParseError) as excinfo:
        load_json(arg, malformed)
    assert str(arg.orig) in str(excinfo.value)
    assert "Expecting" in str(excinfo.value)
