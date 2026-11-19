import sys
import io
import os
import pytest
from httpie.uploads import is_stdin

def test_is_stdin_with_sys_stdin(tmp_path):
    """When the file is sys.stdin, is_stdin should return True."""
    assert is_stdin(sys.stdin) is True

def test_is_stdin_with_regular_file(tmp_path):
    """When the file is a regular file, is_stdin should return False."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    with open(file_path, "rb") as f:
        assert is_stdin(f) is False

def test_is_stdin_with_no_fileno_object(tmp_path):
    """When the object has no fileno method, is_stdin should return False."""
    # StringIO does not have a fileno method
    sio = io.StringIO("data")
    assert is_stdin(sio) is False
