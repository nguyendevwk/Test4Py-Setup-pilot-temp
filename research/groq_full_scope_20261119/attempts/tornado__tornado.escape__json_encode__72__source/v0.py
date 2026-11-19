import json
import pytest
from tornado.escape import json_encode

def test_json_encode_escapes_script_closing_tag():
    # Input containing a closing script tag should be escaped
    data = {"msg": "Hello </script>"}
    encoded = json_encode(data)
    # The output must be valid JSON and must not contain the literal "</"
    assert isinstance(encoded, str)
    assert json.loads(encoded) == data
    assert "</" not in encoded
    assert "<\\/script>" in encoded

def test_json_encode_preserves_other_characters_and_structure():
    # Input with various data types should be encoded correctly
    data = {
        "int": 42,
        "float": 3.14,
        "bool": True,
        "none": None,
        "list": [1, 2, 3],
        "nested": {"a": "b"},
    }
    encoded = json_encode(data)
    # The encoded string should be a valid JSON representation
    decoded = json.loads(encoded)
    assert decoded == data
    # Ensure that no unintended escaping occurs
    assert "<\\/script>" not in encoded
    assert "</" not in encoded

def test_json_encode_raises_on_non_serializable_object():
    # Objects that json.dumps cannot serialize should raise a TypeError
    class Unserializable:
        pass
    obj = Unserializable()
    with pytest.raises(TypeError):
        json_encode(obj)
