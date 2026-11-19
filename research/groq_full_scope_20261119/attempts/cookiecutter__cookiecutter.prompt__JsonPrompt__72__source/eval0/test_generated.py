import json
import pytest
from cookiecutter.prompt import JsonPrompt


def test_process_response_valid_json(tmp_path):
    """JsonPrompt.process_response should parse a valid JSON string into a dict."""
    # Prepare a JSON string with nested structures
    data = {"name": "Alice", "age": 30, "skills": ["python", "testing"]}
    json_str = json.dumps(data)

    # Call the method under test
    result = JsonPrompt.process_response(json_str)

    # Assert that the result is a dict and matches the original data
    assert isinstance(result, dict)
    assert result == data
    # Ensure nested list is preserved
    assert result["skills"] == ["python", "testing"]


def test_process_response_invalid_json():
    """JsonPrompt.process_response should raise a ValueError for malformed JSON."""
    # Malformed JSON (missing closing brace)
    bad_json = '{"name": "Bob", "age": 25'

    # Expect a ValueError when parsing
    with pytest.raises(ValueError):
        JsonPrompt.process_response(bad_json)


def test_process_response_empty_string():
    """JsonPrompt.process_response should raise a ValueError when given an empty string."""
    # Empty string is not valid JSON
    empty = ""

    with pytest.raises(ValueError):
        JsonPrompt.process_response(empty)
