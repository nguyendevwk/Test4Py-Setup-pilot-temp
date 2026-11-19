import builtins
import io
import sys
import types

import pytest

# Import the target function and the settings module
from thefuck.logs import already_configured
from thefuck.conf import settings


def _capture_stdout(func, *args, **kwargs):
    """Helper to capture stdout of a function call."""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        result = func(*args, **kwargs)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return result, output


def test_already_configured_prints_reload_and_returns_none():
    """The function should print the reload command and return None."""
    # Create a simple configuration_details object with a reload attribute
    config = types.SimpleNamespace(reload="thefuck reload")
    result, output = _capture_stdout(already_configured, config)

    # Assert that the function returns None
    assert result is None

    # Assert that the output contains the reload command
    assert "thefuck reload" in output

    # Assert that the output contains the word "alias already configured"
    assert "alias already configured" in output


def test_already_configured_no_colors_when_disabled():
    """When settings.no_colors is True, the output should not contain ANSI codes."""
    # Temporarily disable colors
    original_no_colors = settings.no_colors
    settings.no_colors = True
    try:
        config = types.SimpleNamespace(reload="thefuck reload")
        _, output = _capture_stdout(already_configured, config)

        # ANSI escape sequences start with \x1b[; ensure none are present
        assert "\x1b[" not in output
    finally:
        settings.no_colors = original_no_colors


def test_already_configured_handles_special_reload_string():
    """The function should correctly embed a reload string containing special characters."""
    special_reload = "thefuck reload --force --verbose"
    config = types.SimpleNamespace(reload=special_reload)
    _, output = _capture_stdout(already_configured, config)

    # The output should contain the exact special reload string
    assert special_reload in output
    # Ensure the string is not truncated or altered
    assert output.count(special_reload) == 1
