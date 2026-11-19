import json
import pytest
from cookiecutter.prompt import process_json
from rich.prompt import InvalidResponse


def test_process_json_valid_dict(tmp_path):
    """process_json should return an OrderedDict for a valid JSON dict string."""
    data = {"name": "Alice", "age": 30}
    json_str = json.dumps(data)
    result = process_json(json_str)
    assert isinstance(result, dict)
    assert result == data
    assert list(result.keys()) == ["name", "age"]  # order preserved


def test_process_json_empty_dict(tmp_path):
    """An empty JSON object should be accepted and returned as an empty dict."""
    json_str = "{}"
    result = process_json(json_str)
    assert isinstance(result, dict)
    assert result == {}


def test_process_json_errors(tmp_path):
    """process_json should raise InvalidResponse for non-dict JSON or invalid JSON."""
    # Non-dict JSON (list)
    bad_json = '["a", "b"]'
    with pytest.raises(InvalidResponse) as excinfo:
        process_json(bad_json)
    assert "Requires JSON dict." in str(excinfo.value)

    # Invalid JSON syntax
    bad_json = '{"name": "Bob", "age": 25'  # missing closing brace
    with pytest.raises(InvalidResponse) as excinfo:
        process_json(bad_json)
    assert "Unable to decode to JSON." in str(excinfo.value)
