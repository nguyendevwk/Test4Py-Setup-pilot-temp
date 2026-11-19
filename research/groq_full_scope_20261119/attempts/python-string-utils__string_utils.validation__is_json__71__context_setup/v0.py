import json
import pytest
from string_utils.validation import is_json

def test_is_json_with_valid_dict_and_list():
    # Valid JSON objects should return True
    assert is_json('{"name": "Peter"}') is True
    assert is_json('[1, 2, 3]') is True
    # The parsed result must be a dict or list
    assert isinstance(json.loads('{"name": "Peter"}'), dict)
    assert isinstance(json.loads('[1, 2, 3]'), list)

def test_is_json_with_invalid_and_boundary_inputs():
    # Empty string or whitespace should be considered invalid
    assert is_json('') is False
    assert is_json('   ') is False
    # Malformed JSON should return False
    assert is_json('{nope}') is False
    assert is_json('{"name": "Peter"') is False
    # Non-string input should also return False
    assert is_json(123) is False
    assert is_json(None) is False

def test_is_json_with_large_and_nested_structures():
    # Very large JSON string should still be processed correctly
    large_dict = {"a": list(range(1000))}
    large_json = json.dumps(large_dict)
    assert is_json(large_json) is True
    # Nested structures
    nested_json = '{"outer": {"inner": [1, 2, {"deep": "value"}]}}'
    assert is_json(nested_json) is True
    # Ensure that the function does not raise on complex but valid JSON
    try:
        is_json(nested_json)
    except Exception as exc:
        pytest.fail(f"is_json raised an unexpected exception: {exc}")
