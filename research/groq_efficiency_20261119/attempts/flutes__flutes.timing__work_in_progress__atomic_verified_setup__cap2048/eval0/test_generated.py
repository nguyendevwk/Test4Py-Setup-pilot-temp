import builtins
import io
import os
import pickle
import time
import types
import contextlib

import pytest

from flutes.timing import work_in_progress


def test_context_manager_prints_and_times(tmp_path, capsys):
    """Verify that the context manager prints the description and elapsed time."""
    start = time.time()
    with work_in_progress("Test block"):
        # Simulate a short delay
        time.sleep(0.1)
    end = time.time()
    captured = capsys.readouterr()
    # The output should start with the description and end with "done."
    assert captured.out.startswith("Test block... ")
    assert captured.out.strip().endswith("done.")
    # The elapsed time printed should be close to the actual sleep duration
    elapsed_str = captured.out.strip().split("done. (")[1].rstrip(")")
    elapsed = float(elapsed_str.rstrip("s"))
    assert 0.09 <= elapsed <= 0.2
    # The total time measured by the test should be at least the sleep time
    assert end - start >= 0.09


def test_decorator_times_function(tmp_path, capsys):
    """Verify that the decorator works on a function and prints the correct timing."""
    @work_in_progress("Serialize")
    def serialize(obj, path):
        with open(path, "wb") as f:
            pickle.dump(obj, f)

    data = {"a": 1, "b": 2}
    file_path = tmp_path / "data.pkl"
    serialize(data, file_path)

    captured = capsys.readouterr()
    assert captured.out.startswith("Serialize... ")
    assert captured.out.strip().endswith("done.")
    # Ensure the file was written correctly
    with open(file_path, "rb") as f:
        loaded = pickle.load(f)
    assert loaded == data


def test_error_propagation_and_printing(tmp_path, capsys):
    """Verify that an exception inside the context manager propagates and the timing is still printed."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error block"):
            # Simulate work that raises an exception
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    assert captured.out.startswith("Error block... ")
    assert captured.out.strip().endswith("done.")
    # The exception message should be propagated
    with pytest.raises(RuntimeError, match="boom"):
        with work_in_progress("Another error"):
            raise RuntimeError("boom")
