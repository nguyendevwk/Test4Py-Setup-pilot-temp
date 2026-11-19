import codecs
import base64
import pytest
from flutils.codecs.b64 import register, NAME

def test_register_adds_codec_and_decodes():
    # Ensure codec is not registered before calling register
    with pytest.raises(LookupError):
        codecs.getdecoder(NAME)
    # Register the codec
    register()
    # After registration, decoder should be available
    decoder = codecs.getdecoder(NAME)
    # Test decoding a known base64 string
    decoded_bytes, _ = decoder(b"SGVsbG8gd29ybGQh")  # "Hello world!"
    assert decoded_bytes == b"Hello world!"

def test_register_is_idempotent():
    # Register once
    register()
    # Register again should not raise
    register()
    # Decoder should still work
    decoder = codecs.getdecoder(NAME)
    decoded_bytes, _ = decoder(b"VGVzdA==")  # "Test"
    assert decoded_bytes == b"Test"

def test_codec_roundtrip_with_encoder_and_decoder():
    register()
    encoder = codecs.getencoder(NAME)
    decoder = codecs.getdecoder(NAME)
    original = b"Python 3.11"
    encoded_bytes, _ = encoder(original)
    # The encoded bytes should match base64 standard output
    assert encoded_bytes == base64.b64encode(original)
    decoded_bytes, _ = decoder(encoded_bytes)
    assert decoded_bytes == original
