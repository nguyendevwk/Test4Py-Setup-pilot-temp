import os
import pytest
from pysnooper.tracer import FileWriter

def test_write_appends_when_overwrite_false(tmp_path):
    """FileWriter should append when overwrite flag is False."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=False)
    writer.write("first line\n")
    writer.write("second line\n")
    content = file_path.read_text(encoding="utf-8")
    assert content == "first line\nsecond line\n"

def test_write_overwrites_when_overwrite_true(tmp_path):
    """FileWriter should overwrite the file on the first write when overwrite flag is True."""
    file_path = tmp_path / "log.txt"
    writer = FileWriter(file_path, overwrite=True)
    writer.write("initial content\n")
    # Subsequent write should append because overwrite flag is reset
    writer.write("appended content\n")
    content = file_path.read_text(encoding="utf-8")
    assert content == "initial content\nappended content\n"

def test_write_raises_on_invalid_path(tmp_path):
    """FileWriter should raise an OSError when attempting to write to an invalid path."""
    # Construct a path that is unlikely to exist on any system
    invalid_path = tmp_path / "nonexistent_dir" / "file.txt"
    writer = FileWriter(invalid_path, overwrite=True)
    with pytest.raises(OSError):
        writer.write("data")
