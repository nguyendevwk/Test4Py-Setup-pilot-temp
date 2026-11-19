import codecs
import base64
import pytest

from flutils.codecs.b64 import register, NAME


def test_register_adds_codec_and_decodes_correctly():
    # Ensure codec is not registered before calling register
    with pytest.raises(LookupError):
        codecs.getdecoder(NAME)

    # Register the codec
    register()

    # After registration, the decoder should be available
    decoder = codecs.getdecoder(NAME)
    assert decoder is not None

    # Test that the decoder correctly decodes a base64 string
    original = b"Hello, world!"
    encoded = base64.b64encode(original).decode()
    decoded, _ = decoder(encoded)
    assert decoded == original


def test_register_is_idempotent_and_does_not_raise():
    # Register the codec once
    register()
    # Registering again should not raise any exception
    register()
    # The codec should still be available
    decoder = codecs.getdecoder(NAME)
    assert decoder is not None


def test_decoder_handles_invalid_base64_raises_error():
    # Register the codec
    register()
    decoder = codecs.getdecoder(NAME)

    # Provide an invalid base64 string; the decoder should raise a binascii.Error
    invalid_encoded = "!!!invalid!!!"
    with pytest.raises(Exception) as excinfo:
        decoder(invalid_encoded)
    # The underlying exception should be a binascii.Error
    assert excinfo.type.__name__ == "Error"
