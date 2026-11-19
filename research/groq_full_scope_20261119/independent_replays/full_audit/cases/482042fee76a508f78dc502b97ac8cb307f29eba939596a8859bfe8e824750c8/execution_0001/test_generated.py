import pytest
from httpie.core import decode_raw_args

def test_decode_raw_args_mixed_types(tmp_path):
    # Prepare a mix of string and byte arguments
    args = ["hello", b"world", "foo", b"bar"]
    # Use UTF-8 encoding which can decode all bytes
    decoded = decode_raw_args(args, "utf-8")
    assert decoded == ["hello", "world", "foo", "bar"]
    # Ensure original list is unchanged
    assert args == ["hello", b"world", "foo", b"bar"]

def test_decode_raw_args_empty_list():
    # An empty list should return an empty list without errors
    assert decode_raw_args([], "utf-8") == []

def test_decode_raw_args_invalid_bytes():
    # Bytes that cannot be decoded with the given encoding should raise UnicodeDecodeError
    bad_bytes = [b"\xff\xfe\xfa"]
    with pytest.raises(UnicodeDecodeError):
        decode_raw_args(bad_bytes, "utf-8")
