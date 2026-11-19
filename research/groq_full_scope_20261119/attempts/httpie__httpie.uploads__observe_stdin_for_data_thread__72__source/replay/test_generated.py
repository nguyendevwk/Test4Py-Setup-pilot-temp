import sys
import io
import time
import threading
import types
import importlib
import pytest

# Import the target module
from httpie.uploads import observe_stdin_for_data_thread, Environment

# Helper to create a dummy Environment with stderr capturing
class DummyEnv:
    def __init__(self):
        self.stderr = io.StringIO()

# Test 1: On non‑Windows, with READ_THRESHOLD > 0, a warning is emitted after the timeout
def test_observe_stdin_warning_emitted(tmp_path):
    mod = importlib.reload(importlib.import_module("httpie.uploads"))
    # Ensure we are not on Windows
    mod.is_windows = False
    # Set a short threshold
    mod.READ_THRESHOLD = 0.1
    env = DummyEnv()
    read_event = threading.Event()
    # Use a dummy file object
    dummy_file = io.BytesIO(b"")
    observe_stdin_for_data_thread(env, dummy_file, read_event)
    # Wait longer than the threshold to allow the thread to run
    time.sleep(0.2)
    output = env.stderr.getvalue()
    assert "> warning: no stdin data read in 0.1s" in output

# Test 2: When READ_THRESHOLD is 0, no warning is emitted and no thread is started
def test_observe_stdin_no_threshold(tmp_path):
    mod = importlib.reload(importlib.import_module("httpie.uploads"))
    mod.is_windows = False
    mod.READ_THRESHOLD = 0
    env = DummyEnv()
    read_event = threading.Event()
    dummy_file = io.BytesIO(b"")
    observe_stdin_for_data_thread(env, dummy_file, read_event)
    # Wait to ensure no thread would have run
    time.sleep(0.1)
    output = env.stderr.getvalue()
    assert output == ""

# Test 3: On Windows, the function returns immediately and does not start a thread
def test_observe_stdin_windows(monkeypatch):
    mod = importlib.reload(importlib.import_module("httpie.uploads"))
    # Simulate Windows environment
    monkeypatch.setattr(mod, "is_windows", True)
    env = DummyEnv()
    read_event = threading.Event()
    dummy_file = io.BytesIO(b"")
    result = observe_stdin_for_data_thread(env, dummy_file, read_event)
    assert result is None
    # No warning should be written
    assert env.stderr.getvalue() == ""
