import pytest
from flutils.codecs.b64 import decode


def test_decode_bytes_and_memoryview(tmp_path):
    """Test that decode works for bytes, bytearray and memoryview."""
    original = b"Hello, world!"
    # bytes
    result_bytes, consumed_bytes = decode(original)
    assert result_bytes == "SGVsbG8sIHdvcmxkIQ=="
    assert consumed_bytes == len(original)

    # bytearray
    result_ba, consumed_ba = decode(bytearray(original))
    assert result_ba == result_bytes
    assert consumed_ba == len(original)

    # memoryview
    result_mv, consumed_mv = decode(memoryview(original))
    assert result_mv == result_bytes
    assert consumed_mv == len(original)


def test_decode_empty_input():
    """Decoding an empty input should return an empty string and zero bytes consumed."""
    result, consumed = decode(b"")
    assert result == ""
    assert consumed == 0


def test_decode_invalid_input():
    """Passing a non-byte string should raise a TypeError."""
    with pytest.raises(TypeError):
        decode("not bytes")
