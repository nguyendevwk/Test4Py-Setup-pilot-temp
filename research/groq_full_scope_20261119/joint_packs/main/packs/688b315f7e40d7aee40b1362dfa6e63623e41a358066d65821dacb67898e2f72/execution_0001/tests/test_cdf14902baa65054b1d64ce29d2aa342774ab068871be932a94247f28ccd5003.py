import pytest
from httpie.models import OutputOptions
from requests import Request, Response

# Test that the `any` method correctly reflects the state of the options.
def test_any_method_true_and_false():
    # When at least one option is True, any() should return True.
    opt_true = OutputOptions(kind=None, headers=True, body=False, meta=False)
    assert opt_true.any() is True

    # When all options are False, any() should return False.
    opt_false = OutputOptions(kind=None, headers=False, body=False, meta=False)
    assert opt_false.any() is False

# Test that constructing OutputOptions with explicit arguments works as expected.
def test_outputoptions_construction_and_attributes():
    opt = OutputOptions(kind="request", headers=True, body=True, meta=True)
    assert opt.kind == "request"
    assert opt.headers is True
    assert opt.body is True
    assert opt.meta is True

# Test that calling from_message with an unsupported message type raises an exception.
def test_from_message_with_invalid_message_type():
    # Create a dummy object that is not a requests.Request or requests.Response.
    class DummyMessage:
        pass

    dummy = DummyMessage()
    # from_message should raise a TypeError (or a ValueError) because it cannot infer kind.
    with pytest.raises(Exception):
        OutputOptions.from_message(dummy)
