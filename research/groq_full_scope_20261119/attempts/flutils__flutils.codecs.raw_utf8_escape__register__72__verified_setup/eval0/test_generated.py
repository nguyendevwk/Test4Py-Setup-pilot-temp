import codecs
import importlib
import sys
import types

# Import the target module
mod = importlib.import_module("flutils.codecs.raw_utf8_escape")

# The codec name is defined in the module; we retrieve it for use in tests
CODEC_NAME = getattr(mod, "NAME", None)
assert CODEC_NAME is not None, "Module must define a NAME attribute for the codec"

def test_register_adds_codec():
    """
    Verify that calling register() adds the codec to the codecs registry
    and that the decoder can be retrieved and used.
    """
    # Ensure the codec is not already registered
    with pytest.raises(LookupError):
        codecs.getdecoder(CODEC_NAME)

    # Register the codec
    mod.register()

    # After registration, the decoder should be available
    decoder = codecs.getdecoder(CODEC_NAME)
    assert callable(decoder), "Decoder should be a callable"

    # Test that the decoder works on a simple UTF-8 byte string
    sample_bytes = b"Hello, \xe4\xbd\xa0\xe5\xa5\xbd"  # "Hello, 你好"
    decoded, _ = decoder(sample_bytes)
    assert decoded == "Hello, 你好", "Decoder should correctly decode UTF-8 bytes"

def test_register_is_idempotent():
    """
    Verify that calling register() multiple times does not raise an exception
    and that the codec remains registered.
    """
    # First registration
    mod.register()
    # Second registration should not raise
    mod.register()

    # The decoder should still be available
    decoder = codecs.getdecoder(CODEC_NAME)
    assert callable(decoder), "Decoder should still be callable after repeated registration"

def test_register_without_name_raises():
    """
    Verify that if the module does not define a NAME attribute,
    register() will raise an AttributeError when attempting to access it.
    """
    # Create a temporary module that lacks NAME
    temp_mod = types.ModuleType("temp_mod")
    temp_mod.register = mod.register
    # Temporarily replace the module in sys.modules
    original = sys.modules.get("flutils.codecs.raw_utf8_escape")
    sys.modules["flutils.codecs.raw_utf8_escape"] = temp_mod
    try:
        with pytest.raises(AttributeError):
            temp_mod.register()
    finally:
        # Restore original module
        if original is not None:
            sys.modules["flutils.codecs.raw_utf8_escape"] = original
        else:
            del sys.modules["flutils.codecs.raw_utf8_escape"]
