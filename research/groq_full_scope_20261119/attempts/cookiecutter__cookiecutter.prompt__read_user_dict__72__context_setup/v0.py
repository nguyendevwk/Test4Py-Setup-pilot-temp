import json
import pytest
from cookiecutter.prompt import read_user_dict, process_json, JsonPrompt, DEFAULT_DISPLAY
from rich.prompt import InvalidResponse

def test_read_user_dict_valid_json(monkeypatch):
    # Simulate user input of a valid JSON dict
    monkeypatch.setattr(JsonPrompt, "ask", lambda *args, **kwargs: {"key": "value"})
    result = read_user_dict("my_var", {"default": "dict"}, prompts={"my_var": "Enter dict"})
    assert isinstance(result, dict)
    assert result == {"key": "value"}

def test_process_json_empty_dict():
    # Empty JSON object should return an empty OrderedDict
    empty_json = "{}"
    result = process_json(empty_json)
    assert isinstance(result, dict)
    assert result == {}

def test_process_json_invalid_non_dict(monkeypatch):
    # Input that parses to a list should raise InvalidResponse
    invalid_json = '["a", "b"]'
    with pytest.raises(InvalidResponse) as excinfo:
        process_json(invalid_json)
    assert "Requires JSON dict." in str(excinfo.value)
