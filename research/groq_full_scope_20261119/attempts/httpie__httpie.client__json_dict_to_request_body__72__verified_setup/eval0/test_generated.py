import json
import pytest
from httpie.client import json_dict_to_request_body

def test_json_dict_to_request_body_normal_dict():
    payload = {"name": "Alice", "age": 30}
    result = json_dict_to_request_body(payload)
    # The result should be a JSON string representation of the dict
    assert result == json.dumps(payload)
    # Ensure that the result is a string
    assert isinstance(result, str)

def test_json_dict_to_request_body_empty_dict():
    payload = {}
    result = json_dict_to_request_body(payload)
    # An empty dict should produce an empty string
    assert result == ""
    # The result should still be a string type
    assert isinstance(result, str)

def test_json_dict_to_request_body_top_level_list_unwrapped():
    payload = {"data": [1, 2, 3]}
    # The function unwraps a top-level list if present; here the top-level is a dict,
    # so it should remain unchanged and be JSON-encoded.
    result = json_dict_to_request_body(payload)
    assert result == json.dumps(payload)
    # Test that a top-level list is unwrapped correctly
    list_payload = [1, 2, 3]
    result_list = json_dict_to_request_body(list_payload)
    assert result_list == json.dumps(list_payload)
