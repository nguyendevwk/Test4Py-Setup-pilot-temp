import json
import pytest
from cookiecutter.prompt import JsonPrompt


def test_process_response_valid_json():
    """A well‑formed JSON string should be parsed into a dict."""
    json_str = '{"name": "Alice", "age": 30, "skills": ["python", "testing"]}'
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result == {"name": "Alice", "age": 30, "skills": ["python", "testing"]}


def test_process_response_invalid_json_raises():
    """An invalid JSON string should raise a ValueError."""
    invalid_json = '{"name": "Bob", "age": 25'  # missing closing brace
    with pytest.raises(ValueError):
        JsonPrompt.process_response(invalid_json)


def test_process_response_empty_string_returns_empty_dict():
    """An empty string should be interpreted as an empty JSON object."""
    empty_input = ""
    result = JsonPrompt.process_response(empty_input)
    assert result == {}
