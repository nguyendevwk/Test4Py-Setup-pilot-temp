import pytest
from flutils.codecs.raw_utf8_escape import encode


def test_encode_basic_ascii_and_escape():
    # Input contains normal ASCII and an escaped hex sequence \x41 (A)
    input_text = "Hello\\x41World"
    # Expected: bytes of escaped UTF‑8 hex for "HelloAWorld"
    expected_bytes = b"\\x48\\x65\\x6c\\x6c\\x6f\\x41\\x57\\x6f\\x72\\x6c\\x64"
    out_bytes, consumed = encode(input_text)
    assert out_bytes == expected_bytes
    assert consumed == len(input_text)


def test_encode_empty_string():
    # Empty input should return empty bytes and zero consumed characters
    out_bytes, consumed = encode("")
    assert out_bytes == b""
    assert consumed == 0


def test_encode_invalid_utf8_escape_raises():
    # \xFF is not valid UTF‑8 when interpreted as a byte sequence
    input_text = "\\xFF"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(input_text)
    # The exception should refer to the original input string
    assert str(input_text) in str(excinfo.value)
