import codecs
import pytest
from flutils.codecs import raw_utf8_escape

# Test 1: Registering the codec makes it available in the codecs registry
def test_register_codec_available():
    # Ensure the codec is not registered before calling register
    with pytest.raises(LookupError):
        codecs.getdecoder(raw_utf8_escape.NAME)
    # Register the codec
    raw_utf8_escape.register()
    # After registration, the decoder should be retrievable
    decoder = codecs.getdecoder(raw_utf8_escape.NAME)
    assert callable(decoder), "Decoder should be a callable after registration"

# Test 2: Encoding and decoding a normal string round‑trips correctly
def test_encode_decode_roundtrip():
    raw_utf8_escape.register()
    text = "Hello, 世界! 👋"
    # Encode using the registered codec
    encoded_bytes, _ = codecs.encode(text, raw_utf8_escape.NAME)
    assert isinstance(encoded_bytes, bytes), "Encoded result should be bytes"
    # Decode back
    decoded_text, _ = codecs.decode(encoded_bytes, raw_utf8_escape.NAME)
    assert decoded_text == text, "Decoded text should match original"

# Test 3: Passing a non‑string to the encoder raises a TypeError
def test_encode_invalid_input_type():
    raw_utf8_escape.register()
    with pytest.raises(TypeError):
        codecs.encode(12345, raw_utf8_escape.NAME)
