import codecs
import base64
import importlib
import sys

# Import the target module
from flutils.codecs.b64 import register, NAME

def test_register_adds_codec():
    """Calling register should add a decoder for the codec name."""
    # Ensure the codec is not registered initially
    with pytest.raises(LookupError):
        codecs.getdecoder(NAME)
    # Register the codec
    register()
    # Now the decoder should be available
    decoder, _ = codecs.getdecoder(NAME)
    assert decoder is not None
    # The decoder should be a function that accepts a bytes-like object
    assert callable(decoder)

def test_register_is_idempotent():
    """Calling register multiple times should not raise an exception."""
    # First registration
    register()
    # Second registration should not raise
    register()
    # The codec should still be available
    decoder, _ = codecs.getdecoder(NAME)
    assert decoder is not None

def test_b64_codec_decodes_correctly():
    """The registered codec should correctly decode base64 data."""
    register()
    decoder, _ = codecs.getdecoder(NAME)
    # Prepare a known base64 string
    original = b"Hello, world!"
    encoded = base64.b64encode(original)
    # Use the codec decoder
    decoded, _ = decoder(encoded)
    assert decoded == original
