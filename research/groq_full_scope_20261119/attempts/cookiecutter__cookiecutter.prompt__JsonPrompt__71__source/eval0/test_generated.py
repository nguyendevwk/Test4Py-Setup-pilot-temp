import json
import pytest
from cookiecutter.prompt import JsonPrompt

def test_process_response_valid_json():
    """Process a well‑formed JSON string and verify the resulting dict."""
    json_str = '{"name": "Alice", "age": 30, "skills": ["python", "testing"]}'
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["skills"] == ["python", "testing"]

def test_process_response_empty_string():
    """An empty string should raise a ValueError indicating invalid JSON."""
    with pytest.raises(ValueError) as excinfo:
        JsonPrompt.process_response("")
    assert "Expecting value" in str(excinfo.value)

def test_process_response_malformed_json():
    """A malformed JSON string should raise a ValueError with a clear message."""
    malformed = '{"name": "Bob", "age": 25'  # missing closing brace
    with pytest.raises(ValueError) as excinfo:
        JsonPrompt.process_response(malformed)
    assert "Expecting" in str(excinfo.value)
