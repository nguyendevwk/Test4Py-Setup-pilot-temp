import pytest
from flutils.codecs.raw_utf8_escape import decode
from typing import UserString

def test_decode_normal_bytes():
    # Input: escaped UTF-8 bytes for "Hello, 世界" (H e l l o , space + Chinese)
    # UTF-8 bytes for "Hello, 世界" are:
    # 48 65 6c 6c 6f 2c 20 e4 b8 96 e7 95 8c
    # Escaped as b'\\x48\\x65\\x6c\\x6c\\x6f\\x2c\\x20\\xe4\\xb8\\x96\\xe7\\x95\\x8c'
    escaped = b'\\x48\\x65\\x6c\\x6c\\x6f\\x2c\\x20\\xe4\\xb8\\x96\\xe7\\x95\\x8c'
    result, consumed = decode(escaped)
    assert result == "Hello, 世界"
    assert consumed == len(escaped)

def test_decode_empty_input():
    # Empty input should return empty string and zero consumed bytes
    result, consumed = decode(b'')
    assert result == ""
    assert consumed == 0

def test_decode_invalid_utf8_raises():
    # Escaped bytes that decode to invalid UTF-8 sequence:
    # \x80 is a continuation byte without a leading byte
    invalid = b'\\x80'
    with pytest.raises(UnicodeDecodeError) as excinfo:
        decode(invalid)
    # Verify that the exception is raised with the correct codec name and data
    e = excinfo.value
    assert e.codec == 'eutf8h'
    assert e.object == b'\x80'
    # The start and end should refer to the problematic byte
    assert e.start == 0
    assert e.end == 1
    # Reason should indicate an unexpected continuation byte
    assert "unexpected" in e.reason.lower()
