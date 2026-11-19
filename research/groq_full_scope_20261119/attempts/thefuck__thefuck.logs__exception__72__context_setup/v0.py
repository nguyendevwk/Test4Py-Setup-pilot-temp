import sys
import io
import pytest
from thefuck.logs import exception, color
from thefuck.conf import settings
from traceback import format_exception


def test_exception_writes_trace_and_title(capsys):
    """The exception function should write the title and traceback to stderr."""
    # Create a dummy exception info
    try:
        1 / 0
    except ZeroDivisionError:
        exc_info = sys.exc_info()

    # Capture stderr
    exception("Test Title", exc_info)
    captured = capsys.readouterr()
    # Check that the title appears
    assert "Test Title" in captured.err
    # Check that the traceback contains the exception message
    assert "ZeroDivisionError" in captured.err
    # Check that the separator line is present
    assert "----------------------------" in captured.err


def test_exception_no_colors(monkeypatch, capsys):
    """When settings.no_colors is True, the output should not contain ANSI codes."""
    # Temporarily disable colors
    monkeypatch.setattr(settings, "no_colors", True)

    try:
        int("abc")
    except ValueError:
        exc_info = sys.exc_info()

    exception("Color Test", exc_info)
    captured = capsys.readouterr()
    # ANSI codes start with \x1b, ensure none are present
    assert "\x1b" not in captured.err
    # Title should still be present
    assert "Color Test" in captured.err
    # Reset the setting for other tests
    monkeypatch.setattr(settings, "no_colors", False)


def test_exception_with_empty_exc_info_raises_type_error():
    """Providing an invalid exc_info tuple should raise a TypeError."""
    with pytest.raises(TypeError):
        exception("Invalid", (None, None, None))
