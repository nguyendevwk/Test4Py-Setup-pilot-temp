import base64
import pytest
from flutils.codecs.b64 import decode

def test_decode_normal_bytes():
    """Normal case: bytes input should return correct base64 string and length."""
    data = b"hello world"
    expected_b64 = base64.b64encode(data).decode("utf-8")
    result_str, consumed = decode(data)
    assert result_str == expected_b64
    assert consumed == len(data)

def test_decode_empty_input():
    """Boundary case: empty bytes should return empty string and zero length."""
    data = b""
    result_str, consumed = decode(data)
    assert result_str == ""
    assert consumed == 0

def test_decode_invalid_type_raises():
    """Error case: passing a non-byte-like object should raise TypeError."""
    with pytest.raises(TypeError):
        decode("not bytes")
