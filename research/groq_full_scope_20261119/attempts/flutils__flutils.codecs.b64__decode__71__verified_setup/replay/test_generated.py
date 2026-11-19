import pytest
from flutils.codecs.b64 import decode
import base64


def test_decode_normal_bytes_and_variants():
    """Test that decode correctly encodes bytes, bytearray, and memoryview."""
    original = b"Hello, World!"
    # Direct bytes
    result_str, consumed = decode(original)
    assert result_str == base64.b64encode(original).decode("utf-8")
    assert consumed == len(original)

    # bytearray
    result_str_ba, consumed_ba = decode(bytearray(original))
    assert result_str_ba == result_str
    assert consumed_ba == len(original)

    # memoryview
    result_str_mv, consumed_mv = decode(memoryview(original))
    assert result_str_mv == result_str
    assert consumed_mv == len(original)


def test_decode_empty_input():
    """Test that an empty input returns an empty string and zero consumed."""
    empty = b""
    result_str, consumed = decode(empty)
    assert result_str == ""
    assert consumed == 0


def test_decode_invalid_input_raises_type_error():
    """Test that passing a non‑bytes-like object raises TypeError."""
    with pytest.raises(TypeError):
        decode("not bytes")  # str does not support buffer protocol
