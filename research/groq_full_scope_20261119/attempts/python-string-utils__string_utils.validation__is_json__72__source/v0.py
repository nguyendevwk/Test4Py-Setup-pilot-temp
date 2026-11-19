import json
import pytest
from string_utils.validation import is_json

def test_is_json_valid_objects_and_arrays():
    # Valid JSON objects and arrays should return True
    assert is_json('{"name": "Peter"}') is True
    assert is_json('[1, 2, 3]') is True
    # Nested structures
    nested = '{"data": {"items": [1, 2, 3], "valid": true}}'
    assert is_json(nested) is True

def test_is_json_invalid_strings_and_non_json():
    # Strings that are not valid JSON or not full strings should return False
    assert is_json('{nope}') is False
    assert is_json('Just a plain string') is False
    # JSON with trailing characters
    assert is_json('{"a":1} extra') is False
    # Empty string
    assert is_json('') is False

def test_is_json_boundary_and_error_conditions():
    # Boundary: very large number that might cause OverflowError
    large_number = str(10**400)  # too large for JSON number
    json_str = f'{{"big": {large_number}}}'
    # json.loads will raise OverflowError, is_json should return False
    assert is_json(json_str) is False

    # Boundary: JSON with null value
    assert is_json('{"key": null}') is True

    # Boundary: JSON with boolean values
    assert is_json('{"flag": true}') is True
    assert is_json('{"flag": false}') is True
