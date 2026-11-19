import os
import tempfile
import pytest
from pathlib import Path
from httpie.utils import open_with_lockfile, LockFileError


def test_open_with_lockfile_creates_and_removes_lock(tmp_path):
    """Normal usage: file is opened, lockfile created and removed."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello world")

    lockfile = Path(tempfile.gettempdir()) / \
        os.fsencode(test_file).decode('utf-8').encode('base64').decode()

    # Ensure no lockfile exists before
    assert not lockfile.exists()

    with open_with_lockfile(test_file, "r") as f:
        # Inside context: lockfile should exist
        assert lockfile.exists()
        content = f.read()
        assert content == "hello world"

    # After context: lockfile should be removed
    assert not lockfile.exists()


def test_open_with_lockfile_raises_on_existing_lock(tmp_path):
    """If another process has created the lockfile, opening should fail."""
    test_file = tmp_path / "locked.txt"
    test_file.write_text("locked")

    # Manually create the lockfile to simulate a lock
    lockfile = Path(tempfile.gettempdir()) / \
        os.fsencode(test_file).decode('utf-8').encode('base64').decode()
    lockfile.touch()

    with pytest.raises(LockFileError):
        with open_with_lockfile(test_file, "r"):
            pass

    # Clean up the manually created lockfile
    lockfile.unlink()


def test_open_with_lockfile_removes_lock_on_exception(tmp_path):
    """Lockfile must be removed even if an exception occurs inside the context."""
    test_file = tmp_path / "error.txt"
    test_file.write_text("error")

    lockfile = Path(tempfile.gettempdir()) / \
        os.fsencode(test_file).decode('utf-8').encode('base64').decode()

    try:
        with open_with_lockfile(test_file, "r") as f:
            assert lockfile.exists()
            raise RuntimeError("intentional failure")
    except RuntimeError:
        pass

    # After exception, lockfile should be cleaned up
    assert not lockfile.exists()
