import os
import pytest
from pysnooper.tracer import FileWriter

def test_write_creates_file_and_appends(tmp_path):
    """FileWriter should create a new file and append when overwrite is False."""
    file_path = tmp_path / "out.txt"
    writer = FileWriter(file_path, overwrite=True)
    writer.write("first line\n")
    # After first write, overwrite flag should be reset
    assert writer.overwrite is False
    # Append second line
    writer.write("second line\n")
    content = file_path.read_text(encoding="utf-8")
    assert content == "first line\nsecond line\n"

def test_overwrite_flag_resets_after_write(tmp_path):
    """After a write, the overwrite flag should be set to False regardless of initial value."""
    file_path = tmp_path / "out2.txt"
    writer = FileWriter(file_path, overwrite=True)
    writer.write("content")
    # overwrite flag should now be False
    assert writer.overwrite is False
    # Subsequent write should append
    writer.write("more")
    assert file_path.read_text(encoding="utf-8") == "contentmore"

def test_write_invalid_path_raises(tmp_path):
    """Writing to an invalid path should raise an OSError."""
    # Construct a path that is likely invalid on most systems
    invalid_path = tmp_path / "nonexistent_dir" / "file.txt"
    writer = FileWriter(invalid_path, overwrite=True)
    with pytest.raises(OSError):
        writer.write("data")
