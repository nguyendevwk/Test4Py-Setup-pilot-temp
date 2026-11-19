import pytest
from flutils.codecs.raw_utf8_escape import decode
from typing import UserString

def test_decode_normal_bytes():
    # Input: escaped UTF-8 bytes for "Hello, 世界" (Chinese characters)
    # "Hello, " is ASCII, "世界" in UTF-8 is e4 b8 96 e7 95 8c
    # Escaped as \xE4\xB8\x96\xE7\x95\x8C
    escaped = b"Hello, \\xE4\\xB8\\x96\\xE7\\x95\\x8C"
    result, consumed = decode(escaped)
    assert result == "Hello, 世界"
    assert consumed == len(escaped)

def test_decode_empty_input():
    # Empty input should return empty string and zero bytes consumed
    result, consumed = decode(b"")
    assert result == ""
    assert consumed == 0

def test_decode_invalid_utf8_raises():
    # Provide an escaped sequence that is not valid UTF-8
    # e.g., \xFF is invalid in UTF-8
    escaped = b"\\xFF"
    with pytest.raises(UnicodeDecodeError) as excinfo:
        decode(escaped)
    # The exception should be raised with the custom error message
    assert excinfo.value.args[0] == 'eutf8h'
    # The original data should be present in the exception
    assert excinfo.value.object == bytes(escaped)
