import sys
import io
import pytest
from contextlib import redirect_stderr
from thefuck.logs import exception, color
from thefuck import const
from thefuck.conf import settings

def test_exception_outputs_trace_and_title(monkeypatch):
    # Prepare a fake exception
    try:
        1 / 0
    except ZeroDivisionError:
        exc_info = sys.exc_info()

    # Capture stderr
    stderr = io.StringIO()
    with redirect_stderr(stderr):
        exception("Test Title", exc_info)

    output = stderr.getvalue()
    # Assert that the title is present
    assert "Test Title" in output
    # Assert that the trace contains the exception type
    assert "ZeroDivisionError" in output
    # Assert that the output ends with the separator line
    assert output.strip().endswith("----------------------------")

def test_exception_no_colors(monkeypatch):
    # Disable colors in settings
    monkeypatch.setattr(settings, "no_colors", True)

    # Prepare a fake exception
    try:
        int("abc")
    except ValueError:
        exc_info = sys.exc_info()

    # Capture stderr
    stderr = io.StringIO()
    with redirect_stderr(stderr):
        exception("Color Test", exc_info)

    output = stderr.getvalue()
    # When colors are disabled, no ANSI codes should appear
    assert "\x1b" not in output
    # Title and trace should still be present
    assert "Color Test" in output
    assert "ValueError" in output

def test_exception_invalid_exc_info_raises(monkeypatch):
    # Prepare an invalid exc_info (missing tuple elements)
    invalid_exc_info = (None, None)  # missing traceback

    with pytest.raises(TypeError):
        exception("Invalid", invalid_exc_info)
