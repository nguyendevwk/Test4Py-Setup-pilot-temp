import pytest
from flutils.codecs.raw_utf8_escape import encode


def test_encode_ascii_returns_escaped_bytes_and_length():
    # Input: simple ASCII string
    text = "Hello, World!"
    out_bytes, consumed = encode(text)
    # The output should be the same string encoded as UTF-8 bytes
    assert out_bytes == b"Hello, World!"
    # The number of consumed characters should equal the length of the input
    assert consumed == len(text)


def test_encode_escaped_hex_sequences():
    # Input contains literal escaped hex sequences that represent UTF‑8 bytes
    # The string "é" in UTF‑8 is b'\xc3\xa9', which can be written as "\\xC3\\xA9"
    text = "A\\xC3\\xA9B"
    out_bytes, consumed = encode(text)
    # The output should be the bytes for "AéB" with each byte escaped
    # "A" -> 0x41, "é" -> 0xC3 0xA9, "B" -> 0x42
    expected_bytes = b"\\x41\\xC3\\xA9\\x42"
    assert out_bytes == expected_bytes
    assert consumed == len(text)


def test_encode_invalid_utf8_raises_unicode_encode_error():
    # Input contains an invalid UTF‑8 byte sequence: 0xFF is not a valid start byte
    text = "\\xFF"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(text)
    # The exception should mention the original text and the error reason
    assert "eutf8h" in str(excinfo.value)
    assert "invalid start byte" in str(excinfo.value)
