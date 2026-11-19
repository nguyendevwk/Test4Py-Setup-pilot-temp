import codecs
import base64
import pytest
from flutils.codecs.b64 import register, NAME

def test_register_adds_decoder():
    # Ensure the codec is not registered before calling register
    with pytest.raises(LookupError):
        codecs.getdecoder(NAME)
    # Register the codec
    register()
    # After registration, the decoder should be available
    decoder, _ = codecs.getdecoder(NAME)
    assert decoder is not None
    # Decode a known base64 string
    encoded = base64.b64encode(b"hello world").decode()
    decoded, _ = decoder(encoded)
    assert decoded == b"hello world"

def test_register_is_idempotent():
    # Register the codec twice; should not raise an exception
    register()
    register()
    # Verify that the decoder still works
    decoder, _ = codecs.getdecoder(NAME)
    decoded, _ = decoder(base64.b64encode(b"test").decode())
    assert decoded == b"test"

def test_decoder_handles_invalid_input():
    # Register the codec
    register()
    decoder, _ = codecs.getdecoder(NAME)
    # Provide an invalid base64 string; should raise a binascii.Error
    with pytest.raises(Exception) as excinfo:
        decoder("!!!invalid base64!!!")
    # The exception should be a binascii.Error or its subclass
    from binascii import Error as BinasciiError
    assert isinstance(excinfo.value, BinasciiError)
