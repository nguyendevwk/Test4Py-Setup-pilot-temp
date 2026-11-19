import logging
import sys
import traceback
import types
import datetime
import pytest
from tornado.log import LogFormatter

# Helper to create a LogRecord with a specific message and level
def make_record(msg, level=logging.INFO, exc_info=None):
    return logging.LogRecord(
        name="test",
        level=level,
        pathname=__file__,
        lineno=10,
        msg=msg,
        args=(),
        exc_info=exc_info,
    )

def test_basic_formatting_no_color(tmp_path):
    # Instantiate formatter with color disabled to avoid terminal checks
    fmt = LogFormatter(color=False)
    record = make_record("Hello world", level=logging.INFO)
    formatted = fmt.format(record)
    # The formatted string should contain the message and level initial
    assert "Hello world" in formatted
    assert "[I" in formatted  # level initial
    # No ANSI escape codes should be present
    assert "\x1b" not in formatted

def test_bytes_message_conversion(tmp_path):
    # Pass a bytes message that cannot be decoded as utf-8
    bad_bytes = b"\xff\xfe\xfd"
    record = make_record(bad_bytes, level=logging.ERROR)
    fmt = LogFormatter(color=False)
    formatted = fmt.format(record)
    # The formatter should convert the bytes to a safe unicode representation
    # which will be a string containing the repr of the bytes
    assert "Bad message" not in formatted  # no exception
    assert "b'\\xff\\xfe\\xfd'" in formatted or "b'\\xff\\xfe\\xfd'" in formatted

def test_exception_info_inclusion(tmp_path):
    # Create an exception and capture its exc_info
    try:
        1 / 0
    except ZeroDivisionError:
        exc = sys.exc_info()
    record = make_record("Error occurred", level=logging.CRITICAL, exc_info=exc)
    fmt = LogFormatter(color=False)
    formatted = fmt.format(record)
    # The formatted string should include the exception traceback
    assert "ZeroDivisionError" in formatted
    # The traceback lines should be indented by four spaces
    assert "\n    " in formatted
    # The original message should appear before the traceback
    assert formatted.split("\n")[0].strip().endswith("Error occurred")
