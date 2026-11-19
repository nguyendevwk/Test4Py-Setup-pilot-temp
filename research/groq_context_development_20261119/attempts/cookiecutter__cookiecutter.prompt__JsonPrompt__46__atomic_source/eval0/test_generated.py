import json
import pytest
from cookiecutter.prompt import JsonPrompt


def test_process_response_valid_json_returns_dict():
    """A valid JSON string should be parsed into a dictionary."""
    json_str = '{"name": "Alice", "age": 30}'
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result == {"name": "Alice", "age": 30}


def test_process_response_empty_object_boundary():
    """An empty JSON object should return an empty dictionary."""
    json_str = "{}"
    result = JsonPrompt.process_response(json_str)
    assert result == {}


def test_process_response_invalid_json_raises():
    """An invalid JSON string should raise a JSONDecodeError."""
    invalid_json = '{"name": "Bob", "age": 25'  # missing closing brace
    with pytest.raises(json.JSONDecodeError):
        JsonPrompt.process_response(invalid_json)
