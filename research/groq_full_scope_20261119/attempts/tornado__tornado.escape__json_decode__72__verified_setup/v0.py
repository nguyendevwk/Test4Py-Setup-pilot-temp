import pytest
import json
from tornado.escape import json_decode

def test_json_decode_with_string():
    # Normal JSON string input
    data = {"name": "Alice", "age": 30, "skills": ["python", "testing"]}
    json_str = json.dumps(data)
    result = json_decode(json_str)
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["skills"] == ["python", "testing"]

def test_json_decode_with_bytes():
    # JSON bytes input should be decoded correctly
    data = [1, 2, 3, {"foo": "bar"}]
    json_bytes = json.dumps(data).encode("utf-8")
    result = json_decode(json_bytes)
    assert isinstance(result, list)
    assert result[0] == 1
    assert result[3]["foo"] == "bar"

def test_json_decode_invalid_json_raises():
    # Invalid JSON should raise a JSONDecodeError
    invalid_json = "{'missing_quotes': True}"  # single quotes are invalid in JSON
    with pytest.raises(json.JSONDecodeError):
        json_decode(invalid_json)
