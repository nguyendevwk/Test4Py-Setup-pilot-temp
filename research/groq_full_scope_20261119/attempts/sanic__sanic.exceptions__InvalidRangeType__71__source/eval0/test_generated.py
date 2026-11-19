import pytest
from sanic.exceptions import InvalidRangeType

def test_invalid_range_type_basic_attributes():
    """Verify that the exception has the correct status code and default quiet flag."""
    exc = InvalidRangeType()
    # Status code should be 416 as defined in the class
    assert exc.status_code == 416
    # The quiet flag defaults to True as per the class definition
    assert exc.quiet is True
    # The exception should be an instance of Exception
    assert isinstance(exc, Exception)

def test_invalid_range_type_with_message_and_headers():
    """Check that custom message and headers are stored correctly."""
    message = "Invalid range requested"
    headers = {"Retry-After": "120"}
    exc = InvalidRangeType(message=message, headers=headers)
    # The message should be accessible via the args tuple
    assert exc.args[0] == message
    # Headers should be stored on the exception instance
    assert getattr(exc, "headers", None) == headers

def test_invalid_range_type_inherits_from_range_not_satisfiable():
    """Ensure that the exception is a subclass of RangeNotSatisfiable."""
    exc = InvalidRangeType()
    # Import the parent class for comparison
    from sanic.exceptions import RangeNotSatisfiable
    assert isinstance(exc, RangeNotSatisfiable)
    # The parent class should also have the same status code
    assert exc.status_code == RangeNotSatisfiable.status_code
