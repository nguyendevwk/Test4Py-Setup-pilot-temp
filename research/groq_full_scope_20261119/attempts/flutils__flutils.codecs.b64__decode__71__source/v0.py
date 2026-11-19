import pytest
from flutils.codecs.b64 import decode

def test_decode_normal_bytes_and_memoryview():
    # Normal bytes input
    data_bytes = b"hello world"
    result_str, consumed = decode(data_bytes)
    assert result_str == "aGVsbG8gd29ybGQ="
    assert consumed == len(data_bytes)

    # Same data as bytearray
    data_bytearray = bytearray(data_bytes)
    result_str_ba, consumed_ba = decode(data_bytearray)
    assert result_str_ba == result_str
    assert consumed_ba == len(data_bytearray)

    # Same data as memoryview
    data_memview = memoryview(data_bytes)
    result_str_mv, consumed_mv = decode(data_memview)
    assert result_str_mv == result_str
    assert consumed_mv == len(data_memview)

def test_decode_empty_input():
    # Boundary case: empty input should return empty string and zero consumed
    empty = b""
    result_str, consumed = decode(empty)
    assert result_str == ""
    assert consumed == 0

def test_decode_invalid_input_type():
    # Passing an invalid type should raise a TypeError
    with pytest.raises(TypeError):
        decode(12345)
