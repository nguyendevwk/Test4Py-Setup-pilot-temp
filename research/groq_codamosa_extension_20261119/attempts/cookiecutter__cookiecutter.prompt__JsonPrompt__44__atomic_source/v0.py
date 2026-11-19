import json
import pytest
from cookiecutter.prompt import JsonPrompt

def test_process_response_valid_json(tmp_path):
    # Arrange: create a simple JSON string
    data = {"name": "Alice", "age": 30}
    json_str = json.dumps(data)

    # Act: process the JSON string
    result = JsonPrompt.process_response(json_str)

    # Assert: the result is a dict equal to the original data
    assert isinstance(result, dict)
    assert result == data

def test_process_response_invalid_json():
    # Arrange: an invalid JSON string
    invalid_json = "{name: Alice, age: 30}"  # missing quotes around keys

    # Act & Assert: processing should raise a JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        JsonPrompt.process_response(invalid_json)

def test_process_response_nested_json():
    # Arrange: a nested JSON structure
    nested = {"user": {"id": 1, "roles": ["admin", "user"]}, "active": True}
    json_str = json.dumps(nested)

    # Act: process the nested JSON string
    result = JsonPrompt.process_response(json_str)

    # Assert: the result matches the nested structure
    assert isinstance(result, dict)
    assert result["user"]["id"] == 1
    assert result["user"]["roles"] == ["admin", "user"]
    assert result["active"] is True
