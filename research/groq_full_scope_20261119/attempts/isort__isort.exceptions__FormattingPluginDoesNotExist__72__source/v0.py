import pytest
from isort.exceptions import FormattingPluginDoesNotExist, ISortError


def test_message_contains_formatter():
    """The exception message should include the formatter name."""
    formatter_name = "nonexistent_plugin"
    exc = FormattingPluginDoesNotExist(formatter_name)
    assert formatter_name in str(exc)
    assert "Specified formatting plugin" in str(exc)


def test_attribute_set_correctly():
    """The formatter attribute should be stored on the exception instance."""
    formatter_name = "my_plugin"
    exc = FormattingPluginDoesNotExist(formatter_name)
    assert hasattr(exc, "formatter")
    assert exc.formatter == formatter_name


def test_inheritance_from_isort_error():
    """FormattingPluginDoesNotExist must inherit from ISortError."""
    exc = FormattingPluginDoesNotExist("foo")
    assert isinstance(exc, ISortError)
