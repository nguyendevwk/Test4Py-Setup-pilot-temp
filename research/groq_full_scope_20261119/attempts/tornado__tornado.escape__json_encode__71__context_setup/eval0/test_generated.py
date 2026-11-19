import json
import pytest
from tornado.escape import json_encode


def test_json_encode_escapes_script_closing_tag():
    """
    Verify that json_encode replaces the substring '</' with '<\/'
    to avoid prematurely closing a <script> tag.
    """
    data = {"key": "value", "script": "</script>"}
    encoded = json_encode(data)
    # The original string '</script>' should appear as '<\/script>' in the JSON output
    assert "<\\/script>" in encoded
    # Ensure that the rest of the JSON is valid
    decoded = json.loads(encoded)
    assert decoded == data


def test_json_encode_handles_complex_structure():
    """
    Ensure that json_encode correctly serializes nested structures
    and preserves data types.
    """
    data = {
        "list": [1, 2, {"nested": "text"}],
        "bool": True,
        "none": None,
        "float": 3.14,
    }
    encoded = json_encode(data)
    # The output should be a valid JSON string
    decoded = json.loads(encoded)
    assert decoded == data
    # Check that the string representation contains the expected keys
    for key in data:
        assert f'"{key}"' in encoded


def test_json_encode_raises_on_non_serializable_object():
    """
    json_encode should raise a TypeError when given an object that
    cannot be serialized by the standard json module.
    """
    class Unserializable:
        pass

    obj = Unserializable()
    with pytest.raises(TypeError):
        json_encode(obj)
