import os
import time
import threading
import importlib
import sys
import types

import pytest

# Import the target module
import httpie.uploads as uploads

# Helper Environment that captures stderr writes
class DummyEnv:
    def __init__(self):
        self.stderr = DummyStderr()

class DummyStderr:
    def __init__(self):
        self.contents = []

    def write(self, msg):
        self.contents.append(msg)

    def getvalue(self):
        return "".join(self.contents)

@pytest.mark.timeout(5)
def test_warning_emitted_when_no_stdin_data(monkeypatch):
    # Set a very small threshold to trigger warning quickly
    monkeypatch.setenv("HTTPIE_STDIN_READ_WARN_THRESHOLD", "0.1")
    # Reload module to pick up new env var
    importlib.reload(uploads)

    env = DummyEnv()
    read_event = threading.Event()
    # Use a dummy file object
    file_obj = open(os.devnull, "rb")

    uploads.observe_stdin_for_data_thread(env, file_obj, read_event)

    # Wait longer than threshold to allow thread to run
    time.sleep(0.2)

    # The warning should have been written to stderr
    warning = env.stderr.getvalue()
    assert "> warning: no stdin data read in" in warning
    assert "HTTPIE_STDIN_READ_WARN_THRESHOLD" not in warning  # just check format

    file_obj.close()

@pytest.mark.timeout(5)
def test_no_warning_when_event_set(monkeypatch):
    # Set threshold to a small value
    monkeypatch.setenv("HTTPIE_STDIN_READ_WARN_THRESHOLD", "0.1")
    importlib.reload(uploads)

    env = DummyEnv()
    read_event = threading.Event()
    file_obj = open(os.devnull, "rb")

    # Set the event before calling the function
    read_event.set()
    uploads.observe_stdin_for_data_thread(env, file_obj, read_event)

    # Wait to ensure thread would have had time to warn if it were to
    time.sleep(0.2)

    # No warning should be present
    assert env.stderr.getvalue() == ""

    file_obj.close()

def test_no_thread_started_on_windows(monkeypatch):
    # Force the module to think it's running on Windows
    monkeypatch.setattr(uploads, "is_windows", True)

    env = DummyEnv()
    read_event = threading.Event()
    file_obj = open(os.devnull, "rb")

    # Capture current thread count
    before = threading.active_count()

    uploads.observe_stdin_for_data_thread(env, file_obj, read_event)

    # Wait a short time to ensure no background thread starts
    time.sleep(0.1)

    after = threading.active_count()
    # No new threads should have been created
    assert after == before

    file_obj.close()
