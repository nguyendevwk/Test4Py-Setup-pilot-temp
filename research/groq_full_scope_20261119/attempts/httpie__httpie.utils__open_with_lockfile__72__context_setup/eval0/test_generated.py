import os
import tempfile
import pytest
from pathlib import Path
from httpie.utils import open_with_lockfile, LockFileError


def test_open_with_lockfile_success(tmp_path):
    """Verify that a file can be opened and read/write within the context."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello world")

    # Use the context manager to read the file
    with open_with_lockfile(test_file, "r") as f:
        content = f.read()
    assert content == "hello world"

    # Use the context manager to write to the file
    with open_with_lockfile(test_file, "w") as f:
        f.write("new content")
    assert test_file.read_text() == "new content"

    # Ensure the lock file has been removed after the context
    lock_id = os.fsencode(test_file).decode()
    lock_path = Path(tempfile.gettempdir()) / lock_id
    assert not lock_path.exists()


def test_open_with_lockfile_lock_conflict(tmp_path):
    """Verify that attempting to open a file that is already locked raises LockFileError."""
    test_file = tmp_path / "locked.txt"
    test_file.write_text("locked")

    # Manually create the lock file to simulate a concurrent lock
    lock_id = os.fsencode(test_file).decode()
    lock_path = Path(tempfile.gettempdir()) / lock_id
    lock_path.touch()

    with pytest.raises(LockFileError) as excinfo:
        with open_with_lockfile(test_file, "r") as _:
            pass
    assert "Can't modify a locked file." in str(excinfo.value)

    # Clean up the manually created lock file
    lock_path.unlink()


def test_open_with_lockfile_invalid_path(tmp_path):
    """Verify that opening a non-existent file raises FileNotFoundError."""
    non_existent = tmp_path / "does_not_exist.txt"
    with pytest.raises(FileNotFoundError):
        with open_with_lockfile(non_existent, "r") as _:
            pass
