import json
import pytest
from cookiecutter.prompt import JsonPrompt, process_json
from rich.prompt import InvalidResponse

def test_process_response_valid_json(tmp_path):
    # Normal case: a simple JSON dict
    json_str = '{"key": "value", "number": 42}'
    result = JsonPrompt.process_response(json_str)
    assert isinstance(result, dict)
    assert result == {"key": "value", "number": 42}

def test_process_response_empty_dict(tmp_path):
    # Boundary case: empty JSON object
    json_str = '{}'
    result = JsonPrompt.process_response(json_str)
    assert result == {}
    assert isinstance(result, dict)

def test_process_response_invalid_json_and_non_dict(tmp_path):
    # Error cases: malformed JSON and JSON that is not a dict
    malformed = '{"key": "value",}'          # trailing comma
    not_dict = '["a", "b", "c"]'             # JSON array

    with pytest.raises(InvalidResponse) as exc1:
        process_json(malformed)
    assert "Unable to decode to JSON." in str(exc1.value)

    with pytest.raises(InvalidResponse) as exc2:
        process_json(not_dict)
    assert "Requires JSON dict." in str(exc2.value)
