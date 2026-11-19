import json
import pytest
from cookiecutter.prompt import JsonPrompt, process_json
from rich.prompt import InvalidResponse

def test_process_response_valid_json():
    """JsonPrompt.process_response should return a dict for valid JSON."""
    json_str = '{"key1": "value1", "key2": 2}'
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result == {"key1": "value1", "key2": 2}

def test_process_response_invalid_json_raises():
    """Invalid JSON string should raise InvalidResponse."""
    bad_json = '{"key1": "value1", "key2": 2'  # missing closing brace
    with pytest.raises(InvalidResponse) as excinfo:
        JsonPrompt.process_response(bad_json)
    assert "Unable to decode to JSON." in str(excinfo.value)

def test_process_response_non_dict_raises():
    """JSON that does not decode to a dict should raise InvalidResponse."""
    json_list = '["a", "b", "c"]'
    with pytest.raises(InvalidResponse) as excinfo:
        JsonPrompt.process_response(json_list)
    assert "Requires JSON dict." in str(excinfo.value)
