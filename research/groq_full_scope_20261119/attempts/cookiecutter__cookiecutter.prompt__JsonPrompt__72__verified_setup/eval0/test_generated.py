import json
import pytest
from cookiecutter.prompt import JsonPrompt


def test_process_response_valid_json():
    """JsonPrompt.process_response should parse a valid JSON string into a dict."""
    json_str = '{"name": "Alice", "age": 30, "skills": ["python", "testing"]}'
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["skills"] == ["python", "testing"]


def test_process_response_invalid_json_raises():
    """An invalid JSON string should raise a ValueError."""
    invalid_json = '{"name": "Bob", "age": 25'  # missing closing brace
    with pytest.raises(ValueError):
        JsonPrompt.process_response(invalid_json)


def test_process_response_boundary_empty_string():
    """An empty string should raise a ValueError indicating invalid JSON."""
    with pytest.raises(ValueError):
        JsonPrompt.process_response("")
