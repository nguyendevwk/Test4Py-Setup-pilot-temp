import json
import pytest
from string_utils.validation import is_json

def test_is_json_valid_dict():
    """Valid JSON object should return True."""
    json_str = '{"name": "Peter", "age": 30}'
    assert is_json(json_str) is True
    # Ensure that the parsed value is a dict
    parsed = json.loads(json_str)
    assert isinstance(parsed, dict)
    assert parsed["name"] == "Peter"

def test_is_json_invalid_syntax():
    """Malformed JSON should return False."""
    malformed = '{"name": "Peter", "age": 30'  # missing closing brace
    assert is_json(malformed) is False
    # Also test a non-JSON string that looks like JSON
    non_json = '{nope}'
    assert is_json(non_json) is False

def test_is_json_boundary_empty_and_non_string():
    """Boundary cases: empty string and non-string input should return False."""
    assert is_json("") is False
    assert is_json("   ") is False
    assert is_json(None) is False
    assert is_json(123) is False
    assert is_json(["not", "a", "string"]) is False
