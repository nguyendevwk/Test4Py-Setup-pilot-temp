import time
import pickle
import os
import pytest
from flutes.timing import work_in_progress

def test_decorator_prints_and_times(tmp_path, capsys):
    """Test that the decorator prints the description and timing."""
    # Create a small pickle file
    data = {"a": 1}
    file_path = tmp_path / "data.pkl"
    with open(file_path, "wb") as f:
        pickle.dump(data, f)

    @work_in_progress("Loading file")
    def load_file(path):
        with open(path, "rb") as f:
            return pickle.load(f)

    start = time.time()
    result = load_file(str(file_path))
    end = time.time()
    captured = capsys.readouterr()

    # The result should match the original data
    assert result == data
    # The output should contain the description and a timing
    assert captured.out.startswith("Loading file... ")
    assert "done. (" in captured.out
    # The reported time should be within a reasonable range
    reported_time = float(captured.out.split("done. (")[1].rstrip("s)\n"))
    assert 0 <= reported_time <= end - start + 0.1

def test_context_manager_prints_and_times(tmp_path, capsys):
    """Test that the context manager prints the description and timing."""
    # Create a small pickle file
    data = {"b": 2}
    file_path = tmp_path / "data2.pkl"
    with open(file_path, "wb") as f:
        pickle.dump(data, f)

    start = time.time()
    with work_in_progress("Saving file"):
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
    end = time.time()
    captured = capsys.readouterr()

    # The file should contain the data
    with open(file_path, "rb") as f:
        loaded = pickle.load(f)
    assert loaded == data
    # The output should contain the description and a timing
    assert captured.out.startswith("Saving file... ")
    assert "done. (" in captured.out
    reported_time = float(captured.out.split("done. (")[1].rstrip("s)\n"))
    assert 0 <= reported_time <= end - start + 0.1

def test_exception_propagates_and_prints(tmp_path, capsys):
    """Test that an exception inside the block propagates and the timing is printed."""
    @work_in_progress("Error test")
    def raise_error():
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        raise_error()
    captured = capsys.readouterr()
    # The output should contain the description and a timing even after exception
    assert captured.out.startswith("Error test... ")
    assert "done. (" in captured.out
    reported_time = float(captured.out.split("done. (")[1].rstrip("s)\n"))
    assert reported_time >= 0
