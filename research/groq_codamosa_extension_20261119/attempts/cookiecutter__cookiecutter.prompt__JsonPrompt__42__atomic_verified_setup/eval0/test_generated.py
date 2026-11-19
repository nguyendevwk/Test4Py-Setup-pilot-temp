import json
import pytest
from cookiecutter.prompt import JsonPrompt

def test_process_response_valid_json():
    """A valid JSON string should be parsed into a dict."""
    json_str = '{"name": "Alice", "age": 30}'
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result == {"name": "Alice", "age": 30}

def test_process_response_empty_string_returns_default():
    """An empty string should return the default value (None)."""
    result = JsonPrompt.process_response("")
    assert result is None

def test_process_response_invalid_json_raises():
    """An invalid JSON string should raise a ValueError with a clear message."""
    invalid_json = "{name: Alice, age: 30}"  # missing quotes
    with pytest.raises(ValueError) as excinfo:
        JsonPrompt.process_response(invalid_json)
    assert "Expecting property name" in str(excinfo.value)
