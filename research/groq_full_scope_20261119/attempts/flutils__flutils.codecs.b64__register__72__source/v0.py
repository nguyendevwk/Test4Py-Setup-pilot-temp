import base64
import codecs
import pytest

# Import the target module
import flutils.codecs.b64 as b64_module


def test_register_and_decode():
    """
    Test that the register function registers the 'b64' codec and that
    the decoder correctly decodes a base64 string.
    """
    # Ensure the codec is not registered yet
    with pytest.raises(LookupError):
        codecs.getdecoder("b64")

    # Register the codec
    b64_module.register()

    # After registration, the decoder should be available
    decoder = codecs.getdecoder("b64")
    assert decoder is not None

    # Decode a known base64 string
    original = b"hello world"
    encoded = base64.b64encode(original).decode("ascii")
    decoded_bytes, _ = decoder(encoded)
    assert decoded_bytes == original


def test_register_idempotent():
    """
    Test that calling register multiple times does not raise an exception
    and the codec remains available.
    """
    # First registration
    b64_module.register()
    # Second registration should be harmless
    b64_module.register()

    # The decoder should still work
    decoder = codecs.getdecoder("b64")
    decoded_bytes, _ = decoder(base64.b64encode(b"test").decode("ascii"))
    assert decoded_bytes == b"test"


def test_register_error_on_missing_name():
    """
    Test that if the module's NAME attribute is missing, register raises a NameError.
    """
    # Temporarily delete NAME from the module if it exists
    original_name = getattr(b64_module, "NAME", None)
    if hasattr(b64_module, "NAME"):
        delattr(b64_module, "NAME")

    try:
        with pytest.raises(NameError):
            b64_module.register()
    finally:
        # Restore NAME for other tests
        if original_name is not None:
            setattr(b64_module, "NAME", original_name)
