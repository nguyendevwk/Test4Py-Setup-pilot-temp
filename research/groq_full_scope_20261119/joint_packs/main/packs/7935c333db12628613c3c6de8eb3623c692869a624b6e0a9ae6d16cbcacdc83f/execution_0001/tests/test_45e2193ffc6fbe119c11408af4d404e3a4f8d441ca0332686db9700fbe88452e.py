import logging
import traceback
import sys
import types
import pytest
from tornado.log import LogFormatter

# Helper to create a LogRecord with a given level and message
def make_record(level, msg, exc_info=None):
    return logging.LogRecord(
        name="test",
        level=level,
        pathname=__file__,
        lineno=10,
        msg=msg,
        args=(),
        exc_info=exc_info,
    )

def test_basic_formatting_and_color_codes(tmp_path):
    # Create a formatter with color disabled to avoid terminal dependencies
    fmt = LogFormatter(color=False)
    record = make_record(logging.INFO, "Hello, world!")
    formatted = fmt.format(record)

    # The formatted string should contain the level initial, timestamp, module, line, and message
    assert "[I" in formatted  # level initial
    assert "Hello, world!" in formatted
    # No color escape sequences should be present
    assert "\033[" not in formatted
    # The timestamp should match the default date format
    assert any(ch.isdigit() for ch in formatted.split()[1])  # simple check for digits

def test_bytes_message_is_converted_to_unicode(tmp_path):
    # Create a formatter with color disabled
    fmt = LogFormatter(color=False)
    # Bytes message containing non‑ascii bytes
    bad_bytes = b"bad \xe9 message"
    record = make_record(logging.ERROR, bad_bytes)
    formatted = fmt.format(record)

    # The message should be converted to a string without raising an exception
    assert "bad" in formatted
    # The non‑ascii byte should be represented as a Unicode escape
    assert "\\xe9" in formatted or "é" in formatted

def test_exception_info_is_appended(tmp_path):
    # Create a formatter with color disabled
    fmt = LogFormatter(color=False)
    try:
        1 / 0
    except ZeroDivisionError:
        exc = sys.exc_info()
    record = make_record(logging.WARNING, "An error occurred", exc_info=exc)
    formatted = fmt.format(record)

    # The formatted string should contain the original message
    assert "An error occurred" in formatted
    # It should also contain the exception type and message
    assert "ZeroDivisionError" in formatted
    assert "division by zero" in formatted
    # The exception traceback should be indented on a new line
    assert "\n    " in formatted
