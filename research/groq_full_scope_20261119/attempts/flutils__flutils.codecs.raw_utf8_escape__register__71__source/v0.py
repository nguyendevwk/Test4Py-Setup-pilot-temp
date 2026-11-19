import codecs
import importlib
import sys
import types
import pytest

# Import the target module
mod = importlib.import_module("flutils.codecs.raw_utf8_escape")

# The codec name is expected to be defined in the module
NAME = getattr(mod, "NAME", None)
assert isinstance(NAME, str), "Module must expose a string NAME"

def test_register_and_basic_encode_decode(tmp_path):
    """
    Verify that after calling register(), the codec is available and
    encoding/decoding works for a simple Unicode string.
    """
    # Ensure the codec is not already registered
    with pytest.raises(LookupError):
        codecs.getdecoder(NAME)

    # Register the codec
    mod.register()

    # Now the codec should be available
    decoder = codecs.getdecoder(NAME)
    encoder = codecs.getencoder(NAME)

    # Test a simple string
    original = "Hello, 世界"
    encoded, _ = encoder(original)
    decoded, _ = decoder(encoded)

    assert isinstance(encoded, bytes)
    assert decoded == original

def test_boundary_empty_and_long_string(tmp_path):
    """
    Test encoding/decoding of an empty string and a long string to
    ensure boundary conditions are handled correctly.
    """
    mod.register()
    encoder = codecs.getencoder(NAME)
    decoder = codecs.getdecoder(NAME)

    # Empty string
    empty = ""
    enc_empty, _ = encoder(empty)
    dec_empty, _ = decoder(enc_empty)
    assert enc_empty == b""
    assert dec_empty == empty

    # Long string (repeated pattern)
    long_str = "a" * 10000 + "中" * 5000
    enc_long, _ = encoder(long_str)
    dec_long, _ = decoder(enc_long)
    assert isinstance(enc_long, bytes)
    assert dec_long == long_str

def test_error_on_invalid_input():
    """
    Ensure that passing a non-string to the encoder raises a TypeError,
    and that decoding invalid bytes raises a UnicodeDecodeError.
    """
    mod.register()
    encoder = codecs.getencoder(NAME)
    decoder = codecs.getdecoder(NAME)

    # Encoder should reject non-string input
    with pytest.raises(TypeError):
        encoder(123)

    # Decoder should raise UnicodeDecodeError on invalid byte sequence
    # Construct an invalid byte sequence for UTF-8 (e.g., a lone continuation byte)
    invalid_bytes = b"\x80\x80\x80"
    with pytest.raises(UnicodeDecodeError):
        decoder(invalid_bytes)
