import pytest
from isort.exceptions import UnsupportedSettings, ISortError


def test_unsupported_settings_message_and_attribute():
    """Verify that the exception message contains all provided options and the attribute is stored."""
    settings = {
        "line_length": {"value": 80, "source": "config"},
        "multi_line_output": {"value": 3, "source": "cli"},
    }
    exc = UnsupportedSettings(settings)

    # The message should list each option in the format defined by _format_option
    assert "line_length = 80  (source: 'config')" in str(exc)
    assert "multi_line_output = 3  (source: 'cli')" in str(exc)

    # The stored attribute should match the input dictionary
    assert exc.unsupported_settings == settings


def test_unsupported_settings_empty_dict():
    """An empty dictionary should produce a message with no option lines."""
    exc = UnsupportedSettings({})
    msg = str(exc)
    # The message should not contain any option lines
    assert "\t- " not in msg
    # The attribute should be an empty dict
    assert exc.unsupported_settings == {}


def test_unsupported_settings_is_subclass_of_isort_error():
    """Ensure UnsupportedSettings inherits from ISortError and behaves like a normal exception."""
    settings = {"foo": {"value": "bar", "source": "test"}}
    exc = UnsupportedSettings(settings)
    # isinstance checks
    assert isinstance(exc, UnsupportedSettings)
    assert isinstance(exc, ISortError)
    # Raising and catching the exception
    with pytest.raises(UnsupportedSettings) as cm:
        raise exc
    assert cm.value is exc
