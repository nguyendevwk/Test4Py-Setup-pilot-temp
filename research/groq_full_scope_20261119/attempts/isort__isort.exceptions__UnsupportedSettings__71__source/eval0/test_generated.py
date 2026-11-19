import pytest
from isort.exceptions import UnsupportedSettings

def test_unsupported_settings_initialization_and_attribute():
    """Verify that the exception stores the provided settings and formats the message correctly."""
    settings = {
        "line_length": {"value": 88, "source": "config"},
        "known_third_party": {"value": ["requests"], "source": "cli"},
    }
    exc = UnsupportedSettings(settings)

    # The attribute should be exactly the dict passed in
    assert exc.unsupported_settings is settings

    # The message should contain each option formatted with a tab and the source
    for name, option in settings.items():
        expected_line = f"\t- {name} = {option['value']}  (source: '{option['source']}')"
        assert expected_line in str(exc)

    # The message should start with the standard header
    assert str(exc).startswith("isort was provided settings that it doesn't support:")


def test_unsupported_settings_with_empty_dict():
    """An empty settings dict should produce a message without any option lines."""
    exc = UnsupportedSettings({})
    msg = str(exc)

    # No option lines should be present
    assert "\t-" not in msg

    # The message should still contain the header and the final URL
    assert "isort was provided settings that it doesn't support:" in msg
    assert "https://isort.readthedocs.io/en/latest/configuration/options.html" in msg


def test_unsupported_settings_invalid_input_raises_type_error():
    """Passing a non-dict to UnsupportedSettings should raise a TypeError due to dict unpacking."""
    with pytest.raises(TypeError):
        UnsupportedSettings([("name", {"value": 1, "source": "test"})])
