import pytest
from flutils.codecs.raw_utf8_escape import decode


def test_decode_normal():
    """Normal case: escaped UTF‑8 bytes representing ASCII characters."""
    data = b"\\x48\\x65\\x6c\\x6c\\x6f"  # "Hello"
    result, consumed = decode(data)
    assert result == "Hello"
    assert consumed == len(data)


def test_decode_empty():
    """Boundary case: empty input should return empty string and zero bytes consumed."""
    data = b""
    result, consumed = decode(data)
    assert result == ""
    assert consumed == 0


def test_decode_invalid_utf8():
    """Error case: invalid UTF‑8 sequence should raise UnicodeDecodeError."""
    data = b"\\x80"  # 0x80 is not a valid start byte in UTF‑8
    with pytest.raises(UnicodeDecodeError) as excinfo:
        decode(data)
    # The exception should refer to the original data and the problematic range
    assert excinfo.value.args[1] == data
    assert excinfo.value.start == 0
    assert excinfo.value.end == 1
