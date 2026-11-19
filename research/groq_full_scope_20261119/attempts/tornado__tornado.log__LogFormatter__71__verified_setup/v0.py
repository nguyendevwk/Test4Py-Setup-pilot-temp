import logging
import sys
import types
import builtins
import importlib
import io
import contextlib

import pytest

# Import the target class
from tornado.log import LogFormatter

# Helper to create a LogRecord
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

# Test 1: Normal formatting with color disabled
def test_logformatter_no_color(tmp_path):
    # Disable color by passing color=False
    formatter = LogFormatter(color=False)
    record = make_record(logging.INFO, "Hello world")
    formatted = formatter.format(record)
    # The formatted string should contain the message and level initial
    assert "Hello world" in formatted
    assert "[I" in formatted  # level initial
    # No ANSI escape codes should be present
    assert "\033[" not in formatted

# Test 2: Level not in colors mapping
def test_logformatter_unknown_level():
    # Provide a custom colors dict that excludes WARNING
    formatter = LogFormatter(colors={logging.INFO: 2, logging.ERROR: 1})
    record = make_record(logging.WARNING, "Warn message")
    formatted = formatter.format(record)
    # Since WARNING not in colors, color and end_color should be empty
    assert "\033[" not in formatted
    assert "[W" in formatted
    assert "Warn message" in formatted

# Test 3: Message that raises an exception during formatting
def test_logformatter_bad_message():
    # Create a message that will raise when converted to string
    class BadStr:
        def __str__(self):
            raise ValueError("bad conversion")
    bad_msg = BadStr()
    formatter = LogFormatter()
    record = make_record(logging.ERROR, bad_msg)
    formatted = formatter.format(record)
    # The formatter should catch the exception and include it in the output
    assert "Bad message" in formatted
    assert "ValueError" in formatted
    # The original message should not appear
    assert str(bad_msg) not in formatted
