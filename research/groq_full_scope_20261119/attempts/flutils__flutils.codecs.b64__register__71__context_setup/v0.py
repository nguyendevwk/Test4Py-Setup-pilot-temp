import base64
import codecs
import pytest
from flutils.codecs.b64 import register, encode, decode, NAME

def test_b64_encode_and_decode_roundtrip():
    # Register the codec and verify it is available
    register()
    codec_info = codecs.lookup(NAME)
    assert codec_info.name == NAME
    # Original data
    original = b"Hello, world! 123"
    # Encode using the codec
    encoded_str, consumed = codec_info.encode(original)
    assert isinstance(encoded_str, bytes)
    assert consumed == len(original)
    # Decode back
    decoded_bytes, consumed_dec = codec_info.decode(encoded_str)
    assert isinstance(decoded_bytes, bytes)
    assert consumed_dec == len(encoded_str)
    assert decoded_bytes == original

def test_b64_encode_with_whitespace_and_multiline_input():
    # Input with newlines and indentation
    text = "  SGVsbG8s\n  d29ybGQh\n  MTIz  \n"
    # Use the encode function directly
    out_bytes, consumed = encode(text)
    assert isinstance(out_bytes, bytes)
    assert consumed == len(text)
    # The output should match base64 decoding of the cleaned string
    cleaned = "SGVsbG8s d29ybGQh MTIz"
    expected = base64.b64decode(cleaned.encode())
    assert out_bytes == expected

def test_b64_encode_invalid_input_raises_unicodeencodeerror():
    # Invalid base64 string (contains non-base64 characters)
    bad_text = "!!!invalid!!!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(bad_text)
    # The exception message should mention the problematic string
    assert "not a proper bas64 character string" in str(excinfo.value)
    # The original text should be present in the exception
    assert bad_text in str(excinfo.value)
