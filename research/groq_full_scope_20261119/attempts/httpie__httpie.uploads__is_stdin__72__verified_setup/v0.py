import sys
import os
import io
import tempfile
import pytest
from httpie.uploads import is_stdin


def test_is_stdin_with_sys_stdin(tmp_path):
    """
    Passing sys.stdin should return True because its fileno is 0.
    """
    assert is_stdin(sys.stdin) is True


def test_is_stdin_with_regular_file(tmp_path):
    """
    Passing a regular file object should return False because its fileno is not 0.
    """
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")
    with open(file_path, "rb") as f:
        assert is_stdin(f) is False


def test_is_stdin_with_non_fileno_object(tmp_path):
    """
    Passing an object that does not provide fileno or raises an exception
    should return False.
    """
    class NoFileno:
        pass

    class RaisesFileno:
        def fileno(self):
            raise OSError("no fileno")

    assert is_stdin(NoFileno()) is False
    assert is_stdin(RaisesFileno()) is False
