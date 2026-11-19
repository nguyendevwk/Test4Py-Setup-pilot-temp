import pytest
from isort.exceptions import FormattingPluginDoesNotExist

def test_initialization_and_message():
    """Normal case: verify that the exception stores the formatter and formats the message."""
    exc = FormattingPluginDoesNotExist("black")
    # The formatter attribute should be set correctly
    assert exc.formatter == "black"
    # The message should include the formatter name
    assert "black" in str(exc)
    # The message should start with the expected prefix
    assert str(exc).startswith("Specified formatting plugin of black does not exist.")

def test_empty_formatter_boundary():
    """Boundary case: passing an empty string should still create a valid exception."""
    exc = FormattingPluginDoesNotExist("")
    # The formatter attribute should be an empty string
    assert exc.formatter == ""
    # The message should still be well-formed
    assert str(exc).startswith("Specified formatting plugin of  does not exist.")
    # The message should not be empty
    assert len(str(exc)) > 0

def test_exception_is_subclass_of_exception_and_isort_error():
    """Error behavior: the exception should be a subclass of Exception and ISortError."""
    exc = FormattingPluginDoesNotExist("nonexistent")
    # It should be an instance of Exception
    assert isinstance(exc, Exception)
    # It should also be an instance of ISortError (via inheritance)
    # Import ISortError dynamically to avoid circular import issues
    from isort.exceptions import ISortError
    assert isinstance(exc, ISortError)
