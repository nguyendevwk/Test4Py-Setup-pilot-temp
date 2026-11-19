import codecs
import importlib
import sys

import pytest

# Import the target module
mod = importlib.import_module("flutils.codecs.raw_utf8_escape")

# The codec name is expected to be defined in the module
CODEC_NAME = getattr(mod, "NAME", None)
assert CODEC_NAME is not None, "Module must expose a NAME attribute"


def test_register_adds_decoder_and_encoder():
    """Calling register should add a decoder and encoder for the codec name."""
    # Ensure the codec is not already registered
    with pytest.raises(LookupError):
        codecs.getdecoder(CODEC_NAME)

    # Register the codec
    mod.register()

    # After registration, decoder and encoder should be available
    decoder = codecs.getdecoder(CODEC_NAME)
    encoder = codecs.getencoder(CODEC_NAME)

    # Test that decoding a simple byte string returns the expected Unicode string
    sample_bytes = b"hello\\nworld"
    decoded, _ = decoder(sample_bytes)
    assert decoded == "hello\\nworld"

    # Test that encoding the same string returns the original bytes
    encoded, _ = encoder(decoded)
    assert encoded == sample_bytes


def test_register_is_idempotent():
    """Registering the codec multiple times should not raise an exception."""
    # First registration
    mod.register()
    # Second registration should be harmless
    mod.register()
    # Third registration should also be harmless
    mod.register()

    # Verify that the codec is still available
    decoder = codecs.getdecoder(CODEC_NAME)
    assert callable(decoder)


def test_codec_roundtrip_with_userstring():
    """The codec should correctly round‑trip a UserString instance."""
    from collections import UserString

    # Register the codec
    mod.register()

    # Create a UserString containing escape sequences
    original = UserString("foo\\tbar\\nbaz")

    # Encode the UserString to bytes
    encoder = codecs.getencoder(CODEC_NAME)
    encoded_bytes, _ = encoder(original)
    assert isinstance(encoded_bytes, bytes)

    # Decode the bytes back to a string
    decoder = codecs.getdecoder(CODEC_NAME)
    decoded_str, _ = decoder(encoded_bytes)
    assert decoded_str == original

    # The decoded string should be a plain str, not a UserString
    assert not isinstance(decoded_str, UserString)
