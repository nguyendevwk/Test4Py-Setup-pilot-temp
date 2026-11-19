import pytest
import codecs
from flutils.codecs.b64 import register

def test_register_raises_name_error():
    """The register function should raise a NameError because NAME is undefined."""
    with pytest.raises(NameError):
        register()

def test_getdecoder_before_and_after_register():
    """codecs.getdecoder('b64') should raise LookupError before and after register."""
    with pytest.raises(LookupError):
        codecs.getdecoder('b64')
    # Even after attempting to register, the codec is not available
    try:
        register()
    except NameError:
        pass
    with pytest.raises(LookupError):
        codecs.getdecoder('b64')
