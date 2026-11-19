import pytest
from thefuck.logs import already_configured, color
from thefuck.conf import settings

def test_already_configured_with_reload(capsys):
    """Verify that the function prints the expected message with the reload command."""
    reload_cmd = "thefuck --reload"
    already_configured({"reload": reload_cmd})
    captured = capsys.readouterr()
    assert f"For applying changes run {reload_cmd}" in captured.out
    # Ensure the message contains the alias name
    assert "alias already configured" in captured.out
    # The function should return None
    assert already_configured({"reload": reload_cmd}) is None

def test_already_configured_no_colors(monkeypatch, capsys):
    """When no_colors is True, color codes should be stripped from the output."""
    monkeypatch.setattr(settings, "no_colors", True)
    reload_cmd = "thefuck --reload"
    already_configured({"reload": reload_cmd})
    captured = capsys.readouterr()
    # No ANSI escape sequences should be present
    assert "\x1b" not in captured.out
    # The reload command should still appear
    assert reload_cmd in captured.out

def test_color_function_respects_no_colors(monkeypatch):
    """The helper color() should return an empty string when colors are disabled."""
    monkeypatch.setattr(settings, "no_colors", True)
    assert color("anything") == ""
    monkeypatch.setattr(settings, "no_colors", False)
    # When colors are enabled, the original string should be returned
    assert color("test") == "test"
