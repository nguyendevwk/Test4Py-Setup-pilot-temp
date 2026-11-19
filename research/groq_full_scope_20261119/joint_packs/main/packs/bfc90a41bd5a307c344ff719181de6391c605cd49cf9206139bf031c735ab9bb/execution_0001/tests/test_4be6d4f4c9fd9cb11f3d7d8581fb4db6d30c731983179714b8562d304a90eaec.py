import importlib
import types
import pytest
from contextlib import contextmanager

# Import the target module
from thefuck.logs import color
from thefuck import conf

# Helper to temporarily set settings.no_colors
@contextmanager
def set_no_colors(value):
    original = conf.settings.no_colors
    conf.settings.no_colors = value
    try:
        yield
    finally:
        conf.settings.no_colors = original

def test_color_returns_color_when_enabled(tmp_path):
    """When colors are enabled, the function returns the passed color string."""
    with set_no_colors(False):
        result = color("red")
        assert result == "red", "Expected the original color string when colors are enabled"

def test_color_returns_empty_when_disabled(tmp_path):
    """When colors are disabled, the function returns an empty string."""
    with set_no_colors(True):
        result = color("green")
        assert result == "", "Expected an empty string when colors are disabled"

def test_color_with_non_string_input(tmp_path):
    """The function should return the string representation of non-string inputs when colors are enabled."""
    with set_no_colors(False):
        obj = 123
        result = color(obj)
        assert result == obj, "Expected the original non-string input to be returned unchanged"
