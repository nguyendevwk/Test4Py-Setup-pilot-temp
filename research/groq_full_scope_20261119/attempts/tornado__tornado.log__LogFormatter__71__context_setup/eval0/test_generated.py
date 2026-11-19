import logging
import sys
import types
import builtins
import importlib
import inspect

import pytest

# Import the target class from the module under test
from tornado.log import LogFormatter

# Helper to create a LogRecord with minimal required attributes
def make_record(level, msg, exc_info=None):
    logger = logging.getLogger("test")
    return logger.makeRecord(
        name="test",
        level=level,
        fn="test_module.py",
        lno=42,
        msg=msg,
        args=(),
        exc_info=exc_info,
    )

# ---------------------------------------------------------------------------

def test_basic_formatting_no_color(tmp_path):
    """Verify that a normal message is formatted correctly without color."""
    formatter = LogFormatter(color=False)
    record = make_record(logging.INFO, "Hello, world!")
    formatted = formatter.format(record)

    # The formatted string should contain the level initial, timestamp,
    # module name, line number, and the message itself.
    assert "[I" in formatted  # level initial
    assert "test_module.py:42" in formatted
    assert "Hello, world!" in formatted
    # No ANSI escape sequences should be present
    assert "\x1b" not in formatted

# ---------------------------------------------------------------------------

def test_bytes_message_conversion():
    """Verify that a byte string message is safely converted to unicode."""
    formatter = LogFormatter(color=False)
    # Create a byte string that cannot be decoded as UTF-8
    bad_bytes = b'\xff\xfe\xfd'
    record = make_record(logging.ERROR, bad_bytes)
    formatted = formatter.format(record)

    # The message should be represented by repr(bad_bytes)
    assert "Bad message" not in formatted  # no exception
    assert repr(bad_bytes) in formatted
    # The level initial should still be present
    assert "[E" in formatted

# ---------------------------------------------------------------------------

def test_exception_formatting():
    """Verify that exception information is appended correctly."""
    formatter = LogFormatter(color=False)
    try:
        1 / 0
    except ZeroDivisionError:
        exc_info = sys.exc_info()
    else:
        exc_info = None

    record = make_record(logging.CRITICAL, "An error occurred", exc_info=exc_info)
    formatted = formatter.format(record)

    # The formatted string should contain the exception type and message
    assert "ZeroDivisionError" in formatted
    assert "division by zero" in formatted
    # The exception block should be indented by four spaces
    assert "\n    " in formatted
    # The level initial should be present
    assert "[C" in formatted
