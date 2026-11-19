import json
import pytest
from tornado.escape import json_encode


def test_json_encode_basic_dict():
    """json_encode should correctly encode a simple dictionary."""
    data = {"a": 1, "b": "text"}
    encoded = json_encode(data)
    # The output must be a valid JSON string that matches json.dumps
    assert encoded == json.dumps(data)
    # Ensure the result is a string
    assert isinstance(encoded, str)
    # The string should not contain the problematic sequence
    assert "</" not in encoded


def test_json_encode_escapes_forward_slashes():
    """json_encode must escape the sequence '</' to prevent script tag issues."""
    data = {"html": "<script></script>"}
    encoded = json_encode(data)
    # The original string contains '</', which should be escaped
    assert "<\\/" in encoded
    # The escaped sequence should not appear as '</'
    assert "</" not in encoded
    # The decoded JSON should match the original data
    assert json.loads(encoded) == data


def test_json_encode_non_serializable_raises():
    """json_encode should raise a TypeError when given an unserializable object."""
    class Unserializable:
        pass

    obj = Unserializable()
    with pytest.raises(TypeError):
        json_encode(obj)
