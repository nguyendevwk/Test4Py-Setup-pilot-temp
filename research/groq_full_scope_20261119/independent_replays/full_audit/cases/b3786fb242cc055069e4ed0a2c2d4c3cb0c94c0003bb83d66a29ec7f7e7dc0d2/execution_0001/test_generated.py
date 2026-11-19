import pytest
import base64
from flutils.codecs.b64 import decode


def test_decode_bytes_and_bytearray_and_memoryview(tmp_path):
    # Prepare data in three different byte-like forms
    original = b"Hello, World!"
    bytearray_data = bytearray(original)
    memoryview_data = memoryview(original)

    # Expected base64 string
    expected = base64.b64encode(original).decode("utf-8")

    # Test with bytes
    result_bytes, consumed_bytes = decode(original)
    assert result_bytes == expected
    assert consumed_bytes == len(original)

    # Test with bytearray
    result_ba, consumed_ba = decode(bytearray_data)
    assert result_ba == expected
    assert consumed_ba == len(bytearray_data)

    # Test with memoryview
    result_mv, consumed_mv = decode(memoryview_data)
    assert result_mv == expected
    assert consumed_mv == len(memoryview_data)


def test_decode_empty_input():
    # Empty input should return an empty string and zero consumed bytes
    empty = b""
    result, consumed = decode(empty)
    assert result == ""
    assert consumed == 0


def test_decode_invalid_input_type():
    # Passing a string (not bytes-like) should raise a TypeError
    with pytest.raises(TypeError):
        decode("not bytes")
