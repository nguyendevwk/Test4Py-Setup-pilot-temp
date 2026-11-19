import pytest
from pypara.monetary import MonetaryOperationException

def test_monetary_operation_exception_is_subclass_of_type_error():
    """MonetaryOperationException should inherit from TypeError."""
    exc = MonetaryOperationException("test message")
    assert isinstance(exc, TypeError)
    assert isinstance(exc, MonetaryOperationException)

def test_monetary_operation_exception_message_preserved():
    """The exception should preserve the message passed to its constructor."""
    message = "cannot perform operation"
    exc = MonetaryOperationException(message)
    assert str(exc) == message

def test_monetary_operation_exception_can_be_raised_and_caught():
    """Raising and catching the exception should work as expected."""
    with pytest.raises(MonetaryOperationException) as excinfo:
        raise MonetaryOperationException("error occurred")
    assert str(excinfo.value) == "error occurred"
