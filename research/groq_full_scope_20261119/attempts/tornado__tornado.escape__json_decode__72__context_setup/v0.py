import json
import pytest
from tornado.escape import json_decode

def test_json_decode_with_string():
    # Normal JSON string input
    json_str = '{"name": "Alice", "age": 30, "hobbies": ["reading", "cycling"]}'
    result = json_decode(json_str)
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["hobbies"] == ["reading", "cycling"]

def test_json_decode_with_bytes():
    # JSON bytes input should be decoded correctly
    json_bytes = b'{"active": true, "count": 42}'
    result = json_decode(json_bytes)
    assert isinstance(result, dict)
    assert result["active"] is True
    assert result["count"] == 42

def test_json_decode_invalid_json_raises():
    # Invalid JSON should raise a JSONDecodeError
    invalid_json = '{"missing_end": true'
    with pytest.raises(json.JSONDecodeError):
        json_decode(invalid_json)
