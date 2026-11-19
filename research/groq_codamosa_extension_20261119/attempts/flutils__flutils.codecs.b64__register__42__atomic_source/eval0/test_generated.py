import codecs
import base64
import importlib
import sys
import types
import pytest

# Import the module under test
from flutils.codecs.b64 import register, NAME

def test_register_adds_decoder_and_encoder():
    """After calling register, the codec name is available and works."""
    # Ensure the codec is not registered yet
    with pytest.raises(LookupError):
        codecs.getdecoder(NAME)
    # Register the codec
    register()
    # Now the decoder and encoder should be available
    decoder = codecs.getdecoder(NAME)
    encoder = codecs.getencoder(NAME)
    assert decoder is not None
    assert encoder is not None
    # Test that encoding and decoding round‑trip correctly
    original = b"hello world"
    encoded, _ = encoder(original)
    decoded, _ = decoder(encoded)
    assert decoded == original

def test_register_is_idempotent():
    """Calling register multiple times should not raise an exception."""
    register()
    # Register again; should not raise
    register()
    # Verify still works
    decoder = codecs.getdecoder(NAME)
    encoded, _ = decoder(b"test")
    assert encoded == base64.b64decode(b"test")

def test_register_does_not_override_existing_codec():
    """If a codec with the same name already exists, register should not replace it."""
    # Create a dummy codec with the same name
    def dummy_getreginfo():
        return {
            'name': NAME,
            'encode': lambda obj, errors='strict': (b'dummy', 0),
            'decode': lambda obj, errors='strict': (b'dummy', 0),
        }
    # Register dummy codec
    codecs.register(lambda name: dummy_getreginfo() if name == NAME else None)
    # Capture the original encode/decode
    original_encoder = codecs.getencoder(NAME)
    original_decoder = codecs.getdecoder(NAME)
    # Now register the real codec
    register()
    # The original dummy codec should still be in effect
    enc, _ = original_encoder(b"anything")
    dec, _ = original_decoder(b"anything")
    assert enc == b'dummy'
    assert dec == b'dummy'
