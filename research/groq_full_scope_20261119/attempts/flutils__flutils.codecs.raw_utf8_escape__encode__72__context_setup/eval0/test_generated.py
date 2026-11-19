import pytest
from flutils.codecs.raw_utf8_escape import encode


def test_encode_ascii_returns_bytes_and_length():
    """Encoding a plain ASCII string should return the same bytes and length."""
    text = "Hello, World!"
    out_bytes, consumed = encode(text)
    assert isinstance(out_bytes, bytes)
    assert out_bytes == b"Hello, World!"
    assert consumed == len(text)


def test_encode_non_ascii_and_escaped_sequences():
    """Non‑ASCII characters and escaped hex sequences are correctly encoded."""
    # 'é' is U+00E9, UTF‑8 bytes: C3 A9
    # '\\x41' should become the byte 0x41 (ASCII 'A')
    text = "Café\\x41"
    out_bytes, consumed = encode(text)
    # Expected bytes: C3 A9 41
    assert out_bytes == b"\\xc3\\xa9A"
    assert consumed == len(text)


def test_encode_invalid_utf8_raises_unicode_encode_error():
    """An invalid UTF‑8 escape sequence should raise UnicodeEncodeError."""
    # '\\x80' is an invalid start byte for UTF‑8
    text = "\\x80"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(text)
    # The exception should reference the original text and the problematic range
    assert excinfo.value.args[1] == text
    assert excinfo.value.args[2] == 0
    assert excinfo.value.args[3] == 1
