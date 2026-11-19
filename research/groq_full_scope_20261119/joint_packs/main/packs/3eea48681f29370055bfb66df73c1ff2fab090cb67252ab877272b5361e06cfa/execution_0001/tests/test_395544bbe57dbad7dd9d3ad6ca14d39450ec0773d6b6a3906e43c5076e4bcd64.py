import pytest
from isort.exceptions import FormattingPluginDoesNotExist


def test_exception_message_and_attribute():
    """The exception should store the formatter name and produce the correct message."""
    formatter_name = "nonexistent_formatter"
    exc = FormattingPluginDoesNotExist(formatter_name)

    # The formatter attribute should be set correctly
    assert exc.formatter == formatter_name

    # The message should contain the formatter name and be a string
    assert isinstance(str(exc), str)
    assert formatter_name in str(exc)
    assert "does not exist" in str(exc)


def test_exception_inherits_from_ISortError():
    """FormattingPluginDoesNotExist should be a subclass of ISortError."""
    from isort.exceptions import ISortError

    exc = FormattingPluginDoesNotExist("foo")
    assert isinstance(exc, ISortError)


def test_exception_raises_with_invalid_input():
    """Passing a non-string formatter should still create the exception but store the repr of the value."""
    non_string = 42
    exc = FormattingPluginDoesNotExist(non_string)

    # The formatter attribute should be the original value
    assert exc.formatter == non_string

    # The message should include the string representation of the non-string value
    assert "42" in str(exc)
