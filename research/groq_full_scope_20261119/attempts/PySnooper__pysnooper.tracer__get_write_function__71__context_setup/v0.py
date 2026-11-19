import sys
import os
import pytest
from pysnooper.tracer import get_write_function, FileWriter

def test_write_to_file_and_overwrite(tmp_path):
    # Create a temporary file path
    file_path = tmp_path / "output.txt"
    # First write with overwrite=True
    writer = get_write_function(file_path, overwrite=True)
    writer("first line\n")
    # Verify file content
    assert file_path.read_text(encoding="utf-8") == "first line\n"
    # Second write without overwrite (append mode)
    writer = get_write_function(file_path, overwrite=False)
    writer("second line\n")
    assert file_path.read_text(encoding="utf-8") == "first line\nsecond line\n"
    # Now use overwrite=True again to replace content
    writer = get_write_function(file_path, overwrite=True)
    writer("new content\n")
    assert file_path.read_text(encoding="utf-8") == "new content\n"

def test_overwrite_flag_with_non_path_raises():
    # Passing a callable with overwrite=True should raise
    with pytest.raises(Exception) as excinfo:
        get_write_function(lambda x: x, overwrite=True)
    assert "`overwrite=True` can only be used when writing content to file." in str(excinfo.value)

def test_write_function_callable_output():
    # Define a simple callable that records written strings
    recorded = []
    def my_writer(s):
        recorded.append(s)
    writer = get_write_function(my_writer, overwrite=False)
    writer("hello")
    writer("world")
    assert recorded == ["hello", "world"]
