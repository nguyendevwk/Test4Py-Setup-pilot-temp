import pytest
from isort.exceptions import UnsupportedSettings


def test_unsupported_settings_message_and_attribute(tmp_path):
    # Create a sample unsupported settings dictionary
    settings = {
        "line_length": {"value": 120, "source": "config"},
        "known_third_party": {"value": ["numpy"], "source": "cli"},
    }

    # Instantiate the exception
    exc = UnsupportedSettings(settings)

    # The exception message should contain each option formatted correctly
    assert "line_length = 120" in str(exc)
    assert "source: 'config'" in str(exc)
    assert "known_third_party = ['numpy']" in str(exc)
    assert "source: 'cli'" in str(exc)

    # The unsupported_settings attribute should be the original dict
    assert exc.unsupported_settings is settings
    assert exc.unsupported_settings["line_length"]["value"] == 120
    assert exc.unsupported_settings["known_third_party"]["source"] == "cli"


def test_unsupported_settings_empty_dict(tmp_path):
    # Passing an empty dict should still construct the exception without errors
    exc = UnsupportedSettings({})

    # The message should not contain any option lines
    msg = str(exc)
    assert "isort was provided settings that it doesn't support" in msg
    # No option lines should be present
    assert "\t- " not in msg

    # The attribute should be an empty dict
    assert exc.unsupported_settings == {}


def test_unsupported_settings_invalid_input_raises_type_error():
    # The constructor expects a dict; passing a non-dict should raise a TypeError
    with pytest.raises(TypeError):
        UnsupportedSettings([("line_length", {"value": 80, "source": "config"})])
