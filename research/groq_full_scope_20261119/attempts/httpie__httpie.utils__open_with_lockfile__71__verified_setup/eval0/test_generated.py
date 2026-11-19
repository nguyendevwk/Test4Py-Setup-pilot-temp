import os
import tempfile
import pytest
from pathlib import Path
from httpie.utils import open_with_lockfile, LockFileError


def test_open_with_lockfile_creates_and_removes_lock(tmp_path: Path):
    """Normal usage: file is opened, lock file created, then removed."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text("initial")

    lock_dir = Path(tempfile.gettempdir())
    lock_file = lock_dir / Path(test_file).name  # base64 encoded name

    # Ensure no lock file exists before
    assert not lock_file.exists()

    with open_with_lockfile(test_file, "w") as f:
        # While inside the context, the lock file should exist
        assert lock_file.exists()
        f.write("updated")

    # After context exit, lock file should be removed
    assert not lock_file.exists()

    # Verify file contents were updated
    assert test_file.read_text() == "updated"


def test_open_with_lockfile_raises_on_existing_lock(tmp_path: Path):
    """If another process has already created the lock file, a LockFileError is raised."""
    test_file = tmp_path / "locked.txt"
    test_file.write_text("content")

    lock_dir = Path(tempfile.gettempdir())
    lock_file = lock_dir / Path(test_file).name

    # Manually create the lock file to simulate a lock held by another process
    lock_file.touch()

    with pytest.raises(LockFileError):
        with open_with_lockfile(test_file, "r") as _:
            pass

    # Clean up the manually created lock file
    lock_file.unlink()


def test_open_with_lockfile_file_not_found(tmp_path: Path):
    """Attempting to open a non‑existent file should raise FileNotFoundError."""
    missing_file = tmp_path / "does_not_exist.txt"

    with pytest.raises(FileNotFoundError):
        with open_with_lockfile(missing_file, "r") as _:
            pass
