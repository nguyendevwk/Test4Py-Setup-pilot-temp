import pytest
from flutils.codecs.raw_utf8_escape import encode


def test_encode_ascii_returns_bytes_and_length():
    """Normal case: plain ASCII string should be returned unchanged as escaped bytes."""
    text = "Hello, World!"
    out_bytes, consumed = encode(text)
    # The output should be the same as the input encoded in UTF‑8
    assert out_bytes == text.encode("utf-8")
    # The number of consumed characters must equal the input length
    assert consumed == len(text)


def test_encode_escaped_hex_sequences():
    """Boundary case: string containing escaped hex sequences should be interpreted."""
    # The string contains the literal characters \xC3\xA9 which represent the UTF‑8
    # encoding of the character 'é'.
    text = r"\xC3\xA9"
    out_bytes, consumed = encode(text)
    # The output should be the escaped hex representation of the UTF‑8 bytes for 'é'
    assert out_bytes == b"\\xC3\\xA9"
    # The number of consumed characters must equal the input length
    assert consumed == len(text)


def test_encode_invalid_utf8_raises_unicode_encode_error():
    """Error case: invalid UTF‑8 byte sequence should raise UnicodeEncodeError."""
    # \xFF is not a valid start byte in UTF‑8
    text = r"\xFF"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(text)
    # The exception should mention the original text and the error reason
    assert "invalid start byte" in str(excinfo.value)
    assert "eutf8h" in str(excinfo.value)
