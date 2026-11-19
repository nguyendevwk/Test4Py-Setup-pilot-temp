import pytest
from httpie.core import decode_raw_args

def test_decode_raw_args_normal():
    # Mixed list of str and bytes, all decodable
    args = ["hello", b"world", "foo", b"bar"]
    decoded = decode_raw_args(args, "utf-8")
    assert decoded == ["hello", "world", "foo", "bar"]
    # Ensure original list is unchanged
    assert args == ["hello", b"world", "foo", b"bar"]

def test_decode_raw_args_empty_and_unicode():
    # Empty list should return empty list
    assert decode_raw_args([], "utf-8") == []
    # Unicode characters that require multi-byte encoding
    args = [b"\xe2\x98\x83"]  # snowman in UTF-8
    decoded = decode_raw_args(args, "utf-8")
    assert decoded == ["☃"]

def test_decode_raw_args_invalid_encoding():
    # Bytes that are invalid for the given encoding should raise UnicodeDecodeError
    args = [b"\xff"]
    with pytest.raises(UnicodeDecodeError):
        decode_raw_args(args, "utf-8")
