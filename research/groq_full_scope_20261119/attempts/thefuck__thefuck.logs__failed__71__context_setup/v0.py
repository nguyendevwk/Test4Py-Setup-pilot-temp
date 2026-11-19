import sys
import builtins
import importlib
import types

import pytest

# Import the module under test
from thefuck import logs
from thefuck.conf import settings


def test_failed_with_colors(capsys, monkeypatch):
    """When colors are enabled, failed() writes a colored message to stderr."""
    # Ensure colors are enabled
    monkeypatch.setattr(settings, "no_colors", False)

    # Call the function with a sample message
    logs.failed("error occurred")

    # Capture stderr output
    captured = capsys.readouterr()
    # The output should contain the message surrounded by color codes
    assert "error occurred" in captured.err
    # The color codes should be present (colorama.Fore.RED and Style.RESET_ALL)
    assert "\x1b[31m" in captured.err  # RED
    assert "\x1b[0m" in captured.err   # RESET_ALL


def test_failed_without_colors(capsys, monkeypatch):
    """When colors are disabled, failed() writes a plain message to stderr."""
    # Disable colors
    monkeypatch.setattr(settings, "no_colors", True)

    # Call the function with a sample message
    logs.failed("simple error")

    # Capture stderr output
    captured = capsys.readouterr()
    # The output should be the plain message followed by a newline
    assert captured.err == "simple error\n"
    # No ANSI escape sequences should be present
    assert "\x1b[" not in captured.err


def test_color_function_behavior(monkeypatch):
    """The color helper returns the color code or an empty string based on settings."""
    # Test when colors are disabled
    monkeypatch.setattr(settings, "no_colors", True)
    assert logs.color(logs.colorama.Fore.GREEN) == ""

    # Test when colors are enabled
    monkeypatch.setattr(settings, "no_colors", False)
    assert logs.color(logs.colorama.Fore.GREEN) == logs.colorama.Fore.GREEN
