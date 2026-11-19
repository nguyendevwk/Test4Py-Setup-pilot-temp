import pytest
from thefuck.logs import color
from thefuck import conf

# Test that the function returns an empty string when colors are disabled
def test_color_returns_empty_when_no_colors(monkeypatch):
    # Disable colors
    monkeypatch.setattr(conf.settings, "no_colors", True)
    assert color("red") == ""

# Test that the function returns the original value when colors are enabled
def test_color_returns_original_when_colors_enabled(monkeypatch):
    # Enable colors
    monkeypatch.setattr(conf.settings, "no_colors", False)
    assert color("green") == "green"

# Test that the function correctly handles non-string input when colors are enabled
def test_color_with_non_string_input(monkeypatch):
    # Enable colors
    monkeypatch.setattr(conf.settings, "no_colors", False)
    # Pass an integer; the function should return it unchanged
    assert color(42) == 42
