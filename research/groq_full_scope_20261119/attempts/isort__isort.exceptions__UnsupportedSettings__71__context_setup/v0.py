import pytest
from isort.exceptions import UnsupportedSettings

def test_unsupported_settings_message_and_attribute():
    # Prepare a dictionary of unsupported settings with varied value types
    settings = {
        "line_length": {"value": 80, "source": "config"},
        "known_third_party": {"value": ["requests", "numpy"], "source": "cli"},
        "skip": {"value": None, "source": "runtime"},
    }
    # Instantiate the exception
    exc = UnsupportedSettings(settings)
    # The exception should store the original dictionary
    assert exc.unsupported_settings == settings
    # The message should contain each setting formatted correctly
    for name, option in settings.items():
        expected_line = f"\t- {name} = {option['value']}  (source: '{option['source']}')"
        assert expected_line in str(exc)
    # The message should start with the expected header
    assert str(exc).startswith("isort was provided settings that it doesn't support:")

def test_unsupported_settings_with_empty_dict():
    # An empty dictionary should still produce a valid exception
    exc = UnsupportedSettings({})
    # No errors should be listed in the message
    assert "errors" not in str(exc)
    # The unsupported_settings attribute should be an empty dict
    assert exc.unsupported_settings == {}

def test_unsupported_settings_format_option_static_method():
    # Test the static formatting method directly
    formatted = UnsupportedSettings._format_option(
        "include_trailing_comma", True, "config"
    )
    # The formatted string should match the expected pattern
    assert formatted == "\t- include_trailing_comma = True  (source: 'config')"
