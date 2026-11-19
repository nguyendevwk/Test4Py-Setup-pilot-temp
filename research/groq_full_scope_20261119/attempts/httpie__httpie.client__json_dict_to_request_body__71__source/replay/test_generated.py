import json
import pytest
from httpie.client import json_dict_to_request_body

def test_json_dict_to_request_body_with_normal_dict():
    payload = {"name": "Alice", "age": 30}
    result = json_dict_to_request_body(payload)
    # The result should be a JSON string representation of the dict
    assert result == json.dumps(payload)
    # Ensure the result is a string
    assert isinstance(result, str)

def test_json_dict_to_request_body_with_empty_dict():
    payload = {}
    result = json_dict_to_request_body(payload)
    # An empty dict should produce an empty string
    assert result == ""
    # The result should still be a string type
    assert isinstance(result, str)

def test_json_dict_to_request_body_with_top_level_list():
    payload = [{"id": 1}, {"id": 2}]
    result = json_dict_to_request_body(payload)
    # The function unwraps top-level lists, so the result should be a JSON string of the list
    assert result == json.dumps(payload)
    # Ensure the result is a string
    assert isinstance(result, str)
