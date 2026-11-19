import json
import pytest
from string_utils.validation import is_json

def test_is_json_valid_dict():
    """Valid JSON object should return True."""
    json_str = '{"name": "Alice", "age": 30}'
    assert is_json(json_str) is True
    # Ensure that the parsed value is a dict
    assert isinstance(json.loads(json_str), dict)

def test_is_json_valid_list_and_boundary():
    """Valid JSON list should return True; empty string should return False."""
    json_list = '[1, 2, 3]'
    assert is_json(json_list) is True
    assert isinstance(json.loads(json_list), list)

    # Boundary case: empty string is not a full string
    assert is_json('') is False

def test_is_json_invalid_inputs():
    """Malformed JSON or non-JSON should return False."""
    malformed = '{nope}'
    assert is_json(malformed) is False

    # Non-string input should also return False
    assert is_json(123) is False
