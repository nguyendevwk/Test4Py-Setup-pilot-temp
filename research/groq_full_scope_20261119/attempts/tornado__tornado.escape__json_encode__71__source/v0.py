import json
import pytest
from tornado.escape import json_encode

def test_json_encode_escapes_script_closing_tag():
    # Normal case: ensure that the string "</script>" is escaped to "<\\/script>"
    data = {"key": "</script>"}
    encoded = json_encode(data)
    # The output should be a JSON string containing the escaped sequence
    assert encoded == '{"key":"<\\/script>"}'
    # Verify that decoding yields the original value
    assert json.loads(encoded) == data

def test_json_encode_handles_nested_structures_and_unicode():
    # Boundary case: nested lists and unicode characters
    data = {
        "list": [1, 2, {"inner": "value</test>"}],
        "unicode": "✓"
    }
    encoded = json_encode(data)
    # The escaped sequence should appear only once
    assert "<\\/test>" in encoded
    # The unicode character should be preserved
    assert "✓" in encoded
    # Decoding should recover the original structure
    assert json.loads(encoded) == data

def test_json_encode_raises_on_non_serializable_object():
    # Error case: passing a non-JSON-serializable object should raise TypeError
    class NotSerializable:
        pass
    with pytest.raises(TypeError):
        json_encode(NotSerializable())
