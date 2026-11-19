import json
import pytest
from cookiecutter.prompt import JsonPrompt


def test_process_response_valid_json():
    """JsonPrompt.process_response should return a dict for a valid JSON string."""
    json_str = '{"name": "Alice", "age": 30, "skills": ["python", "testing"]}'
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["skills"] == ["python", "testing"]


def test_process_response_empty_string_raises():
    """An empty string is not valid JSON and should raise a ValueError."""
    with pytest.raises(ValueError):
        JsonPrompt.process_response("")


def test_process_response_invalid_json_raises():
    """Malformed JSON should raise a ValueError with an informative message."""
    malformed = '{"name": "Bob", "age": 25'  # missing closing brace
    with pytest.raises(ValueError) as excinfo:
        JsonPrompt.process_response(malformed)
    assert "Expecting" in str(excinfo.value) or "JSON" in str(excinfo.value)
