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
    # Passing a stream (io.StringIO) with overwrite=True should raise
    stream = io.StringIO()
    with pytest.raises(Exception, match="`overwrite=True` can only be used"):
        get_write_function(stream, overwrite=True)

def test_write_to_callable_and_stderr(monkeypatch, capsys):
    # Callable output
    captured = []
    def custom_writer(s):
        captured.append(s)
    writer = get_write_function(custom_writer, overwrite=False)
    writer("foo")
    assert captured == ["foo"]

    # None output writes to stderr
    writer_stderr = get_write_function(None, overwrite=False)
    writer_stderr("bar")
    captured_err = capsys.readouterr().err
    assert "bar" in captured_err
