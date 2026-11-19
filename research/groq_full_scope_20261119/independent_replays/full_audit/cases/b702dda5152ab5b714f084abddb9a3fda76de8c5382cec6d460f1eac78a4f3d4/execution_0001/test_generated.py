import pytest
from isort.exceptions import FormattingPluginDoesNotExist

def test_instantiation_message_and_attribute():
    """Normal case: message contains the formatter and attribute is set."""
    formatter_name = "black"
    exc = FormattingPluginDoesNotExist(formatter_name)
    # The exception should be an instance of Exception
    assert isinstance(exc, Exception)
    # The formatter attribute should match the input
    assert exc.formatter == formatter_name
    # The message should include the formatter name
    assert formatter_name in str(exc)
    # The message should start with the expected prefix
    assert str(exc).startswith(f"Specified formatting plugin of {formatter_name} does not exist")

def test_empty_formatter():
    """Boundary case: empty string as formatter."""
    exc = FormattingPluginDoesNotExist("")
    # The formatter attribute should be the empty string
    assert exc.formatter == ""
    # The message should still be well-formed
    assert str(exc) == "Specified formatting plugin of  does not exist. "

def test_non_string_formatter():
    """Error-like case: passing a non-string (e.g., integer) should still work but convert to string."""
    formatter_value = 42
    exc = FormattingPluginDoesNotExist(formatter_value)
    # The formatter attribute should be the integer value
    assert exc.formatter == formatter_value
    # The message should contain the string representation of the integer
    assert "42" in str(exc)
    # The message should not raise an exception during formatting
    assert isinstance(str(exc), str)
