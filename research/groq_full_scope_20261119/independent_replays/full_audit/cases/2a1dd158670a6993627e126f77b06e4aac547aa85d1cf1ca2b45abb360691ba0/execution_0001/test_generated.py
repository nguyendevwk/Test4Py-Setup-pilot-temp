import os
import pytest
from pysnooper.tracer import FileWriter

def test_write_creates_file_and_appends(tmp_path):
    """FileWriter should create a new file and append when overwrite is False."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=True)
    writer.write("first line\n")
    # After first write, overwrite flag should be reset
    assert writer.overwrite is False
    # Append second line
    writer.write("second line\n")
    content = file_path.read_text(encoding="utf-8")
    assert content == "first line\nsecond line\n"

def test_overwrite_flag_rewrites_file(tmp_path):
    """When overwrite is True, FileWriter should rewrite the file."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=True)
    writer.write("initial\n")
    # Set overwrite to True again to rewrite
    writer.overwrite = True
    writer.write("replaced\n")
    content = file_path.read_text(encoding="utf-8")
    assert content == "replaced\n"

def test_write_invalid_path_raises(tmp_path):
    """FileWriter should raise an OSError when the path is invalid."""
    # Use a directory path that is not writable (e.g., root on Unix)
    invalid_path = os.path.join("/", "nonexistent_dir", "file.txt")
    writer = FileWriter(invalid_path, overwrite=True)
    with pytest.raises(OSError):
        writer.write("data")
