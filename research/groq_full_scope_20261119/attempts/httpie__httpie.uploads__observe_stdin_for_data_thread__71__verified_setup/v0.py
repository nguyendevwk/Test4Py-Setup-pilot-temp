import io
import threading
import time
import types
import importlib
import pytest

# Import the target function and the module to patch globals
mod = importlib.import_module("httpie.uploads")
observe = mod.observe_stdin_for_data_thread
is_windows = mod.is_windows
READ_THRESHOLD = getattr(mod, "READ_THRESHOLD", 5)  # default if not defined


class DummyStderr:
    def __init__(self):
        self.written = []

    def write(self, msg: str):
        self.written.append(msg)


class DummyEnv:
    def __init__(self):
        self.stderr = DummyStderr()


def test_warning_is_written_when_no_input(monkeypatch):
    """When the read event is not set within READ_THRESHOLD, a warning is written."""
    # Ensure we are not on Windows and set a short threshold
    monkeypatch.setattr(mod, "is_windows", False)
    monkeypatch.setattr(mod, "READ_THRESHOLD", 0.1)

    env = DummyEnv()
    read_event = threading.Event()
    # Call the function; it starts a daemon thread
    observe(env, io.BytesIO(b""), read_event)

    # Wait longer than the threshold to allow the thread to run
    time.sleep(0.2)

    # The warning should have been written to stderr
    assert any("warning: no stdin data read" in msg for msg in env.stderr.written)


def test_no_warning_when_event_set(monkeypatch):
    """If the read event is set before the threshold, no warning is written."""
    monkeypatch.setattr(mod, "is_windows", False)
    monkeypatch.setattr(mod, "READ_THRESHOLD", 0.5)

    env = DummyEnv()
    read_event = threading.Event()
    observe(env, io.BytesIO(b""), read_event)

    # Set the event before the threshold expires
    time.sleep(0.1)
    read_event.set()

    # Wait to ensure thread would have run if it were to warn
    time.sleep(0.5)

    # No warning should have been written
    assert not env.stderr.written


def test_no_thread_when_windows_or_threshold_zero(monkeypatch):
    """On Windows or when READ_THRESHOLD is 0, the function returns immediately without starting a thread."""
    # Case 1: Windows
    monkeypatch.setattr(mod, "is_windows", True)
    env = DummyEnv()
    read_event = threading.Event()
    result = observe(env, io.BytesIO(b""), read_event)
    assert result is None
    assert not env.stderr.written

    # Case 2: Threshold zero
    monkeypatch.setattr(mod, "is_windows", False)
    monkeypatch.setattr(mod, "READ_THRESHOLD", 0)
    env2 = DummyEnv()
    read_event2 = threading.Event()
    result2 = observe(env2, io.BytesIO(b""), read_event2)
    assert result2 is None
    assert not env2.stderr.written
