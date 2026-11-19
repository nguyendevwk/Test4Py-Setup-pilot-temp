import codecs
import base64
import pytest
from flutils.codecs.b64 import register, encode, decode, NAME


def test_register_and_codec_roundtrip(tmp_path):
    # Register the codec and verify it can be retrieved
    register()
    codec_info = codecs.getdecoder(NAME)
    assert codec_info is not None

    # Prepare a sample byte sequence
    original_bytes = b"Hello, world!"
    # Encode using our codec
    encoded_str, consumed = encode(original_bytes.decode('utf-8'), errors='ignore')
    assert consumed == len(original_bytes)
    # The encoded string should be valid base64
    assert isinstance(encoded_str, bytes)
    # Decode back using the codec
    decoded_bytes, decoded_len = decode(encoded_str, errors='ignore')
    assert decoded_len == len(encoded_str)
    assert decoded_bytes == original_bytes


def test_encode_with_whitespace_and_multiline(tmp_path):
    # Register the codec
    register()
    # Input with newlines and indentation
    multiline_input = """
        SGVsbG8s
        IHdvcmxkIQ==
    """
    # Encode should strip whitespace and decode correctly
    decoded_bytes, length = encode(multiline_input, errors='ignore')
    assert length == len(multiline_input)
    assert decoded_bytes == b"Hello, world!"


def test_encode_invalid_base64_raises_unicodeencodeerror(tmp_path):
    register()
    # Invalid base64 string
    bad_input = "!!! not base64 !!!"
    with pytest.raises(UnicodeEncodeError) as excinfo:
        encode(bad_input, errors='ignore')
    # The exception message should mention the problematic string
    assert "not a proper bas64 character string" in str(excinfo.value)
    assert bad_input in str(excinfo.value)
