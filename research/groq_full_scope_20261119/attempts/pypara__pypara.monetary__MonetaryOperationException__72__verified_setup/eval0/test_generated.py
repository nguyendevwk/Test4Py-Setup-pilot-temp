import pytest
from pypara.monetary import MonetaryOperationException

def test_monetary_operation_exception_is_subclass_of_type_error():
    """MonetaryOperationException should inherit from TypeError."""
    assert issubclass(MonetaryOperationException, TypeError)

def test_monetary_operation_exception_can_be_instantiated_with_message():
    """Instantiating with a message should store it correctly."""
    msg = "Invalid monetary operation"
    exc = MonetaryOperationException(msg)
    assert isinstance(exc, MonetaryOperationException)
    assert str(exc) == msg

def test_monetary_operation_exception_default_message_is_empty_string():
    """When no message is provided, the exception's string representation should be empty."""
    exc = MonetaryOperationException()
    assert isinstance(exc, MonetaryOperationException)
    assert str(exc) == ""
