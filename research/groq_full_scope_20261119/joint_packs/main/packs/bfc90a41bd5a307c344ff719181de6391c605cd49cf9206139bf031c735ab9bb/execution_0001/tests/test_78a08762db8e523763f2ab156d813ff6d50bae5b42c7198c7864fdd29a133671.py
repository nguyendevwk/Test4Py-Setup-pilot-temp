import importlib
import types
import sys
import pytest

# Import the target module
from thefuck.logs import color
from thefuck import conf

# Helper to temporarily set settings.no_colors
class _NoColorsContext:
    def __init__(self, value):
        self.value = value
        self.original = conf.settings.no_colors

    def __enter__(self):
        conf.settings.no_colors = self.value

    def __exit__(self, exc_type, exc_val, exc_tb):
        conf.settings.no_colors = self.original

def test_color_returns_color_when_enabled():
    """When colors are enabled, the function returns the provided color string."""
    with _NoColorsContext(False):
        assert color("red") == "red"

def test_color_returns_empty_when_disabled():
    """When colors are disabled, the function returns an empty string regardless of input."""
    with _NoColorsContext(True):
        assert color("red") == ""
        assert color("any") == ""

def test_color_handles_empty_string_input():
    """The function should correctly handle an empty string input."""
    with _NoColorsContext(False):
        assert color("") == ""
