import json
import pytest
from cookiecutter.prompt import JsonPrompt, process_json
from rich.prompt import InvalidResponse

def test_process_response_valid_json(tmp_path):
    """Process a valid JSON string and verify the resulting dict."""
    # Create a temporary file to simulate user input
    json_str = json.dumps({"key": "value", "number": 42})
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result == {"key": "value", "number": 42}

def test_process_response_invalid_json_raises(tmp_path):
    """Ensure that malformed JSON triggers an InvalidResponse exception."""
    malformed = '{"key": "value", "missing_end":'
    with pytest.raises(InvalidResponse) as excinfo:
        JsonPrompt.process_response(malformed)
    assert "Unable to decode to JSON." in str(excinfo.value)

def test_process_response_non_dict_raises(tmp_path):
    """Verify that JSON that is not a dict raises an InvalidResponse."""
    json_list = json.dumps([1, 2, 3])
    with pytest.raises(InvalidResponse) as excinfo:
        JsonPrompt.process_response(json_list)
    assert "Requires JSON dict." in str(excinfo.value)
