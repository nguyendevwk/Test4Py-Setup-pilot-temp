import json
import pytest
from tornado.escape import json_decode

def test_json_decode_with_string_and_bytes():
    # Normal case: decode a JSON string
    data_str = '{"name": "Alice", "age": 30}'
    result_str = json_decode(data_str)
    assert result_str == {"name": "Alice", "age": 30}

    # Same JSON provided as bytes
    data_bytes = b'{"name": "Bob", "age": 25}'
    result_bytes = json_decode(data_bytes)
    assert result_bytes == {"name": "Bob", "age": 25}

def test_json_decode_boundary_empty_and_null():
    # Empty JSON object
    empty_obj = '{}'
    assert json_decode(empty_obj) == {}

    # JSON null value
    null_value = 'null'
    assert json_decode(null_value) is None

def test_json_decode_invalid_input_raises():
    # Malformed JSON should raise a JSONDecodeError
    malformed = '{"name": "Charlie", "age": 40'  # missing closing brace
    with pytest.raises(json.JSONDecodeError):
        json_decode(malformed)

    # Non-JSON bytes should also raise
    non_json_bytes = b'not a json'
    with pytest.raises(json.JSONDecodeError):
        json_decode(non_json_bytes)
