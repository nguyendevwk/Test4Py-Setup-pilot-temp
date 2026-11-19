import pytest
from flutils.codecs.raw_utf8_escape import decode


def test_decode_normal_escaped_utf8():
    # Escaped hex for "Hello"
    data = b"\\x48\\x65\\x6c\\x6c\\x6f"
    result, consumed = decode(data)
    assert result == "Hello"
    assert consumed == len(data)


def test_decode_empty_input():
    data = b""
    result, consumed = decode(data)
    assert result == ""
    assert consumed == 0


def test_decode_invalid_utf8_raises():
    # \x80 is an invalid start byte for UTF‑8
    data = b"\\x80"
    with pytest.raises(UnicodeDecodeError) as excinfo:
        decode(data)
    # Ensure the error is raised from our custom codec
    assert excinfo.value.args[0] == "eutf8h"
    # The error should reference the original data bytes
    assert excinfo.value.object == b"\x80"
