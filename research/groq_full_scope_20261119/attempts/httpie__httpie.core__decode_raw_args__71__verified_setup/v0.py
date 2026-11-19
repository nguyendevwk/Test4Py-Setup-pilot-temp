import pytest
from httpie.core import decode_raw_args

def test_decode_raw_args_normal_and_mixed_types():
    # Mixed list of strings and bytes
    args = ["hello", b"world", "foo", b"bar"]
    decoded = decode_raw_args(args, "utf-8")
    assert decoded == ["hello", "world", "foo", "bar"]
    # Ensure original list is unchanged
    assert args == ["hello", b"world", "foo", b"bar"]

def test_decode_raw_args_empty_list():
    # Empty input should return an empty list
    assert decode_raw_args([], "utf-8") == []

def test_decode_raw_args_invalid_encoding_raises():
    # Bytes that cannot be decoded with the given encoding should raise UnicodeDecodeError
    bad_bytes = b"\xff\xfe\xfa"
    with pytest.raises(UnicodeDecodeError):
        decode_raw_args([bad_bytes], "utf-8")
