import io
import os
import sys
import time
import threading
import types
import builtins
import importlib
import pytest

# Import the target function and related globals
from httpie.uploads import observe_stdin_for_data_thread, READ_THRESHOLD, is_windows

# Helper to create a minimal Environment with a writable stderr
class DummyEnv:
    def __init__(self):
        self.stderr = io.StringIO()

# Test that a warning is emitted when no data is read within the threshold
def test_observe_stdin_warning_emitted(monkeypatch, tmp_path):
    # Ensure we are not on Windows and set a short threshold
    monkeypatch.setattr('httpie.uploads.is_windows', False)
    monkeypatch.setattr('httpie.uploads.READ_THRESHOLD', 0.1)

    env = DummyEnv()
    read_event = threading.Event()

    # Capture the thread start time
    start = time.time()
    observe_stdin_for_data_thread(env, sys.stdin, read_event)

    # Wait longer than the threshold to allow the warning to be written
    time.sleep(0.2)

    # The warning should be present in stderr
    output = env.stderr.getvalue()
    assert '> warning: no stdin data read in 0.1s' in output
    # Ensure the warning is emitted after the threshold
    assert time.time() - start >= 0.1

# Test that no warning is emitted if the event is set before the threshold
def test_observe_stdin_no_warning_when_event_set(monkeypatch, tmp_path):
    monkeypatch.setattr('httpie.uploads.is_windows', False)
    monkeypatch.setattr('httpie.uploads.READ_THRESHOLD', 0.5)

    env = DummyEnv()
    read_event = threading.Event()

    observe_stdin_for_data_thread(env, sys.stdin, read_event)

    # Set the event before the threshold expires
    read_event.set()

    # Wait a bit to ensure the thread would have fired if it were to
    time.sleep(0.6)

    # No warning should be present
    assert env.stderr.getvalue() == ''

# Test that when READ_THRESHOLD is zero, the function returns immediately
def test_observe_stdin_no_thread_when_threshold_zero(monkeypatch, tmp_path):
    monkeypatch.setattr('httpie.uploads.is_windows', False)
    monkeypatch.setattr('httpie.uploads.READ_THRESHOLD', 0)

    env = DummyEnv()
    read_event = threading.Event()

    observe_stdin_for_data_thread(env, sys.stdin, read_event)

    # Since threshold is zero, no thread should be started and no warning emitted
    assert env.stderr.getvalue() == ''
