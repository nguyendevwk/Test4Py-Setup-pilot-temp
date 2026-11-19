import os
import pytest
from pysnooper.tracer import FileWriter


def test_write_creates_file_and_appends(tmp_path):
    """FileWriter should create a new file and append when overwrite is False."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=True)

    # First write should create the file with content
    writer.write("first line\n")
    assert file_path.read_text(encoding="utf-8") == "first line\n"

    # Subsequent write should append
    writer.write("second line\n")
    assert file_path.read_text(encoding="utf-8") == "first line\nsecond line\n"


def test_overwrite_flag_resets_after_write(tmp_path):
    """After a write, the overwrite flag should be reset to False."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=True)

    writer.write("content")
    # After writing, overwrite should be False
    assert writer.overwrite is False

    # Now writing again should append, not overwrite
    writer.write("more")
    assert file_path.read_text(encoding="utf-8") == "contentmore"


def test_write_raises_on_invalid_path(tmp_path):
    """FileWriter should raise an exception when the path is invalid."""
    # Use a directory path that cannot be opened for writing
    dir_path = tmp_path / "nonexistent_dir"
    writer = FileWriter(dir_path, overwrite=True)

    # Attempting to write should raise an OSError (FileNotFoundError)
    with pytest.raises(OSError):
        writer.write("data")
