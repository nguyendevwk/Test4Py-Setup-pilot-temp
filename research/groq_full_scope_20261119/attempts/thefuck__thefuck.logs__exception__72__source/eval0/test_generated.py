import sys
import io
import pytest
from thefuck.logs import exception
from traceback import TracebackException

def test_exception_outputs_title_and_trace(tmp_path):
    # Create a simple exception to capture
    try:
        1 / 0
    except ZeroDivisionError:
        exc_info = sys.exc_info()
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        exception("DivisionError", exc_info)
        output = sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr
    # Assert title is present
    assert "DivisionError" in output
    # Assert trace contains the exception type and message
    assert "ZeroDivisionError" in output
    assert "division by zero" in output
    # Assert separator line is present
    assert "----------------------------" in output

def test_exception_with_unicode_title_and_message(tmp_path):
    # Raise an exception with a unicode message
    try:
        raise ValueError("Ошибка: неверный ввод")
    except ValueError:
        exc_info = sys.exc_info()
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        exception("UnicodeTest", exc_info)
        output = sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr
    # Assert unicode title and message are present
    assert "UnicodeTest" in output
    assert "Ошибка: неверный ввод" in output

def test_exception_includes_color_codes(tmp_path):
    # Use a simple exception
    try:
        [][2]
    except IndexError:
        exc_info = sys.exc_info()
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        exception("IndexErrorTest", exc_info)
        output = sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr
    # The output should contain ANSI escape sequences for color
    # Colorama uses ESC character \x1b
    assert "\x1b[" in output
    # Ensure reset code is present
    assert "\x1b[0m" in output
