import base64
import codecs
import pytest
from flutils.codecs.b64 import register, encode, decode, NAME


def test_register_and_codec_roundtrip(tmp_path):
    # Register the codec and verify it can be retrieved
    register()
    codec_info = codecs.lookup(NAME)
    assert codec_info.name == NAME
    assert codec_info.encode is encode
    assert codec_info.decode is decode

    # Prepare some binary data and encode it
    original = b"Hello, world!"
    encoded_str, consumed = codec_info.encode(original)
    assert isinstance(encoded_str, bytes)
    assert consumed == len(original)

    # Decode the string back to bytes
    decoded_bytes, decoded_len = codec_info.decode(encoded_str)
    assert decoded_bytes == original
    assert decoded_len == len(encoded_str)


def test_encode_and_decode_with_whitespace_and_lines(tmp_path):
    # Create a base64 string with newlines and indentation
    raw_bytes = b"Python testing 123"
    b64_bytes = base64.b64encode(raw_bytes)
    b64_str = b64_bytes.decode("utf-8")
    # Insert line breaks and spaces
    formatted = f"  {b64_str[:10]}\n{b64_str[10:20]}\n   {b64_str[20:]}\n"
    # Encode using the custom codec
    decoded, _ = encode(formatted)
    assert decoded == raw_bytes

    # Now decode the original bytes back to string
    encoded_str, _ = decode(raw_bytes)
    # The encoded string should match the original base64 string
    assert encoded_str == b64_str


def test_encode_error_on_invalid_base64():
    # Provide an invalid base64 string
    invalid = "!!! not base64 !!!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(invalid)
    # The exception message should mention the problematic string
    assert "not a proper bas64 character string" in str(excinfo.value)
    # The original text should be present in the exception context
    assert "!!! not base64 !!!" in str(excinfo.value)
