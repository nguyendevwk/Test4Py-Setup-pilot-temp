import codecs
import pytest
from flutils.codecs.raw_utf8_escape import encode, decode, register, NAME

# Ensure the codec is registered before tests
register()


def test_roundtrip_basic_string():
    """Encode a normal string and decode it back, expecting identity."""
    original = "Hello, 世界! \x01\x02"
    # Encode the string to escaped UTF‑8 bytes
    encoded_bytes, encoded_len = encode(original)
    assert isinstance(encoded_bytes, bytes)
    assert encoded_len == len(original)

    # Decode the bytes back to a string
    decoded_str, decoded_len = decode(encoded_bytes)
    assert isinstance(decoded_str, str)
    assert decoded_len == len(encoded_bytes)
    assert decoded_str == original


def test_escape_sequences_and_boundary():
    """Test handling of explicit escaped hex sequences and boundary values."""
    # The string contains literal backslashes and hex escapes
    original = r"Line1\nLine2\x7F\x80\xFF"
    # Encode: the literal \xHH should become actual bytes
    encoded_bytes, _ = encode(original)
    # The resulting bytes should contain the escaped representation
    # of the original string when decoded with the codec
    decoded_str, _ = decode(encoded_bytes)
    assert decoded_str == original

    # Verify that the encoded bytes contain the expected escaped hex
    # For example, \x7F should appear as the two characters '\\x7F'
    assert b"\\x7F" in encoded_bytes
    assert b"\\x80" in encoded_bytes
    assert b"\\xFF" in encoded_bytes


def test_invalid_utf8_raises_encode_error():
    """Encoding a string that contains an invalid UTF‑8 sequence should raise."""
    # Construct a string that contains a lone surrogate (invalid in UTF‑8)
    invalid_str = "Invalid \uDC00"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(invalid_str)
    # The exception should be raised by our custom codec
    assert excinfo.value.args[0] == 'eutf8h'
    # The problematic part should be reported in the exception
    assert excinfo.value.args[1] == str(invalid_str)
