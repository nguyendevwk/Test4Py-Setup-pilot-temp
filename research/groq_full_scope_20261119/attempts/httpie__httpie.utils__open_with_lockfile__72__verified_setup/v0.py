import os
import tempfile
import pytest
from pathlib import Path
from httpie.utils import open_with_lockfile

def test_open_with_lockfile_normal(tmp_path):
    # Create a temporary file and write to it using the context manager
    test_file = tmp_path / "test.txt"
    test_file.write_text("")  # ensure file exists

    lock_dir = Path(tempfile.gettempdir())
    lock_file = lock_dir / base64.b64encode(os.fsencode(test_file)).decode()

    # Ensure no lock file exists before
    assert not lock_file.exists()

    with open_with_lockfile(test_file, "w") as f:
        f.write("hello")

    # After exiting the context, the lock file should be removed
    assert not lock_file.exists()

    # Verify content was written
    assert test_file.read_text() == "hello"

def test_open_with_lockfile_lock_conflict(tmp_path):
    # Create a temporary file and open it to create a lock
    test_file = tmp_path / "conflict.txt"
    test_file.write_text("data")

    lock_dir = Path(tempfile.gettempdir())
    lock_file = lock_dir / base64.b64encode(os.fsencode(test_file)).decode()

    # First context creates the lock file
    with open_with_lockfile(test_file, "r") as f:
        assert f.read() == "data"
        # While inside the context, the lock file exists
        assert lock_file.exists()

        # Attempt to open the same file again in the same process
        # This should raise a NameError because LockFileError is not defined
        with pytest.raises(NameError):
            with open_with_lockfile(test_file, "r") as f2:
                f2.read()

    # After exiting the first context, the lock file should be removed
    assert not lock_file.exists()

def test_open_with_lockfile_file_not_found(tmp_path):
    # Reference a non-existent file
    missing_file = tmp_path / "missing.txt"

    # Opening a non-existent file should raise FileNotFoundError
    with pytest.raises(FileNotFoundError):
        with open_with_lockfile(missing_file, "r") as f:
            f.read()
