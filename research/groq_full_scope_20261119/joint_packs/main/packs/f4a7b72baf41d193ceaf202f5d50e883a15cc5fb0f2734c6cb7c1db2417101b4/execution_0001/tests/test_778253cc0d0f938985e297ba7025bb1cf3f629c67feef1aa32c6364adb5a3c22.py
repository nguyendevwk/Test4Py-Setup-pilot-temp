import json
import pytest
from cookiecutter.prompt import process_json
from rich.prompt import InvalidResponse

def test_process_json_valid_dict():
    """Normal case: valid JSON dict is returned unchanged."""
    data = {"name": "Alice", "age": 30}
    json_str = json.dumps(data)
    result = process_json(json_str)
    assert isinstance(result, dict)
    assert result == data
    # Ensure the order is preserved (OrderedDict)
    assert list(result.keys()) == ["name", "age"]

def test_process_json_boundary_empty_dict():
    """Boundary case: empty JSON object is accepted."""
    json_str = "{}"
    result = process_json(json_str)
    assert result == {}
    assert isinstance(result, dict)

def test_process_json_error_invalid_json_and_non_dict():
    """Error cases: malformed JSON and non-dict JSON raise InvalidResponse."""
    # Malformed JSON
    malformed = "{name: Alice}"  # missing quotes
    with pytest.raises(InvalidResponse) as excinfo:
        process_json(malformed)
    assert "Unable to decode to JSON." in str(excinfo.value)

    # Valid JSON but not a dict
    json_list = '["a", "b"]'
    with pytest.raises(InvalidResponse) as excinfo:
        process_json(json_list)
    assert "Requires JSON dict." in str(excinfo.value)
