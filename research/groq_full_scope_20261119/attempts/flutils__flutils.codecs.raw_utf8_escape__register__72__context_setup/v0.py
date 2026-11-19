import codecs
import pytest
from flutils.codecs.raw_utf8_escape import register, encode, decode, NAME

# Ensure the codec is registered before tests
register()


def test_encode_decode_roundtrip():
    """Normal case: encode a string with escaped bytes and decode back."""
    original = "Hello\\x20World\\x21"  # contains escaped space and exclamation
    encoded_bytes, enc_len = encode(original)
    assert isinstance(encoded_bytes, bytes)
    assert enc_len == len(original)

    decoded_str, dec_len = decode(encoded_bytes)
    assert isinstance(decoded_str, str)
    assert dec_len == len(encoded_bytes)
    # The decoded string should match the original after interpreting escapes
    assert decoded_str == "Hello World!"


def test_empty_input():
    """Boundary case: empty string/bytes should roundtrip to empty."""
    encoded_bytes, enc_len = encode("")
    assert encoded_bytes == b""
    assert enc_len == 0

    decoded_str, dec_len = decode(b"")
    assert decoded_str == ""
    assert dec_len == 0


def test_invalid_utf8_escape_raises():
    """Error case: invalid UTF‑8 escape sequence should raise UnicodeEncodeError."""
    # \xFF is not valid UTF‑8 start byte
    bad_input = "bad\\xFF"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(bad_input)
    # The exception should reference the codec name
    assert excinfo.value.args[0] == 'eutf8h'
    # The error message should mention the problematic byte
    assert "bad" in excinfo.value.args[1]
