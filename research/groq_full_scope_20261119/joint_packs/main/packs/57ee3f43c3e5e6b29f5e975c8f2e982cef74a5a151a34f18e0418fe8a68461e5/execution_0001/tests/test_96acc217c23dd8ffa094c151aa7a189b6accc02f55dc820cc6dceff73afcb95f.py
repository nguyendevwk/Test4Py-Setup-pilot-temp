import json
import pytest
from string_utils.validation import is_json

def test_is_json_valid_dict():
    """Valid JSON object should return True."""
    json_str = '{"name": "Alice", "age": 30}'
    assert is_json(json_str) is True
    # Ensure that the string is parsed correctly
    parsed = json.loads(json_str)
    assert isinstance(parsed, dict)
    assert parsed["name"] == "Alice"
    assert parsed["age"] == 30

def test_is_json_invalid_empty_string():
    """Empty string should not be considered valid JSON."""
    empty = ""
    assert is_json(empty) is False

def test_is_json_non_string_input():
    """Non-string input should return False without raising."""
    non_string = 12345
    assert is_json(non_string) is False
