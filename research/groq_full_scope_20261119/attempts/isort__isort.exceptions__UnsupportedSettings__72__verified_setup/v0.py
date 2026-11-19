import pytest
from isort.exceptions import UnsupportedSettings


def test_unsupported_settings_message_and_attribute():
    """Verify that the exception message contains the formatted options
    and that the unsupported_settings attribute is stored correctly."""
    settings = {
        "line_length": {"value": 80, "source": "config"},
        "known_third_party": {"value": ["numpy"], "source": "cli"},
    }
    exc = UnsupportedSettings(settings)

    # The message should start with the standard header
    assert exc.args[0].startswith(
        "isort was provided settings that it doesn't support:\n\n"
    )

    # Each option should appear in the message with correct formatting
    for name, option in settings.items():
        expected_line = f"\t- {name} = {option['value']}  (source: '{option['source']}')"
        assert expected_line in exc.args[0]

    # The attribute should be the same dictionary passed in
    assert exc.unsupported_settings is settings


def test_unsupported_settings_empty_dict():
    """An empty dictionary should produce a message with no option lines."""
    exc = UnsupportedSettings({})
    # The message should contain the header and no option lines
    assert exc.args[0].startswith(
        "isort was provided settings that it doesn't support:\n\n"
    )
    # After the header, there should be two newlines and then the final link
    # So the message should not contain any tab characters
    assert "\t" not in exc.args[0]
    # The unsupported_settings attribute should be an empty dict
    assert exc.unsupported_settings == {}


def test_unsupported_settings_invalid_input_type():
    """Passing a non-dict type should raise a TypeError during message formatting."""
    with pytest.raises(TypeError):
        UnsupportedSettings([("line_length", {"value": 80, "source": "config"})])
