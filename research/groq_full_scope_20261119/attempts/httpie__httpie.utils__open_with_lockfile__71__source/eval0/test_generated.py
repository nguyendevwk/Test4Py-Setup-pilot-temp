import os
import tempfile
import pytest
from pathlib import Path
from httpie.utils import open_with_lockfile, LockFileError


def test_open_with_lockfile_creates_and_removes_lock(tmp_path: Path):
    """Normal usage: file is opened and lock file is removed after context."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello world")

    lock_file = Path(tempfile.gettempdir()) / \
        os.path.basename(str(test_file)).encode().hex()

    # Ensure no lock file exists before
    assert not lock_file.exists()

    with open_with_lockfile(test_file, "r") as f:
        # Inside context: lock file should exist
        assert lock_file.exists()
        content = f.read()
        assert content == "hello world"

    # After context: lock file should be removed
    assert not lock_file.exists()


def test_open_with_lockfile_raises_on_existing_lock(tmp_path: Path):
    """If another process has created the lock file, opening should fail."""
    test_file = tmp_path / "locked.txt"
    test_file.write_text("data")

    lock_file = Path(tempfile.gettempdir()) / \
        os.path.basename(str(test_file)).encode().hex()
    lock_file.touch()  # Simulate existing lock

    with pytest.raises(LockFileError):
        with open_with_lockfile(test_file, "r"):
            pass

    # Clean up
    lock_file.unlink()


def test_open_with_lockfile_removes_lock_on_exception(tmp_path: Path):
    """If an exception occurs inside the context, the lock file is still removed."""
    test_file = tmp_path / "error.txt"
    test_file.write_text("content")

    lock_file = Path(tempfile.gettempdir()) / \
        os.path.basename(str(test_file)).encode().hex()

    try:
        with open_with_lockfile(test_file, "r") as f:
            assert lock_file.exists()
            raise RuntimeError("intentional error")
    except RuntimeError:
        pass

    # After exception, lock file should be removed
    assert not lock_file.exists()
