import pytest
from pypara.monetary import MonetaryOperationException

def test_mon_exception_inherits_type_error_and_has_message():
    """MonetaryOperationException should inherit from TypeError and store the message."""
    msg = "Operation not supported for this currency."
    exc = MonetaryOperationException(msg)
    # Check inheritance
    assert isinstance(exc, TypeError)
    # Check message stored correctly
    assert str(exc) == msg
    # Ensure args contain the message
    assert exc.args == (msg,)

def test_raising_and_catching_mon_exception():
    """Raising MonetaryOperationException should propagate as a TypeError."""
    def raise_exc():
        raise MonetaryOperationException("Invalid operation")

    with pytest.raises(TypeError) as excinfo:
        raise_exc()
    # The caught exception should be the same instance type
    assert isinstance(excinfo.value, MonetaryOperationException)
    assert str(excinfo.value) == "Invalid operation"

def test_mon_exception_can_be_used_in_exception_chaining():
    """MonetaryOperationException should support exception chaining."""
    original = ValueError("original error")
    try:
        raise original
    except ValueError as e:
        raise MonetaryOperationException("Chained error") from e

    with pytest.raises(MonetaryOperationException) as excinfo:
        raise MonetaryOperationException("Chained error") from original

    # The __cause__ attribute should reference the original exception
    assert excinfo.value.__cause__ is original
    assert str(excinfo.value) == "Chained error"
