import sys
import os
import pytest
from pysnooper.tracer import get_write_function, FileWriter

def test_write_to_stderr_when_output_is_none(capsys):
    """When output is None, the returned function writes to sys.stderr."""
    write = get_write_function(None, overwrite=False)
    test_msg = "hello stderr\n"
    write(test_msg)
    captured = capsys.readouterr()
    assert captured.err == test_msg
    assert captured.out == ""

def test_write_to_file_and_overwrite(tmp_path):
    """When output is a path, the returned function writes to the file and respects overwrite flag."""
    file_path = tmp_path / "log.txt"
    write = get_write_function(file_path, overwrite=True)
    write("first line\n")
    # overwrite should be True initially, so file is created anew
    assert file_path.read_text(encoding="utf-8") == "first line\n"
    # subsequent writes should append because overwrite flag is reset
    write("second line\n")
    assert file_path.read_text(encoding="utf-8") == "first line\nsecond line\n"

def test_overwrite_flag_error_when_output_not_path():
    """Providing overwrite=True with a non-path output raises an exception."""
    with pytest.raises(Exception, match="`overwrite=True` can only be used when writing"):
        get_write_function(lambda x: x, overwrite=True)
