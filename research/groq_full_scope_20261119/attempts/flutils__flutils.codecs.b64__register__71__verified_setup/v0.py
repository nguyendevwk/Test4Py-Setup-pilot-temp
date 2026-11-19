import codecs
import base64
import pytest

from flutils.codecs.b64 import register, NAME


def test_register_adds_codec():
    """Calling register should add a decoder for the 'b64' codec."""
    # Ensure the codec is not already registered
    with pytest.raises(LookupError):
        codecs.getdecoder(NAME)

    # Register the codec
    register()

    # After registration, the decoder should be available
    decoder = codecs.getdecoder(NAME)
    assert decoder is not None
    # The decoder should decode a simple base64 string correctly
    decoded, _ = decoder(base64.b64encode(b"hello").decode())
    assert decoded == b"hello"


def test_register_is_idempotent():
    """Registering the codec multiple times should not raise an exception."""
    # First registration
    register()
    # Second registration should not raise
    register()
    # The codec should still work
    decoded, _ = codecs.getdecoder(NAME)(base64.b64encode(b"world").decode())
    assert decoded == b"world"


def test_codec_roundtrip():
    """The registered codec should correctly encode and decode data."""
    register()
    # Encode using the codec's encoder
    encoder = codecs.getencoder(NAME)
    encoded, _ = encoder(b"pytest")
    # The encoded bytes should match base64 encoding
    assert encoded == base64.b64encode(b"pytest")
    # Decode back
    decoder = codecs.getdecoder(NAME)
    decoded, _ = decoder(encoded.decode())
    assert decoded == b"pytest"
