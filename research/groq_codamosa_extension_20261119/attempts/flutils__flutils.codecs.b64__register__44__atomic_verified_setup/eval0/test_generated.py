import codecs
import base64
import importlib
import sys

# Import the target module
from flutils.codecs.b64 import register, NAME


def test_register_adds_codec():
    """Calling register should add a decoder for the codec name."""
    # Ensure the codec is not already registered
    with pytest.raises(LookupError):
        codecs.getdecoder(NAME)

    # Register the codec
    register()

    # After registration, the decoder should be available
    decoder, _ = codecs.getdecoder(NAME)
    assert decoder is not None
    # The decoder should correctly decode a simple base64 string
    encoded = base64.b64encode(b"hello").decode()
    decoded, _ = decoder(encoded)
    assert decoded == b"hello"


def test_register_idempotent():
    """Registering the codec multiple times should not raise an exception."""
    # First registration
    register()
    # Second registration should be harmless
    register()
    # The codec should still be available
    decoder, _ = codecs.getdecoder(NAME)
    assert decoder is not None
    # Decode a known value
    decoded, _ = decoder(base64.b64encode(b"world").decode())
    assert decoded == b"world"


def test_codec_handles_invalid_input():
    """The codec decoder should raise a binascii.Error for invalid base64 input."""
    register()
    decoder, _ = codecs.getdecoder(NAME)
    # Provide an invalid base64 string
    invalid_input = "!!!invalid!!!"
    with pytest.raises(base64.binascii.Error):
        decoder(invalid_input)
