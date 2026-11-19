import io
import os
import time
import threading
import types
import sys
import pytest

# Import the target function and the module to access globals
import httpie.uploads as uploads

# Helper Environment mock
class DummyEnv:
    def __init__(self):
        self.stderr = io.StringIO()

# Test 1: Normal warning emission after timeout
def test_observe_stdin_warning_emitted(tmp_path):
    # Ensure we are not on Windows and set a small threshold
    uploads.is_windows = False
    uploads.READ_THRESHOLD = 0.1

    env = DummyEnv()
    read_event = threading.Event()

    # Call the function which starts the thread
    uploads.observe_stdin_for_data_thread(env, io.BytesIO(b""), read_event)

    # Wait longer than the threshold to allow the warning to be written
    time.sleep(0.2)

    # The warning should now be present in stderr
    stderr_output = env.stderr.getvalue()
    assert "> warning: no stdin data read in 0.1s" in stderr_output
    assert "httpie.io/docs/cli/best-practices" in stderr_output

# Test 2: No warning when READ_THRESHOLD is zero
def test_no_warning_when_threshold_zero(tmp_path):
    uploads.is_windows = False
    uploads.READ_THRESHOLD = 0

    env = DummyEnv()
    read_event = threading.Event()

    uploads.observe_stdin_for_data_thread(env, io.BytesIO(b""), read_event)

    # Wait to ensure no thread runs
    time.sleep(0.2)

    # stderr should remain empty
    assert env.stderr.getvalue() == ""

# Test 3: Function returns immediately on Windows
def test_returns_none_on_windows(tmp_path):
    uploads.is_windows = True
    uploads.READ_THRESHOLD = 0.1  # value irrelevant on Windows

    env = DummyEnv()
    read_event = threading.Event()

    result = uploads.observe_stdin_for_data_thread(env, io.BytesIO(b""), read_event)

    # The function should return None and not start a thread
    assert result is None
    # No warning should be written
    assert env.stderr.getvalue() == ""
