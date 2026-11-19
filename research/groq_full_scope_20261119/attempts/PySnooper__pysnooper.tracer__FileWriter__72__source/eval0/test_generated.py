import os
import pytest
from pysnooper.tracer import FileWriter

def test_write_appends(tmp_path):
    """FileWriter should append when overwrite is False."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=False)
    writer.write("first line\n")
    writer.write("second line\n")
    content = file_path.read_text(encoding="utf-8")
    assert content == "first line\nsecond line\n"

def test_overwrite_flag(tmp_path):
    """After a write, overwrite flag should reset to False."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=True)
    writer.write("initial\n")
    # overwrite should now be False
    writer.write("appended\n")
    content = file_path.read_text(encoding="utf-8")
    assert content == "initial\nappended\n"

def test_invalid_path_raises(tmp_path):
    """Writing to an invalid path should raise an OSError."""
    # Create a directory and use it as a file path
    dir_path = tmp_path / "not_a_file"
    dir_path.mkdir()
    writer = FileWriter(dir_path, overwrite=True)
    with pytest.raises(OSError):
        writer.write("data")
