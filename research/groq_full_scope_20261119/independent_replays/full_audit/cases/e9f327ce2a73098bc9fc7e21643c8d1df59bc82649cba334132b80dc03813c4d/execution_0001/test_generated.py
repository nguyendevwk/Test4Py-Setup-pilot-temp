import io
import os
import sys
import time
import threading
import types
import pytest

# Import the target function and the module to patch globals
from httpie.uploads import observe_stdin_for_data_thread, is_windows

# Helper to capture stderr output
class StderrCapture(io.StringIO):
    def __enter__(self):
        self._stdout = sys.stderr
        sys.stderr = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stderr = self._stdout

@pytest.fixture
def env():
    """Simple mock Environment with a stderr attribute."""
    class MockEnv:
        def __init__(self):
            self.stderr = io.StringIO()
    return MockEnv()

def test_warning_emitted_after_timeout(monkeypatch, env, tmp_path):
    """When no data is read within READ_THRESHOLD, a warning is written."""
    # Ensure we are not on Windows
    monkeypatch.setattr('httpie.uploads.is_windows', False)
    # Set a small threshold for quick test
    monkeypatch.setattr('httpie.uploads.READ_THRESHOLD', 0.1)
    # Create a dummy file object (not used by the function)
    dummy_file = tmp_path / "dummy.txt"
    dummy_file.write_text("test")
    file_obj = dummy_file.open()
    read_event = threading.Event()

    observe_stdin_for_data_thread(env, file_obj, read_event)

    # Wait longer than threshold to allow thread to run
    time.sleep(0.2)
    # The warning should be present in env.stderr
    output = env.stderr.getvalue()
    assert "> warning: no stdin data read in 0.1s" in output
    assert "httpie.io/docs/cli/best-practices" in output

def test_no_warning_when_event_set(monkeypatch, env, tmp_path):
    """If the read_event is set before the timeout, no warning is emitted."""
    monkeypatch.setattr('httpie.uploads.is_windows', False)
    monkeypatch.setattr('httpie.uploads.READ_THRESHOLD', 0.1)
    dummy_file = tmp_path / "dummy.txt"
    dummy_file.write_text("test")
    file_obj = dummy_file.open()
    read_event = threading.Event()
    read_event.set()  # Simulate data already read

    observe_stdin_for_data_thread(env, file_obj, read_event)

    time.sleep(0.2)
    output = env.stderr.getvalue()
    assert output == ""

def test_no_thread_when_threshold_zero(monkeypatch, env, tmp_path):
    """When READ_THRESHOLD is 0, the function returns immediately without starting a thread."""
    monkeypatch.setattr('httpie.uploads.is_windows', False)
    monkeypatch.setattr('httpie.uploads.READ_THRESHOLD', 0)
    dummy_file = tmp_path / "dummy.txt"
    dummy_file.write_text("test")
    file_obj = dummy_file.open()
    read_event = threading.Event()

    observe_stdin_for_data_thread(env, file_obj, read_event)

    # No thread should be running; we can check by ensuring no warning after a delay
    time.sleep(0.2)
    output = env.stderr.getvalue()
    assert output == ""
