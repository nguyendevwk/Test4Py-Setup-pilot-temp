import os
import sys
import pytest
from pysnooper.tracer import get_write_function
from pysnooper import utils

def test_write_to_file(tmp_path):
    """Writing to a file path should create the file with the given content."""
    file_path = tmp_path / "output.txt"
    write = get_write_function(file_path, overwrite=True)
    write("hello\n")
    # Verify file content
    assert file_path.read_text() == "hello\n"

def test_overwrite_flag_error():
    """Passing overwrite=True with a non-path output should raise an exception."""
    with pytest.raises(Exception, match="`overwrite=True` can only be used"):
        get_write_function(output=print, overwrite=True)

def test_callable_output():
    """When a callable is provided, it should be used directly."""
    captured = []
    def my_writer(s):
        captured.append(s)
    write = get_write_function(my_writer, overwrite=False)
    write("test")
    assert captured == ["test"]
