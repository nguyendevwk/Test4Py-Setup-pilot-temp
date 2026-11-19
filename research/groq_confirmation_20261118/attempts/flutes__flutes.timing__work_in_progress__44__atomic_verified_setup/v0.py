import time
import builtins
import pytest
from flutes.timing import work_in_progress


def test_work_in_progress_prints_and_measures_time(capsys):
    """The context manager should print a start message, yield control,
    then print a completion message with a positive elapsed time."""
    with work_in_progress("Test task"):
        time.sleep(0.1)
    out, err = capsys.readouterr()
    assert "Test task... " in out
    assert "done. (" in out
    # Extract the time value from the printed message
    time_str = out.split("done. (")[1].rstrip("s)")
    elapsed = float(time_str)
    assert elapsed >= 0.1, f"Elapsed time {elapsed} is less than expected sleep"


def test_work_in_progress_zero_sleep(capsys):
    """When the block does nothing, the elapsed time should be very small."""
    with work_in_progress("No-op"):
        pass
    out, _ = capsys.readouterr()
    assert "No-op... " in out
    assert "done. (" in out
    time_str = out.split("done. (")[1].rstrip("s)")
    elapsed = float(time_str)
    assert elapsed < 0.01, f"Elapsed time {elapsed} should be near zero for no-op"


def test_work_in_progress_multiple_calls(tmp_path, capsys):
    """Multiple consecutive uses should each print correctly and measure time independently."""
    file_path = tmp_path / "dummy.txt"
    file_path.write_text("hello")
    with work_in_progress("Read file"):
        data = file_path.read_text()
    with work_in_progress("Write file"):
        file_path.write_text(data.upper())
    out, _ = capsys.readouterr()
    # Check that both start messages appear
    assert "Read file... " in out
    assert "Write file... " in out
    # Ensure each block has a corresponding done message
    assert out.count("done. (") == 2
    # Verify that the file contents were transformed correctly
    assert file_path.read_text() == "HELLO"
