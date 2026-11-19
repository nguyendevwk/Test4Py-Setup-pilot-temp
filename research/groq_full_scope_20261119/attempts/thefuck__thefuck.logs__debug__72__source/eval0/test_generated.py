import sys
import io
import contextlib
import pytest
from thefuck.logs import debug
from thefuck import conf

# Helper to capture stderr
@contextlib.contextmanager
def capture_stderr():
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        yield sys.stderr
    finally:
        sys.stderr = old_stderr

def test_debug_enabled_writes_formatted_message(tmp_path):
    # Enable debug mode
    conf.settings.debug = True
    msg = "Test message"
    with capture_stderr() as err:
        debug(msg)
    output = err.getvalue()
    # The output should contain the message and the ANSI reset code
    assert msg in output
    assert "DEBUG:" in output
    assert "\x1b[0m" in output  # reset code from colorama

def test_debug_disabled_does_not_write(tmp_path):
    # Disable debug mode
    conf.settings.debug = False
    msg = "Should not appear"
    with capture_stderr() as err:
        debug(msg)
    output = err.getvalue()
    # No output should be produced
    assert output == ""

def test_debug_with_unicode_message(tmp_path):
    # Enable debug mode
    conf.settings.debug = True
    msg = "Unicode test: 測試"
    with capture_stderr() as err:
        debug(msg)
    output = err.getvalue()
    # Ensure unicode characters are preserved
    assert "測試" in output
    assert msg in output
