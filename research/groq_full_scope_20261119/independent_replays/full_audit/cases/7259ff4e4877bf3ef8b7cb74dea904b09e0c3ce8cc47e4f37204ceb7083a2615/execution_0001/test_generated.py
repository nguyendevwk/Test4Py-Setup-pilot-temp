import json
import pytest
from cookiecutter.prompt import process_json
from rich.prompt import InvalidResponse

def test_process_json_valid_dict(tmp_path):
    # Create a JSON string that represents a dictionary
    data = {"name": "Alice", "age": 30}
    json_str = json.dumps(data)
    result = process_json(json_str)
    # The result should be an OrderedDict preserving insertion order
    assert isinstance(result, dict)
    assert list(result.keys()) == ["name", "age"]
    assert result["name"] == "Alice"
    assert result["age"] == 30

def test_process_json_invalid_json_raises():
    # Provide a malformed JSON string
    bad_json = '{"name": "Bob", "age": 25'  # missing closing brace
    with pytest.raises(InvalidResponse) as excinfo:
        process_json(bad_json)
    # The exception message should indicate a decoding error
    assert "Unable to decode to JSON." in str(excinfo.value)

def test_process_json_non_dict_raises():
    # Provide a JSON string that decodes to a list, not a dict
    bad_type = json.dumps([1, 2, 3])
    with pytest.raises(InvalidResponse) as excinfo:
        process_json(bad_type)
    # The exception message should indicate that a dict is required
    assert "Requires JSON dict." in str(excinfo.value)
