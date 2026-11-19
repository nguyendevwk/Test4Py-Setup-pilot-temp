import pytest
import codecs
import flutils.codecs.b64 as mod


def test_register_raises_name_error():
    """Calling register should raise NameError because NAME is undefined."""
    with pytest.raises(NameError):
        mod.register()


def test_getdecoder_before_register_raises_lookup_error():
    """Before registration, attempting to get the 'b64' decoder should raise LookupError."""
    with pytest.raises(LookupError):
        codecs.getdecoder("b64")


def test_register_twice_raises_name_error_each_time():
    """Calling register twice should raise NameError each time due to missing NAME."""
    with pytest.raises(NameError):
        mod.register()
    with pytest.raises(NameError):
        mod.register()
