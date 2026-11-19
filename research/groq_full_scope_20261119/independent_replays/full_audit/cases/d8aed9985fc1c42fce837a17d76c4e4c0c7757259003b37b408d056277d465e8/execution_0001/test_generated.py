import sys
import os
import io
import pytest
from pysnooper.tracer import get_write_function
from pysnooper import utils

def test_write_to_file_and_overwrite(tmp_path):
    # Create a temporary file and write to it
    file_path = tmp_path / "output.txt"
    writer = get_write_function(file_path, overwrite=False)
    writer("hello\n")
    # Verify content
    assert file_path.read_text() == "hello\n"

    # Overwrite the file
    writer_overwrite = get_write_function(file_path, overwrite=True)
    writer_overwrite("world\n")
    assert file_path.read_text() == "world\n"

def test_overwrite_error_for_non_path_output():
    # Passing a stream (not a path) with overwrite=True should raise
    stream = io.StringIO()
    with pytest.raises(Exception, match="`overwrite=True` can only be used when writing"):
        get_write_function(stream, overwrite=True)

def test_write_to_stderr_and_callable(monkeypatch):
    # Capture stderr
    captured = io.StringIO()
    monkeypatch.setattr(sys, "stderr", captured)

    # get_write_function with output=None writes to stderr
    writer = get_write_function(None, overwrite=False)
    writer("error message\n")
    assert captured.getvalue() == "error message\n"

    # get_write_function with a custom callable
    called = {"value": None}
    def custom_writer(s):
        called["value"] = s

    writer_callable = get_write_function(custom_writer, overwrite=False)
    writer_callable("custom\n")
    assert called["value"] == "custom\n"
