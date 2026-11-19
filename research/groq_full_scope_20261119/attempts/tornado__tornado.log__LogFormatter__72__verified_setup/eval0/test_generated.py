import logging
import sys
import types
import datetime
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

def test_basic_formatting_no_color(monkeypatch):
    # Disable color support by monkeypatching the helper that checks terminal
    monkeypatch.setattr("tornado.log._stderr_supports_color", lambda: False)
    fmt = LogFormatter(color=False)
    record = make_record(logging.INFO, "Hello world")
    formatted = fmt.format(record)
    # The formatted string should contain the level initial, timestamp, module, line, and message
    assert "[I" in formatted
    assert "Hello world" in formatted
    # No color escape sequences should be present
    assert "\033[" not in formatted

def test_color_mapping_and_timestamp(monkeypatch):
    # Enable color support by faking a terminal that supports it
    monkeypatch.setattr("tornado.log._stderr_supports_color", lambda: True)
    # Fake curses module with minimal interface
    fake_curses = types.SimpleNamespace()
    fake_curses.tigetstr = lambda name: b"\x1b[2;3%dm" if name in ("setaf", "setf") else b"\x1b[0m"
    fake_curses.tparm = lambda seq, code: seq % code
    monkeypatch.setitem(sys.modules, "curses", fake_curses)
    fmt = LogFormatter(color=True)
    record = make_record(logging.ERROR, "Error occurred")
    formatted = fmt.format(record)
    # The formatted string should start with the ANSI escape code for red
    assert formatted.startswith("\033[2;31m")
    # The reset code should appear after the message
    assert "\033[0m" in formatted
    # Timestamp should match the default date format
    timestamp = datetime.datetime.now().strftime(fmt.datefmt)
    assert timestamp in formatted

def test_bad_message_handling():
    # Create a record with a message that will raise an exception when converted to string
    class BadStr:
        def __str__(self):
            raise ValueError("bad conversion")
    bad_msg = BadStr()
    record = make_record(logging.WARNING, bad_msg)
    fmt = LogFormatter()
    formatted = fmt.format(record)
    # The formatter should catch the exception and include a diagnostic message
    assert "Bad message" in formatted
    assert "bad conversion" in formatted
    # The rest of the record should still be formatted correctly
    assert "[W" in formatted
    assert "test" in formatted
