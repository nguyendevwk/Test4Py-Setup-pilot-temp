import os
import tempfile
import pytest
from pathlib import Path
from httpie.utils import open_with_lockfile, LockFileError


def test_open_with_lockfile_reads_and_writes(tmp_path: Path):
    """Normal usage: file is opened, written to, read from, and lockfile is cleaned up."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")

    # Open the file with the lockfile context manager
    with open_with_lockfile(test_file, "r") as f:
        content = f.read()
    assert content == "hello world"

    # Verify that the lockfile was created and then removed
    file_id = os.fsencode(test_file).decode()
    lockfile = Path(tempfile.gettempdir()) / file_id
    assert not lockfile.exists(), "Lockfile should be removed after context exit"


def test_open_with_lockfile_lockfile_error(tmp_path: Path):
    """If a lockfile already exists, open_with_lockfile should raise LockFileError."""
    test_file = tmp_path / "locked.txt"
    test_file.write_text("locked content")

    # Manually create the lockfile to simulate a concurrent lock
    file_id = os.fsencode(test_file).decode()
    lockfile = Path(tempfile.gettempdir()) / file_id
    lockfile.touch()

    with pytest.raises(LockFileError):
        with open_with_lockfile(test_file, "r") as _:
            pass

    # Clean up the manually created lockfile
    lockfile.unlink()


def test_open_with_lockfile_closes_file(tmp_path: Path):
    """The file should be closed after the generator exits."""
    test_file = tmp_path / "close.txt"
    test_file.write_text("close test")

    # Open the file and keep a reference to the file object
    gen = open_with_lockfile(test_file, "r")
    f = next(gen)
    # The file should be open while inside the generator
    assert not f.closed
    # Exhaust the generator to trigger finally block
    try:
        next(gen)
    except StopIteration:
        pass
    # After generator exit, the file should be closed
    assert f.closed
