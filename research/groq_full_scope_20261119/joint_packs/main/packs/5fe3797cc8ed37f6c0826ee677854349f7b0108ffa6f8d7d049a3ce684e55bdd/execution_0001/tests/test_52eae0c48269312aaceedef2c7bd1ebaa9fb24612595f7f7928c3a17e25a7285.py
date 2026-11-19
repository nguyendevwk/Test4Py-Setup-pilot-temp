import json
import pytest
from tornado.escape import json_encode

def test_json_encode_basic_and_escape():
    # Basic encoding of a simple string
    result = json_encode("hello")
    assert result == json.dumps("hello")
    # Ensure that the output never contains the sequence '</'
    assert "</" not in result
    # Verify that a string containing '</' is escaped
    dangerous = "foo</script>"
    escaped = json_encode(dangerous)
    assert "<\\/" in escaped
    assert "</script>" not in escaped
    # The escaped string should still be valid JSON
    assert json.loads(escaped) == dangerous

def test_json_encode_complex_structure():
    # Complex nested structure with various types
    data = {
        "list": [1, 2, {"key": "value</test>"}],
        "bool": True,
        "none": None,
        "float": 3.14,
    }
    encoded = json_encode(data)
    # No '</' sequence should appear
    assert "</" not in encoded
    # The encoded string should decode back to the original data
    decoded = json.loads(encoded)
    assert decoded == data
    # Ensure that the special substring was escaped
    assert "<\\/" in encoded

def test_json_encode_non_serializable_object():
    # Objects that json.dumps cannot serialize should raise TypeError
    class Unserializable:
        pass
    obj = Unserializable()
    with pytest.raises(TypeError):
        json_encode(obj)
