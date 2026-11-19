import pytest
from isort.exceptions import FormattingPluginDoesNotExist, ISortError


def test_formatting_plugin_does_not_exist_initialization():
    """The exception should store the formatter name and produce the correct message."""
    formatter_name = "nonexistent_formatter"
    exc = FormattingPluginDoesNotExist(formatter_name)

    # The formatter attribute should be set correctly
    assert exc.formatter == formatter_name

    # The message should include the formatter name
    assert formatter_name in str(exc)
    assert "Specified formatting plugin of" in str(exc)


def test_formatting_plugin_does_not_exist_inherits_isort_error():
    """FormattingPluginDoesNotExist must be a subclass of ISortError."""
    exc = FormattingPluginDoesNotExist("foo")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_formatting_plugin_does_not_exist_raises_and_catches():
    """Raising the exception should propagate correctly and be catchable."""
    with pytest.raises(FormattingPluginDoesNotExist) as excinfo:
        raise FormattingPluginDoesNotExist("bad_plugin")

    # The caught exception should be the same instance
    assert excinfo.value.formatter == "bad_plugin"
    assert "bad_plugin" in str(excinfo.value)
