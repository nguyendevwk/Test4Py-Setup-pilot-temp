import json
import pytest
from cookiecutter.prompt import JsonPrompt


def test_process_response_valid_json(tmp_path):
    """JsonPrompt.process_response should parse a valid JSON string into a dict."""
    # Arrange: a simple JSON string
    json_str = '{"name": "Alice", "age": 30}'
    # Act
    result = JsonPrompt.process_response(json_str)
    # Assert
    assert isinstance(result, dict)
    assert result == {"name": "Alice", "age": 30}
    # Ensure that nested structures are preserved
    nested_str = '{"data": {"items": [1, 2, 3], "flag": true}}'
    nested_result = JsonPrompt.process_response(nested_str)
    assert nested_result == {"data": {"items": [1, 2, 3], "flag": True}}


def test_process_response_invalid_json_raises():
    """JsonPrompt.process_response should raise a ValueError for malformed JSON."""
    # Arrange: malformed JSON (missing closing brace)
    bad_json = '{"name": "Bob", "age": 25'
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        JsonPrompt.process_response(bad_json)
    # The exception message should indicate JSON decoding error
    assert "Expecting" in str(excinfo.value) or "JSON" in str(excinfo.value)


def test_process_response_boundary_empty_string():
    """JsonPrompt.process_response should raise a ValueError when given an empty string."""
    empty_str = ""
    with pytest.raises(ValueError) as excinfo:
        JsonPrompt.process_response(empty_str)
    # The error should mention that the input is not valid JSON
    assert "Expecting" in str(excinfo.value) or "JSON" in str(excinfo.value)
