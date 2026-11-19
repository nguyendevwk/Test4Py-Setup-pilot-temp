import json
import pytest
from cookiecutter.prompt import process_json
from rich.prompt import InvalidResponse

def test_process_json_valid_dict():
    # Normal case: a simple JSON object
    json_str = '{"name": "Alice", "age": 30}'
    result = process_json(json_str)
    assert isinstance(result, dict)
    assert result == {"name": "Alice", "age": 30}

def test_process_json_empty_dict_and_order():
    # Boundary case: empty JSON object and order preservation
    json_str = '{}'
    result = process_json(json_str)
    assert result == {}
    # Ensure the returned type preserves order (OrderedDict)
    assert type(result).__name__ == "OrderedDict"

def test_process_json_invalid_and_non_dict():
    # Error case: malformed JSON
    with pytest.raises(InvalidResponse) as excinfo:
        process_json('{"name": "Bob", "age": }')
    assert 'Unable to decode to JSON.' in str(excinfo.value)

    # Error case: valid JSON but not a dict (e.g., a list)
    with pytest.raises(InvalidResponse) as excinfo:
        process_json('["a", "b", "c"]')
    assert 'Requires JSON dict.' in str(excinfo.value)
