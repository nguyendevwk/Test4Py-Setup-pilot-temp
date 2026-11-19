import pytest
from pypara.monetary import MonetaryOperationException

def test_monetary_operation_exception_inherits_type_error():
    """MonetaryOperationException should be a subclass of TypeError."""
    exc = MonetaryOperationException("Test message")
    assert isinstance(exc, TypeError), "MonetaryOperationException must inherit from TypeError"
    assert isinstance(exc, MonetaryOperationException), "Instance must be of its own type"

def test_monetary_operation_exception_message():
    """The exception should store and expose the message passed to it."""
    message = "Cannot perform operation due to insufficient funds."
    exc = MonetaryOperationException(message)
    assert str(exc) == message, "Exception message should match the provided string"

def test_monetary_operation_exception_can_be_raised_and_caught():
    """Raising and catching the exception should work as expected."""
    with pytest.raises(MonetaryOperationException) as excinfo:
        raise MonetaryOperationException("Operation failed")
    assert "Operation failed" in str(excinfo.value), "Caught exception should contain the original message"
