import logging
import sys
import types
import traceback
import pytest
from tornado.log import LogFormatter, _safe_unicode

# Helper to create a LogRecord with minimal required attributes
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

def test_basic_formatting_no_color(tmp_path):
    # Force no color by disabling _stderr_supports_color
    original = LogFormatter._stderr_supports_color if hasattr(LogFormatter, "_stderr_supports_color") else None
    try:
        LogFormatter._stderr_supports_color = lambda: False
        formatter = LogFormatter(color=False)
        record = make_record(logging.INFO, "Hello world")
        formatted = formatter.format(record)
        # The formatted string should contain the message and level initial
        assert "Hello world" in formatted
        assert "[I" in formatted  # level initial
        # No color codes should be present
        assert "\033[" not in formatted
    finally:
        if original is not None:
            LogFormatter._stderr_supports_color = original

def test_bytes_message_conversion(tmp_path):
    # Create a bytes message that is not valid UTF-8
    bad_bytes = b'\xff\xfe\xfd'
    record = make_record(logging.ERROR, bad_bytes)
    formatter = LogFormatter(color=False)
    formatted = formatter.format(record)
    # The formatter should convert the bytes to a repr string
    assert repr(bad_bytes) in formatted
    # Ensure no exception was raised during formatting
    assert "Bad message" not in formatted

def test_exception_formatting(tmp_path):
    try:
        raise ValueError("boom")
    except ValueError:
        exc_info = sys.exc_info()
    record = make_record(logging.ERROR, "An error occurred", exc_info=exc_info)
    formatter = LogFormatter(color=False)
    formatted = formatter.format(record)
    # The formatted string should contain the original message
    assert "An error occurred" in formatted
    # It should also contain the exception type and message
    assert "ValueError" in formatted
    assert "boom" in formatted
    # The exception traceback should be indented by four spaces
    assert "\n    " in formatted
