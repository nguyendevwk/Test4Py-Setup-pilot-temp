import pytest
from isort.exceptions import FormattingPluginDoesNotExist, ISortError


def test_formatting_plugin_does_not_exist_initialization():
    """The exception should store the formatter name and inherit from ISortError."""
    formatter_name = "nonexistent_formatter"
    exc = FormattingPluginDoesNotExist(formatter_name)
    assert isinstance(exc, ISortError)
    assert exc.formatter == formatter_name
    assert str(exc) == f"Specified formatting plugin of {formatter_name} does not exist. "


def test_formatting_plugin_does_not_exist_message_content():
    """The error message should contain the formatter name and be a non-empty string."""
    formatter_name = "bad_plugin"
    exc = FormattingPluginDoesNotExist(formatter_name)
    message = str(exc)
    assert isinstance(message, str)
    assert message
    assert formatter_name in message
    assert message.endswith(" ")


def test_formatting_plugin_does_not_exist_repr_and_hash():
    """The exception should be hashable and its repr should include the formatter."""
    formatter_name = "missing"
    exc = FormattingPluginDoesNotExist(formatter_name)
    # Hashability
    assert hash(exc) == hash((FormattingPluginDoesNotExist, formatter_name))
    # Representation
    rep = repr(exc)
    assert isinstance(rep, str)
    assert formatter_name in rep
    assert "FormattingPluginDoesNotExist" in rep
