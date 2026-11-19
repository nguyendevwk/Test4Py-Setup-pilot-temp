import json
import pytest
from string_utils.validation import is_json

def test_is_json_valid_objects_and_arrays():
    # Valid JSON objects and arrays should return True
    assert is_json('{"name": "Alice", "age": 30}') is True
    assert is_json('[1, 2, 3, {"key": "value"}]') is True
    # Ensure that the function correctly parses nested structures
    nested = '{"outer": {"inner": [1, 2, 3]}}'
    assert is_json(nested) is True
    # The returned value must be a dict or list when parsed
    parsed = json.loads(nested)
    assert isinstance(parsed, dict)
    assert isinstance(parsed["outer"], dict)
    assert isinstance(parsed["outer"]["inner"], list)

def test_is_json_invalid_strings_and_non_json():
    # Strings that are not valid JSON should return False
    assert is_json('{"name": "Bob"') is False          # missing closing brace
    assert is_json('Just a plain string') is False
    assert is_json('12345') is False                   # number not wrapped in JSON object/array
    assert is_json('true') is False                    # boolean literal not wrapped
    # Empty string should also be False
    assert is_json('') is False

def test_is_json_boundary_and_error_handling():
    # Boundary: very large JSON string (but still valid)
    large_list = '[' + ','.join(['0'] * 1000) + ']'
    assert is_json(large_list) is True
    # Non-string input should be handled gracefully and return False
    assert is_json(42) is False
    assert is_json(None) is False
    # Input that causes json.loads to raise an exception (e.g., too large number)
    # Use a string that matches the regex but is not a valid JSON number
    invalid_number = '1e309'  # Infinity in JSON is not allowed
    assert is_json(invalid_number) is False
