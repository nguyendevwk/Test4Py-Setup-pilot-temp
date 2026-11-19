import time
import pickle
import os
import builtins
import contextlib
import pytest
from flutes.timing import work_in_progress

def test_decorator_with_sleep(tmp_path, capsys):
    """Decorator should time a function and print the correct format."""
    @work_in_progress("Sleeping")
    def sleepy(seconds):
        time.sleep(seconds)
        return seconds

    result = sleepy(0.1)
    captured = capsys.readouterr()
    assert result == 0.1
    assert captured.out.startswith("Sleeping... ")
    assert captured.out.endswith("done. (")
    # Ensure the printed duration is close to the sleep time
    duration_str = captured.out.split("done. (")[1].rstrip("s)")
    duration = float(duration_str)
    assert 0.09 <= duration <= 0.2

def test_context_manager_with_file(tmp_path, capsys):
    """Context manager should time a block and print the correct format."""
    file_path = tmp_path / "test.bin"
    data = {"key": "value"}
    with work_in_progress("Writing file"):
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
    captured = capsys.readouterr()
    assert captured.out.startswith("Writing file... ")
    assert captured.out.endswith("done. (")
    # Verify file was written correctly
    with open(file_path, "rb") as f:
        loaded = pickle.load(f)
    assert loaded == data

def test_error_propagation_and_timing(tmp_path, capsys):
    """An exception inside the timed block should propagate and still print timing."""
    file_path = tmp_path / "error.bin"
    with pytest.raises(RuntimeError):
        with work_in_progress("Error block"):
            with open(file_path, "wb") as f:
                pickle.dump({"a": 1}, f)
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    assert captured.out.startswith("Error block... ")
    assert captured.out.endswith("done. (")
    # Ensure the file was created before the exception
    assert file_path.exists()
