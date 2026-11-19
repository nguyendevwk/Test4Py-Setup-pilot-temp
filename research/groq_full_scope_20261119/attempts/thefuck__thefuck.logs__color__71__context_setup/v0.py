import importlib
import types
import pytest

# Import the module under test
import thefuck.logs as logs


def test_color_returns_color_when_enabled(monkeypatch):
    """When no_colors is False, the function should return the provided color string."""
    # Ensure the setting is False
    monkeypatch.setattr(logs.settings, "no_colors", False)
    # Reload the module to pick up the patched setting
    importlib.reload(logs)
    result = logs.color("red")
    assert result == "red", "Expected the original color string to be returned when colors are enabled"


def test_color_returns_empty_when_disabled(monkeypatch):
    """When no_colors is True, the function should return an empty string regardless of input."""
    monkeypatch.setattr(logs.settings, "no_colors", True)
    importlib.reload(logs)
    result = logs.color("blue")
    assert result == "", "Expected an empty string when colors are disabled"


def test_color_accepts_non_string_input(monkeypatch):
    """The function should return the input unchanged if it is not a string and colors are enabled."""
    monkeypatch.setattr(logs.settings, "no_colors", False)
    importlib.reload(logs)
    # Pass an integer; the function should return the integer unchanged
    result = logs.color(42)
    assert result == 42, "Expected the original non-string input to be returned unchanged"
