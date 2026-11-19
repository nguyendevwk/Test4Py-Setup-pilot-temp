import codecs
import base64
import importlib
import sys

# Import the target module
import flutils.codecs.b64 as b64_module


def test_register_and_decode(tmp_path):
    """Verify that registering the codec allows decoding of a base64 string."""
    # Ensure the codec is not registered initially
    with pytest.raises(LookupError):
        codecs.getdecoder("b64")

    # Register the codec
    b64_module.register()

    # Now the decoder should be available
    decoder = codecs.getdecoder("b64")
    assert decoder is not None

    # Decode a known base64 string
    original = b"Hello, world!"
    encoded = base64.b64encode(original).decode()
    decoded, _ = decoder(encoded)
    assert decoded == original


def test_register_idempotent(tmp_path):
    """Calling register multiple times should not raise an exception."""
    # First registration
    b64_module.register()
    # Second registration should be harmless
    b64_module.register()
    # The codec should still be available
    decoder = codecs.getdecoder("b64")
    assert decoder is not None


def test_invalid_input_raises_error(tmp_path):
    """Decoding an invalid base64 string should raise a binascii.Error."""
    b64_module.register()
    decoder = codecs.getdecoder("b64")
    # Provide an invalid base64 string
    invalid = "!!! not base64 !!!"
    with pytest.raises(base64.binascii.Error):
        decoder(invalid)
