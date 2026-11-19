import os
import pytest
from pysnooper.tracer import FileWriter

def test_write_appends_and_resets_overwrite(tmp_path):
    """FileWriter should append when overwrite is False and reset flag."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=True)

    # First write with overwrite=True should create file and write content
    writer.write("first\n")
    assert file_path.read_text(encoding="utf-8") == "first\n"

    # Subsequent write should append because overwrite flag was reset
    writer.write("second\n")
    assert file_path.read_text(encoding="utf-8") == "first\nsecond\n"

    # Explicitly set overwrite to True again and write
    writer.overwrite = True
    writer.write("third\n")
    assert file_path.read_text(encoding="utf-8") == "third\n"

def test_write_empty_string(tmp_path):
    """Writing an empty string should create an empty file without error."""
    file_path = tmp_path / "empty.txt"
    writer = FileWriter(file_path, overwrite=True)

    writer.write("")
    # File should exist and be empty
    assert file_path.exists()
    assert file_path.read_bytes() == b""

def test_write_invalid_path_raises(tmp_path):
    """Attempting to write to a directory path should raise an OSError."""
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    writer = FileWriter(dir_path, overwrite=True)

    with pytest.raises(OSError):
        writer.write("content")
