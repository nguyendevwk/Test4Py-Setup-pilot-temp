import importlib
import types
import pytest

# Import the target module
from thefuck.logs import color
from thefuck.conf import settings


def test_color_enabled(monkeypatch):
    """When colors are enabled, the function returns the passed value."""
    # Ensure colors are enabled
    monkeypatch.setattr(settings, "no_colors", False)
    assert color("red") == "red"
    assert color(123) == 123  # any value should be returned unchanged


def test_color_disabled(monkeypatch):
    """When colors are disabled, the function returns an empty string."""
    # Disable colors
    monkeypatch.setattr(settings, "no_colors", True)
    assert color("red") == ""
    assert color(123) == ""  # numeric values are also suppressed


def test_color_with_none(monkeypatch):
    """Passing None should return None when colors are enabled and '' when disabled."""
    monkeypatch.setattr(settings, "no_colors", False)
    assert color(None) is None
    monkeypatch.setattr(settings, "no_colors", True)
    assert color(None) == ""
