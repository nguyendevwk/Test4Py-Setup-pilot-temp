import json
import pytest
from cookiecutter.prompt import process_json
from rich.prompt import InvalidResponse


def test_process_json_valid_dict(tmp_path):
    # Normal case: a simple JSON dict
    data = {"name": "Alice", "age": 30}
    json_str = json.dumps(data)
    result = process_json(json_str)
    assert isinstance(result, dict)
    assert result == data
    assert isinstance(result, type(data))  # preserves OrderedDict if used


def test_process_json_empty_dict(tmp_path):
    # Boundary case: empty JSON dict
    json_str = "{}"
    result = process_json(json_str)
    assert result == {}
    assert isinstance(result, dict)


def test_process_json_invalid_input(tmp_path):
    # Error cases: non-dict JSON and malformed JSON
    # Non-dict JSON (a list)
    with pytest.raises(InvalidResponse) as excinfo:
        process_json("[1, 2, 3]")
    assert "Requires JSON dict." in str(excinfo.value)

    # Malformed JSON
    with pytest.raises(InvalidResponse) as excinfo:
        process_json("{invalid json}")
    assert "Unable to decode to JSON." in str(excinfo.value)
