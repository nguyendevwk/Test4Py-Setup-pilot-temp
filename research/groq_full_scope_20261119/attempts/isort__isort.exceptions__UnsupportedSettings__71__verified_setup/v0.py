import pytest
from isort.exceptions import UnsupportedSettings


def test_unsupported_settings_empty_dict():
    """When no unsupported settings are provided, the error message should be minimal."""
    exc = UnsupportedSettings({})
    # The message should contain the introductory text but no option lines.
    assert "isort was provided settings that it doesn't support" in str(exc)
    # No tabulated options should appear.
    assert "\t-" not in str(exc)
    # The unsupported_settings attribute should be the empty dict passed in.
    assert exc.unsupported_settings == {}


def test_unsupported_settings_multiple_options():
    """The error message should list each unsupported setting with its value and source."""
    options = {
        "line_length": {"value": 88, "source": "config"},
        "known_third_party": {"value": ["requests"], "source": "cli"},
    }
    exc = UnsupportedSettings(options)
    msg = str(exc)
    # Each option should appear on its own line with correct formatting.
    assert "\t- line_length = 88  (source: 'config')" in msg
    assert "\t- known_third_party = ['requests']  (source: 'cli')" in msg
    # The attribute should reference the original dict.
    assert exc.unsupported_settings is options


def test_unsupported_settings_invalid_input_type():
    """Providing a non-dict to UnsupportedSettings should raise a TypeError."""
    with pytest.raises(TypeError):
        UnsupportedSettings([("key", {"value": 1, "source": "test"})])
